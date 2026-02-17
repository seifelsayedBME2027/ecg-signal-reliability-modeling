import numpy as np
import wfdb
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load ECG
record = wfdb.rdrecord(
    "data/raw/mit-bih-arrhythmia-database-1.0.0/100"
)
ecg = record.p_signal[:, 0]
fs = record.fs

# Bandpass filter parameters
lowcut = 0.5
highcut = 40.0
order = 4

# Design Butterworth bandpass filter
nyquist = 0.5 * fs
low = lowcut / nyquist
high = highcut / nyquist

b, a = butter(order, [low, high], btype="band")

# Apply filter (zero-phase)
filtered_ecg = filtfilt(b, a, ecg)

# Plot comparison (zoomed)
plt.figure(figsize=(10, 4))
plt.plot(ecg[:2000], label="Raw ECG", alpha=0.6)
plt.plot(filtered_ecg[:2000], label="Filtered ECG", linewidth=2)
plt.legend()
plt.title("Raw vs Filtered ECG (~5.5 seconds)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()
