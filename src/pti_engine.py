import numpy as np
from scipy.signal import find_peaks


# ============================================================
# 1. R-Peak Detection
# ============================================================

def detect_r_peaks(ecg_signal, fs):
    peaks, _ = find_peaks(
        ecg_signal,
        distance=fs * 0.4,
        height=0.5
    )
    return peaks


# ============================================================
# 2. RR Interval Cleaning
# ============================================================

def compute_clean_rr(r_peaks, fs):
    rr_intervals = np.diff(r_peaks) / fs
    rr_clean = rr_intervals[
        (rr_intervals > 0.3) & (rr_intervals < 2.0)
    ]
    return rr_clean


# ============================================================
# 3. Sliding Window PTI
# ============================================================

def compute_pti(rr_intervals_clean, window_size=30, step_size=5):

    if len(rr_intervals_clean) < 10:
        return np.array([]), np.array([])

    rr_times = np.cumsum(rr_intervals_clean)

    start_time = 0
    end_time = rr_times[-1]

    window_centers = []
    pti_scores = []

    while start_time + window_size < end_time:

        mask = (rr_times >= start_time) & \
               (rr_times < start_time + window_size)

        rr_window = rr_intervals_clean[mask]

        if len(rr_window) > 5:

            # Signal Integrity
            expected_beats = window_size / np.mean(rr_window)
            valid_ratio = len(rr_window) / expected_beats
            signal_integrity = min(valid_ratio, 1)

            # Physiologic Plausibility
            hr_window = 60 / rr_window
            physiologic_score = np.mean(
                (hr_window > 40) & (hr_window < 180)
            )

            # Rhythm Stability
            rmssd_window = np.sqrt(
                np.mean(np.diff(rr_window) ** 2)
            )
            stability_score = 1 / (1 + rmssd_window * 10)

            # Final PTI
            pti = (
                0.4 * signal_integrity +
                0.3 * physiologic_score +
                0.3 * stability_score
            )

            window_centers.append(start_time + window_size / 2)
            pti_scores.append(pti)

        start_time += step_size

    return np.array(window_centers), np.array(pti_scores)
