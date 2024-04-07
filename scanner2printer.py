import sys
import os
import time
import json
import serial

sys.path.append(r".")
from PyRingIt import RingIT # noqa
from utils.record import Record # noqa
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION  # noqa

with open(DEFAULT_CONFIG_FILE_LOCATION, "r") as config_file:
    config_data = json.load(config_file)
port, baudrate, prefix  = config_data["devices"]["qr_scanner"]["port"], config_data["devices"]["qr_scanner"]["baudrate"], config_data["devices"]["qr_scanner"]["prefix"]


class BarcodeScanner:
    def __init__(self):
        self.ser = serial.Serial(timeout=0.01)
        self.first_scan_result = None

    def start_scanning(self):
        if self.init_ser() != 0:
            print("Couldn't open serial port due to an error")
            self.ser.close()
            return

        print("Scanning for barcodes...")
        while self.first_scan_result is None:
            ret_val = self.listen_to_port()
            if isinstance(ret_val, str):
                self.handle_scan_result(ret_val)
            elif ret_val in [-1, -2]:
                print("Invalid QR code" if ret_val == -1 else "Serial port read exception")
            time.sleep(0.1)
        self.ser.close()
        print("Scan Finished")

    def init_ser(self):
        self.ser.close()
        self.ser.port, self.ser.baudrate = port, int(baudrate)
        try:
            self.ser.open()
        except Exception as e:
            print(f"Couldn't open serial port due to an error {e}")
            return 1
        return 0

    def listen_to_port(self):
        try:
            qr_output = self.ser.readline()
        except Exception as e:
            print(f"QR scanner read exception {e}")
            qr_output = b''
            self.ser.close()
            return -2
        if len(qr_output) > 1:
            full_str_qr_output = qr_output.decode('utf-8')
            str_qr_output = full_str_qr_output.replace(prefix, "")
            return str_qr_output
        return 0

    def handle_scan_result(self, result):
        print("Scan Result:", result)
        if self.first_scan_result is None:
            self.first_scan_result = result


def main_menu():
    rit = RingIT("video")
    scanner = BarcodeScanner()

    while True:
        print("\033[4mGenerate and print QR code:\033[0m")
        print("1. Scan")
        print("2. Manually input a UUID")
        print("3. Exit")
        current_uuid = ""
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            # Option 1: Scan and print barcode
            scanner.start_scanning()
            current_uuid = scanner.first_scan_result
        elif choice == '2':
            # Option 2: Manually input a UUID, generate a barcode, and then print it
            current_uuid = input("Enter a UUID: ")
        elif choice == '3':
            print("\n Exiting... \n")
            break
        else:
            print("Invalid choice. Please choose a valid option (1/2/3)")
            continue

        # Generate the QR image without specifying quality
        try:
            print("Creating QR image...")
            record = Record(rit.ring_it_params, rit.mv_session, 25, scan=current_uuid)
            rit.create_qr_image(record)
            print("\n The path to access your barcode is:", os.path.normpath(record.qrimage) + "\n")
            # record.qrimage = os.path.normpath(r'C:\Users\PortyOne\Desktop\qr_with_text\dfg_text.png')
            ret = rit.print_qr(r"C:\Users\PortyOne\Desktop\qr_with_text\dfg_text.png")
            if ret != 0:
                raise ValueError("Couldn't print, check file path")
        except Exception as e:
            print(e)

        print("QR image printed successfully!")


if __name__ == "__main__":
    main_menu()

    # If you have issues with printing - chack qr_printer cofiguration in ring_gui_config (labal size, name of printer, etc)
