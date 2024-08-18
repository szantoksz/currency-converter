# import libs
import sys
import os
import requests
import webbrowser
import json

import tkinter as tk
from tkinter import ttk, messagebox


class Files:
    def __init__(self, filename):
        self.api_key_file_name = f"{filename}.json"
        self.api_key_file_path = os.path.join(self.get_executable_directory(), self.api_key_file_name)
        self.api_key_file_existence = self.check_file_existence(self.api_key_file_path)
        if not self.api_key_file_existence:
            self.create_file(self.api_key_file_path)

    @staticmethod
    def get_executable_directory():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def check_file_existence(path):
        return os.path.exists(path)

    @staticmethod
    def create_file(path):
        with open(path, "w") as file:
            file.write('{"apikey": "NaN"}')


class Gui:
    def __init__(self, apikeyname):
        self.api_key_name = apikeyname
        self.api = Api()
        self.currencies_all = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD",
                               "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN",
                               "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUP", "CVE", "CZK", "DJF",
                               "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL",
                               "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF",
                               "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES",
                               "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD",
                               "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
                               "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB",
                               "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR",
                               "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SOS", "SRD", "SSP", "STN", "SYP",
                               "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH",
                               "UGX", "USD", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF",
                               "XPF", "YER", "ZAR", "ZMW", "ZWL"]

        self.currencies_minimal = ["EUR", "GBP", "HUF", "USD", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "RUB", "SEK",
                                   "NOK", "KRW", "SGD", "PLN", "BRL", "MXN", "ILS", "TRY", "THB", "ZAR", "NZD", "RON",
                                   "CZK", "DKK"]

        self.root = None
        self.window_config()

        self.style = None
        self.window_style()

        self.frame_main = None
        self.window_frames()

        self.label_from = None
        self.label_to = None
        self.label_apikey = None
        self.window_labels()

        self.combobox_from_values = None
        self.combobox_from = None
        self.combobox_to_values = None
        self.combobox_to = None
        self.default_combobox_values()
        self.window_comboboxes()

        self.entry_from = None
        self.entry_to_value = None
        self.entry_to = None
        self.entry_apikey_value = None
        self.entry_apikey = None
        self.set_api_key_entry()
        self.set_to_entry("NaN")
        self.window_entries()

        self.checkbutton_all_currencies_value = None
        self.checkbutton_all_currencies = None
        self.window_checkbuttons()

        self.button_convert = None
        self.button_set = None
        self.button_check = None
        self.button_open_web = None
        self.window_buttons()

        self.window_run()

    def window_config(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.attributes("-fullscreen", False)
        self.root.geometry("316x230")
        self.root.title("Currency Converter")

    def window_style(self):
        self.style = ttk.Style()
        self.style.configure("frame_main.TFrame", background="white")
        self.style.configure("checkbutton_all_currencies.TCheckbutton", background="white")

    def window_frames(self):
        self.frame_main = ttk.Frame(self.root, style="frame_main.TFrame")
        self.frame_main.pack(fill="both", expand=True)

    def window_labels(self):
        self.label_from = ttk.Label(self.frame_main, text="From:", background="white", font=("Arial", 15, "bold"))
        self.label_from.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

        self.label_to = ttk.Label(self.frame_main, text="To:", background="white", font=("Arial", 15, "bold"))
        self.label_to.grid(row=0, column=0, padx=(190, 0), pady=(10, 0), sticky="w")

        self.label_apikey = ttk.Label(self.frame_main, text="API KEY:", background="white", font=("Arial", 15, "bold"))
        self.label_apikey.grid(row=3, column=0, padx=(10, 0), pady=(45, 0), sticky="w")

    def default_combobox_values(self):
        self.combobox_from_values = self.currencies_minimal
        self.combobox_to_values = self.currencies_minimal

    def window_comboboxes(self):
        self.combobox_from = ttk.Combobox(self.frame_main, values=self.combobox_from_values, width=4)
        self.combobox_from.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        self.combobox_to = ttk.Combobox(self.frame_main, values=self.combobox_from_values, width=4)
        self.combobox_to.grid(row=1, column=0, padx=(190, 0), pady=(0, 0), sticky="w")

    def set_api_key_entry(self):
        self.entry_apikey_value = tk.StringVar(value=self.api.get_current_api_key(self.api_key_name))

    def set_to_entry(self, value):
        self.entry_to_value = tk.StringVar(value=value)

    def window_entries(self):
        self.entry_from = ttk.Entry(self.frame_main, width=10)
        self.entry_from.grid(row=1, column=0, padx=(60, 0), pady=(0, 0), sticky="w")

        self.entry_to = ttk.Entry(self.frame_main, width=10, textvariable=self.entry_to_value)
        self.entry_to.config(state="disabled")
        self.entry_to.grid(row=1, column=0, padx=(240, 0), pady=(0, 0), sticky="w")

        self.entry_apikey = ttk.Entry(self.frame_main, width=24, textvariable=self.entry_apikey_value)
        self.entry_apikey.grid(row=3, column=0, padx=(100, 0), pady=(45, 0), sticky="w")

    def window_checkbuttons(self):
        self.checkbutton_all_currencies_value = tk.BooleanVar()
        self.checkbutton_all_currencies = ttk.Checkbutton(self.frame_main, text="Show All Supported Currencies",
                                                          variable=self.checkbutton_all_currencies_value,
                                                          command=self.checkbutton_all_currencies_click,
                                                          style="checkbutton_all_currencies.TCheckbutton")
        self.checkbutton_all_currencies.grid(row=2, column=0, padx=(10, 0), pady=(25, 0), sticky="w")

    def window_buttons(self):
        self.button_convert = ttk.Button(self.frame_main, text="Convert", command=self.button_convert_click)
        self.button_convert.grid(row=2, column=0, padx=(217, 0), pady=(25, 0), sticky="w")

        self.button_set = ttk.Button(self.frame_main, text="Set", command=self.button_set_click, width=7)
        self.button_set.grid(row=3, column=0, padx=(257, 0), pady=(45, 0), sticky="w")

        self.button_check = ttk.Button(self.frame_main, text="Check", command=self.button_check_click)
        self.button_check.grid(row=4, column=0, padx=(150, 0), pady=(10, 0), sticky="w")

        self.button_open_web = ttk.Button(self.frame_main, text="Open Web", command=self.button_open_web_click)
        self.button_open_web.grid(row=4, column=0, padx=(233, 0), pady=(10, 0), sticky="w")

    def window_run(self):
        self.root.mainloop()

    def checkbutton_all_currencies_click(self):
        if self.checkbutton_all_currencies_value.get():
            temp_value_from = self.combobox_from.get()
            temp_value_to = self.combobox_to.get()
            self.combobox_from_values = self.currencies_all
            self.combobox_to_values = self.currencies_all
            self.window_comboboxes()
            self.combobox_from.set(temp_value_from)
            self.combobox_to.set(temp_value_to)
        else:
            temp_value_from = self.combobox_from.get()
            temp_value_to = self.combobox_to.get()
            self.combobox_from_values = self.currencies_minimal
            self.combobox_to_values = self.currencies_minimal
            self.window_comboboxes()
            self.combobox_from.set(temp_value_from)
            self.combobox_to.set(temp_value_to)

    def button_convert_click(self):
        temp_value_from = self.combobox_from.get()
        temp_value_to = self.combobox_to.get()

        temp_value_from_valid = temp_value_from in self.currencies_all
        temp_value_to_valid = temp_value_to in self.currencies_all

        stop = False

        if not temp_value_from_valid:
            stop = True
            messagebox.showerror("Error", f"'{temp_value_from}' Is Not A Supported Currency")

        if not stop and not temp_value_to_valid:
            stop = True
            messagebox.showerror("Error", f"'{temp_value_to}' Is Not A Supported Currency")

        if not stop and temp_value_from_valid and temp_value_to_valid:
            try:
                float(self.entry_from.get())
            except ValueError:
                temp_value_convert = self.entry_from.get()
                stop = True
                messagebox.showerror("Error", f"'{temp_value_convert}' Is Not Convertable")

        if not stop:
            apikey = self.entry_apikey.get()
            currency1 = self.combobox_from.get()
            currency2 = self.combobox_to.get()
            amount = float(self.entry_from.get())
            response, conversion = self.api.convert_currencies(apikey, currency1, currency2, amount)
            if response != "success":
                messagebox.showerror("Error", "API Key Is Invalid")
            else:
                conversion = round(conversion, 2)
                temp_entry_from = self.entry_from.get()
                self.set_to_entry(conversion)
                self.window_entries()
                self.entry_from.insert(0, temp_entry_from)

    def button_set_click(self):
        apikey = self.entry_apikey.get()
        api_result_response = self.api.check_current_api_key(apikey)
        if api_result_response != "success":
            messagebox.showerror("Error", "API Key Is Invalid")
        else:
            messagebox.showinfo("Success", "Saved New API Key")
            self.api.save_new_api_key(self.api_key_name, apikey)
            self.set_api_key_entry()
            temp_entry_from = self.entry_from.get()
            self.window_entries()
            self.entry_from.insert(0, temp_entry_from)

    def button_check_click(self):
        apikey = self.entry_apikey.get()
        api_result_response = self.api.check_current_api_key(apikey)
        if api_result_response != "success":
            messagebox.showerror("Error", "API Key Is Invalid")
        else:
            messagebox.showinfo("Success", "API Key Is Valid")

    @staticmethod
    def button_open_web_click():
        webbrowser.open("https://www.exchangerate-api.com")


class Api:
    def __init__(self):
        pass

    @staticmethod
    def get_executable_directory():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def get_current_api_key(self, apikeyname):
        api_key_name = f"{apikeyname}.json"
        api_key_path = os.path.join(self.get_executable_directory(), api_key_name)
        with open(api_key_path, "r") as file:
            data = json.load(file)
            return data.get("apikey")

    @staticmethod
    def check_current_api_key(apikey):
        url = f"https://v6.exchangerate-api.com/v6/{apikey}/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data.get("result")

    def save_new_api_key(self, apikeyname, apikey):
        api_key_name = f"{apikeyname}.json"
        api_key_path = os.path.join(self.get_executable_directory(), api_key_name)
        with open(api_key_path, "w") as file:
            content = '{"apikey": "' + apikey + '"}'
            file.write(content)

    @staticmethod
    def convert_currencies(apikey, currency1, currency2, amount):
        url = f"https://v6.exchangerate-api.com/v6/{apikey}/pair/{currency1}/{currency2}/{amount}"
        response = requests.get(url)
        data = response.json()
        if data.get("result") != "success":
            return data.get("result"), "NaN"
        else:
            return data.get("result"), data.get("conversion_result")


def main():
    Files("apikey")
    Gui("apikey")


if __name__ == "__main__":
    main()
