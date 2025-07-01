import matplotlib.pyplot as plt
from bhspc_singlemode.spc import BHSingleMode, BHSingleModeSim

# Toggle simulation mode
use_simulation = True

if use_simulation:
    spc = BHSingleModeSim(collection_time_ms=1000, bins=1024)
    spc.configure(CFD_LOW=10, CFD_HIGH=80, TAC_RANGE=2)
    spc.start_measurement()
    histogram = spc.get_histogram()
else:
    dll_path = r"your .dll file location"
    ini_path = r"your .ini file location"
    spc = BHSingleMode(dll_path, ini_path)
    spc.configure({
        10: 10,   # CFD_LOW
        11: 80,   # CFD_HIGH
        26: 60,   # SYNC_LEVEL
        32: 2,    # TAC_RANGE
        41: 1000  # COLLECTION_TIME
        #add extra parameters with correct para IDs
        #12: 5,  # CFD_HOLDOFF (ns)
        #13: 0,  # CFD_ZC_LEVEL
        #25: -20,  # SYNC_THRESHOLD (mV)
        #27: 4,  # SYNC_HOLDOFF (ns)
        #28: 4,  # SYNC_FREQ_DIV
        #30: 0,  # TRIGGER (0=SW, 1=EXT)
        #33: 10,  # TAC_LIMIT_LOW (%)
        #34: 80,  # TAC_LIMIT_HIGH (%)
        #35: 1,  # TAC_GAIN
        #36: 0,  # TAC_OFFSET (%)
    })
    histogram = spc.start_measurement(page_size=1024)

# Plot the result
plt.plot(histogram)
plt.title("TCSPC Histogram")
plt.xlabel("Time Bins")
plt.ylabel("Photon Counts")
plt.grid(True)
plt.show()
