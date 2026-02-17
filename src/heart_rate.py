import wfdb
import numpy as np
import matplotlib.pyplot as plt

from pti_engine import detect_r_peaks
from pti_engine import compute_clean_rr
from pti_engine import compute_pti

plt.ion()

# ============================================================
# Load ECG
# ============================================================

record = wfdb.rdrecord(
    "./data/raw/mit-bih-arrhythmia-database-1.0.0/100"
)

ecg_signal = record.p_signal[:, 0]
fs = record.fs

# ============================================================
# Clean Signal PTI
# ============================================================

r_peaks = detect_r_peaks(ecg_signal, fs)
rr_clean = compute_clean_rr(r_peaks, fs)

window_centers, pti_scores = compute_pti(rr_clean)

print("Mean Clean PTI:", np.mean(pti_scores))

plt.figure()
plt.plot(window_centers, pti_scores)
plt.title("Clean PTI")
plt.xlabel("Time (s)")
plt.ylabel("PTI")
plt.ylim(0, 1.1)
plt.show()

input("Press Enter to exit...")
