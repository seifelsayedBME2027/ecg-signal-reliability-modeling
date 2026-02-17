import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# Load ECG
record = wfdb.rdrecord(
    "data/raw/mit-bih-arrhythmia-database-1.0.0/100"
)
ecg = record.p_signal[:, 0]
fs = record.fs

# Bandpass filter
lowcut, highcut = 0.5, 40
nyq = 0.5 * fs
b, a = butter(4, [lowcut/nyq, highcut/nyq], btype="band")
filtered_ecg = filtfilt(b, a, ecg)

# R-peak detection
peaks, properties = find_peaks(
    filtered_ecg,
    distance=0.6 * fs,      # minimum 100 BPM max
    height=np.mean(filtered_ecg) + 0.5 * np.std(filtered_ecg)
)

# Plot zoomed ECG with peaks
plt.figure(figsize=(10, 4))
plt.plot(filtered_ecg[:2000], label="Filtered ECG")
# Only plot peaks in the zoomed window
zoom_peaks = peaks[peaks < 2000]

plt.plot(zoom_peaks, 
         filtered_ecg[zoom_peaks], 
         "ro", label="R-peaks")
plt.legend()
plt.title("R-Peak Detection (~5.5 seconds)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()
