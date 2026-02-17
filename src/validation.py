import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

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
# Records to Validate
# ============================================================

records = ["100", "101", "102", "103", "104"]

clean_means = []
noisy_means = []
percent_drops = []

for rec in records:

    print(f"\nProcessing record {rec}")

    record = wfdb.rdrecord(
        f"./data/raw/mit-bih-arrhythmia-database-1.0.0/{rec}"
    )

    ecg_signal = record.p_signal[:, 0]
    fs = record.fs

    # -------- Clean PTI --------
    r_peaks = detect_r_peaks(ecg_signal, fs)
    rr_clean = compute_clean_rr(r_peaks, fs)
    _, pti_clean = compute_pti(rr_clean)

    mean_clean = np.nanmean(pti_clean)
    clean_means.append(mean_clean)

    # -------- Noisy PTI --------
    ecg_noisy = add_motion_artifact(ecg_signal)
    ecg_noisy = add_baseline_drift(ecg_noisy, fs)

    r_peaks_noisy = detect_r_peaks(ecg_noisy, fs)
    rr_noisy = compute_clean_rr(r_peaks_noisy, fs)
    _, pti_noisy = compute_pti(rr_noisy)

    mean_noisy = np.nanmean(pti_noisy)
    noisy_means.append(mean_noisy)

    # -------- Percent Drop --------
    percent_drop = ((mean_clean - mean_noisy) / mean_clean) * 100
    percent_drops.append(percent_drop)

    print("Mean Clean PTI:", round(mean_clean, 4))
    print("Mean Noisy PTI:", round(mean_noisy, 4))
    print("Percent PTI Drop:", round(percent_drop, 2), "%")


# ============================================================
# Summary Statistics
# ============================================================

avg_clean = np.mean(clean_means)
avg_noisy = np.mean(noisy_means)
avg_drop = np.mean(percent_drops)

print("\n==============================")
print("Overall Results")
print("==============================")
print("Average Clean PTI:", round(avg_clean, 4))
print("Average Noisy PTI:", round(avg_noisy, 4))
print("Average Percent Drop:", round(avg_drop, 2), "%")

# Paired t-test
t_stat, p_value = ttest_rel(clean_means, noisy_means)

print("\nPaired T-Test Results")
print("T-statistic:", round(t_stat, 4))
print("P-value:", p_value)

if p_value < 0.05:
    print("Result: Statistically significant PTI degradation under noise.")
else:
    print("Result: No statistically significant degradation detected.")


# ============================================================
# Plot Results
# ============================================================

x = np.arange(len(records))

plt.figure()
plt.bar(x - 0.2, clean_means, width=0.4, label="Clean")
plt.bar(x + 0.2, noisy_means, width=0.4, label="Noisy")

plt.xticks(x, records)
plt.ylabel("Mean PTI")
plt.title("PTI Validation Across Multiple MIT-BIH Records")
plt.ylim(0, 1.1)
plt.legend()
plt.show()

input("Press Enter to exit...")

