import matplotlib.pyplot as plt
from bhspc_singlemode.spc import BHSingleMode, BHSingleModeSim

# Toggle simulation mode
use_simulation = False

if use_simulation:
    spc = BHSingleModeSim(collection_time_ms=1000, bins=1024)
    spc.configure(CFD_LOW=10, CFD_HIGH=80, TAC_RANGE=2)
    spc.start_measurement()
    histogram = spc.get_histogram()
else:
    dll_path = r"C:\Users\purushothaman\PycharmProjects\bhspc_singlemode\spcm64.dll"
    ini_path = r"C:\Users\purushothaman\PycharmProjects\bhspc_singlemode\spcm.ini"
    spc = BHSingleMode(dll_path, ini_path)
    spc.configure({
        10: 10,   # CFD_LOW
        11: 80,   # CFD_HIGH
        26: 60,   # SYNC_LEVEL
        32: 2,    # TAC_RANGE
        41: 1000  # COLLECTION_TIME
    })
    histogram = spc.start_measurement(page_size=1024)

# Plot the result
plt.plot(histogram)
plt.title("TCSPC Histogram")
plt.xlabel("Time Bins")
plt.ylabel("Photon Counts")
plt.grid(True)
plt.show()
