import ctypes
import numpy as np
import time
from ctypes import c_short, c_int, c_ushort, POINTER, byref, c_char_p

class BHSingleMode:
    def __init__(self, dll_path, ini_path):
        self.dll = ctypes.WinDLL(dll_path)
        self.ini_path = ini_path.encode("utf-8")

        self.module = 0  # Assuming one module
        self._define_functions()
        self._init_module()

    def _define_functions(self):
        self.dll.SPC_init.argtypes = [c_char_p]
        self.dll.SPC_init.restype = c_short

        self.dll.SPC_set_parameter.argtypes = [c_int, c_int, c_int]
        self.dll.SPC_set_parameter.restype = c_short

        self.dll.SPC_start_measurement.argtypes = [c_int]
        self.dll.SPC_start_measurement.restype = c_short

        self.dll.SPC_test_state.argtypes = [c_int, POINTER(c_short)]
        self.dll.SPC_test_state.restype = c_short

        self.dll.SPC_read_data_page.argtypes = [c_int, c_int, c_int, POINTER(c_ushort)]
        self.dll.SPC_read_data_page.restype = c_short

        self.dll.SPC_stop_measurement.argtypes = [c_int]
        self.dll.SPC_stop_measurement.restype = c_short

    def _init_module(self):
        ret = self.dll.SPC_init(self.ini_path)
        if ret != 0:
            raise RuntimeError(f"SPC_init failed with code {ret}")
        print("[HW] SPC module initialized.")

    def configure(self, params):
        for param, value in params.items():
            ret = self.dll.SPC_set_parameter(self.module, param, value)
            print(f"[HW] Set param {param} to {value}: {ret}")
            if ret != 0:
                raise RuntimeError(f"Failed to set parameter {param}")

    def start_measurement(self, page_size):
        self.dll.SPC_start_measurement(self.module)
        print("[HW] Measurement started...")
        state = c_short()
        while True:
            self.dll.SPC_test_state(self.module, byref(state))
            if state.value == 0:
                break
            time.sleep(0.1)
        print("[HW] Measurement finished.")

        buffer = (c_ushort * page_size)()
        ret = self.dll.SPC_read_data_page(self.module, 0, 0, buffer)
        if ret != 0:
            raise RuntimeError("Failed to read data.")
        return list(buffer[:page_size])

class BHSingleModeSim:
    def __init__(self, collection_time_ms=1000, bins=1024):
        self.collection_time_ms = collection_time_ms
        self.bins = bins
        self.histogram = [0] * bins

    def configure(self, **kwargs):
        print("[Sim] Configuration accepted:", kwargs)

    def start_measurement(self):
        print("[Sim] Starting simulated measurement...")
        time.sleep(self.collection_time_ms / 1000.0)
        self._generate_histogram()

    def _generate_histogram(self):
        x = np.arange(self.bins)
        decay = np.exp(-x / (self.bins / 10)) * 1000
        noise = np.random.normal(0, 10, self.bins)
        self.histogram = (decay + noise).clip(min=0).astype(int).tolist()

    def get_histogram(self):
        return self.histogram
