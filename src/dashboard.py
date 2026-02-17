import wfdb
import numpy as np
import matplotlib.pyplot as plt

from pti_engine import detect_r_peaks
from pti_engine import compute_clean_rr
from pti_engine import compute_pti


# ============================================================
# Noise Functions
# ============================================================

def add_motion_artifact(ecg, noise_level=0.6):
    noise = noise_level * np.random.randn(len(ecg))
    return ecg + noise

def add_baseline_drift(ecg, fs, drift_strength=0.5):
    t = np.arange(len(ecg)) / fs
    drift = drift_strength * np.sin(2 * np.pi * 0.3 * t)
    return ecg + drift


# ============================================================
# Load ECG Record
# ============================================================

record = wfdb.rdrecord(
    "./data/raw/mit-bih-arrhythmia-database-1.0.0/100"
)

ecg_signal = record.p_signal[:, 0]
fs = record.fs

# Limit duration for cleaner visualization (first 20 seconds)
duration = 120
samples = int(duration * fs)

ecg_signal = ecg_signal[:samples]


# ============================================================
# Clean Processing
# ============================================================

r_peaks_clean = detect_r_peaks(ecg_signal, fs)
rr_clean = compute_clean_rr(r_peaks_clean, fs)
times_clean, pti_clean = compute_pti(rr_clean)


# ============================================================
# Noisy Processing
# ============================================================

ecg_noisy = add_motion_artifact(ecg_signal)
ecg_noisy = add_baseline_drift(ecg_noisy, fs)

r_peaks_noisy = detect_r_peaks(ecg_noisy, fs)
rr_noisy = compute_clean_rr(r_peaks_noisy, fs)
times_noisy, pti_noisy = compute_pti(rr_noisy)


# ============================================================
# Create Dashboard
# ============================================================

fig, axs = plt.subplots(4, 1, figsize=(12, 10))

time_axis = np.arange(len(ecg_signal)) / fs


# 1️⃣ Clean ECG + Peaks
axs[0].plot(time_axis, ecg_signal)
axs[0].scatter(
    r_peaks_clean / fs,
    ecg_signal[r_peaks_clean],
    marker="o"
)
axs[0].set_title("Clean ECG with R-Peaks")
axs[0].set_ylabel("Amplitude")


# 2️⃣ Noisy ECG + Peaks
axs[1].plot(time_axis, ecg_noisy)
axs[1].scatter(
    r_peaks_noisy / fs,
    ecg_noisy[r_peaks_noisy],
    marker="o"
)
axs[1].set_title("Noisy ECG with R-Peaks")
axs[1].set_ylabel("Amplitude")


# 3️⃣ RR Intervals
axs[2].plot(rr_clean, label="Clean RR")
axs[2].plot(rr_noisy, label="Noisy RR")
axs[2].set_title("RR Intervals")
axs[2].set_ylabel("Seconds")
axs[2].legend()


# 4️⃣ PTI Curve
axs[3].plot(times_clean, pti_clean, label="Clean PTI")
axs[3].plot(times_noisy, pti_noisy, label="Noisy PTI")
mean_clean = np.nanmean(pti_clean)
mean_noisy = np.nanmean(pti_noisy)
axs[3].set_title(
    f"Peak Trust Index (Clean: {mean_clean:.3f} | Noisy: {mean_noisy:.3f})"
)
axs[3].set_ylabel("PTI")
axs[3].set_xlabel("Time (s)")
axs[3].set_ylim(0, 1.1)
axs[3].legend()


plt.tight_layout()
plt.subplots_adjust(hspace=0.6)
plt.savefig("pti_dashboard.png", dpi=300)
plt.show()

input("Press Enter to exit...")
