import wfdb
import matplotlib.pyplot as plt

record = wfdb.rdrecord(
    "data/raw/mit-bih-arrhythmia-database-1.0.0/100"
)
ecg = record.p_signal[:, 0]

plt.figure()
plt.plot(ecg)
plt.show()
