import subprocess
import re
from InfoHolderClass import *
import math
import json
import requests

class InfoCollectorClass:

    manufacturer_replacements = [("Inc.", ""),
                                 ("Hewlett-Packard", "HP")
                                 ]

    model_replacements = [("non-vPro", ""),
                          ("HP", ""),
                          ("Pavilion", ""),
                          ("Notebook", ""),
                          ("PC", ""),
                          ("Latitude", ""),
                          ("EasyNote", ""),
                          ("LIFEBOOK", ""),
                          ("ProBook", "")]

    cpu_replacements = [("@", ""),
                        ("Intel(R)", ""),
                        ("Core(TM)", ""),
                        ("CPU", "")]

    gpu_replacements = [("compatible controller:", ""),
                        ("Core processor Graphics Controller", ""),
                        ("Corporation", ""),
                        ("Advanced Micro Devices", ""),
                        ("Inc.", ""),
                        ("Madison", ""),
                        ("Mobility", ""),
                        ("Radeon", "")]

    def __init__(self):
        self.serial = InfoHolderClass("Serial", self.get_serial())
        self.manufacturer = InfoHolderClass("Manufacturer", self.get_manufacturer("Manufacturer"))
        self.model = InfoHolderClass("Model", self.get_model("Model"))
        self.cpu = InfoHolderClass("CPU", self.get_cpu("CPU"))
        self.ram = InfoHolderClass("RAM", self.get_ram())
        self.gpu = InfoHolderClass("GPU", self.get_gpu("GPU"))
        self.hdd = InfoHolderClass("HDD", self.get_hdd())
        display_dict = self.form_display_dict()
        self.diagonal = InfoHolderClass("Diagonal", display_dict['diagonal'])
        self.resolution = InfoHolderClass("Resolution", display_dict['resolution'])
        self.category = InfoHolderClass("Category", display_dict['category'])
        self.license = InfoHolderClass("License", "")
        self.camera = InfoHolderClass("Camera", "")
        self.cover = InfoHolderClass("Cover", "")
        self.display = InfoHolderClass("Display", "")
        self.bezel = InfoHolderClass("Bezel", "")
        self.keyboard = InfoHolderClass("Keyboard", "")
        self.mouse = InfoHolderClass("Mouse", "")
        self.sound = InfoHolderClass("Sound", "")
        self.cdrom = InfoHolderClass("CD-ROM", "")
        self.battery = InfoHolderClass("Battery", self.get_battery())
        self.hdd_cover = InfoHolderClass("HDD Cover", "")
        self.ram_cover = InfoHolderClass("RAM Cover", "")
        self.other = InfoHolderClass("Other", "")
        self.tester = InfoHolderClass("Tester", "")
        self.bios = InfoHolderClass("BIOS", "bios placeholder")
        hdd_serial1, hdd_serial2, hdd_serial3 = self.get_hdd_serials()
        self.hdd_serial1 = InfoHolderClass('hdd_serial1', hdd_serial1)
        self.hdd_serial2 = InfoHolderClass('hdd_serial2', hdd_serial2)
        self.hdd_serial3 = InfoHolderClass('hdd_serial3', hdd_serial3)
        print(self.hdd_serial1.toString())
        print(self.hdd_serial2.toString())
        print(self.hdd_serial3.toString())
        self.motherboard_serial = InfoHolderClass('motherboard_serial', self.get_motherboard_serial())
        print(self.motherboard_serial.toString())



    def get_serial(self):
        output = subprocess.check_output(["sudo", "lshw"])
        pattern = re.compile(b'\\n.*serial.*\\n')
        splitted_text = re.findall(pattern, output)[0].decode('utf-8').split(' ')
        return splitted_text[splitted_text.index("serial:")+1]

    def get_manufacturer(self, title):
        variable = subprocess.check_output(["sudo", "dmidecode", "-t", "chassis", "|", "grep", "'Manufacturer:'"])
        pattern = re.compile(b'Manufacturer: (.+?)\\n\\t')
        text = re.findall(pattern, variable)[0].decode('utf-8')
        if "samsung" in text.lower():
            return "Samsung"
        if "asus" in text.lower():
            return "ASUS"
        return self.replace_strings(title, text)

    def get_model(self, title):
        variable = subprocess.check_output(["sudo", "dmidecode", "|", "grep", "'Product Name: '"])
        pattern = re.compile(b'Product Name: (.+?)\\n\\t')
        text = re.findall(pattern, variable)[0].decode('utf-8')
        return self.replace_strings(title, text)

    def get_cpu(self, title):
        variable = subprocess.check_output(["lscpu"])
        pattern = re.compile(b'Model name: (.+?)\\n')
        text = re.findall(pattern, variable)[0].decode('utf-8')
        return self.replace_strings(title, text)

    def get_ram(self):
        variable = subprocess.check_output(["sudo", "lshw", "-C", "memory"])
        pattern1 = re.compile(b'size: (.+?)GiB\\n')
        result1 = re.search(pattern1, variable).group(1).decode('utf-8') + "GB"
        pattern2 = re.compile(b'DDR[0-9]+')
        result2 = re.findall(pattern2, variable)[0].decode('utf-8')
        return result1 + " " + result2

    def get_gpu(self, title):
        variable = subprocess.check_output(["lspci"])
        pattern = re.compile(b' VGA (.+)\\n')
        gpus = re.findall(pattern, variable)
        text = ""
        for gpu in gpus:
            gpustring = gpu.decode('utf-8')
            if text != "":
                text += " | "
            if 'Intel' in gpustring:
                text += 'Intel'
            elif 'ATI' in gpustring:
                text += 'ATI'
            elif ('NVIDIA' in gpustring) and ('[' in gpustring) and (']' in gpustring):
                gpu_strings_list = self.replace_strings(title, gpustring).split("[")
                text += "NVIDIA" + gpu_strings_list[len(gpu_strings_list)-1].replace("GeForce", "").replace("]", "")\
                    .replace("NVIDIA", "").strip()
            else:
                text += self.replace_strings(title, gpustring)
        return text

    def form_display_dict(self):
        display_dict = {}
        variable = subprocess.check_output(["xrandr"])
        pattern = re.compile(b'.*connected.*')
        result = re.findall(pattern, variable)[0].decode('utf-8')
        diagonal = self.get_diagonal(result)
        display_dict.update({"diagonal": diagonal})
        resolution = self.get_resolution(result)
        display_dict.update({"resolution": resolution})
        category = self.get_resolution_category(resolution)
        display_dict.update({"category": category})
        return display_dict

    def get_diagonal(self, stat_string):
        patdim = '[0-9]+mm x [0-9]+mm'
        dimstr = re.findall(patdim, stat_string)[0]
        dim_arr = dimstr.replace("mm", "").replace(" ", "").split("x")
        diag = str(
            round(
                math.sqrt(
                    (int(dim_arr[0]) / 25.4) ** 2 + (int(dim_arr[1]) / 25.4) ** 2
                )
                , 1)
        )
        return diag+'"'

    def get_resolution(self, stat_string):
        respat = " [0-9]+x[0-9]+"
        res = re.findall(respat, stat_string)[0]
        return res

    def get_resolution_category(self, res):
        px = int(res.split('x')[1])
        if (px < 720):
            return "N/A"
        elif (px < 1080):
            return "HD"
        elif (px < 1440):
            return "Full HD"
        elif (px < 1536):
            return "Quad HD"
        elif (px < 2160):
            return "2000"
        elif (px < 2540):
            return "2160p/4K UHD"
        elif (px < 3072):
            return "2540p"
        elif (px < 4320):
            return "4000p"
        elif (px >= 4320):
            return "4320p/8K UHD"

    def get_hdd(self):
        variable = subprocess.check_output(["sudo", "lshw", "-class", "disk", "-class", "storage"])
        pattern = re.compile(b'[0-9]+GB')
        result = re.findall(pattern, variable)
        if result:
            text = ""
            for member in result:
                if text != "":
                    text = " - "
                text += member.decode('utf-8')
            return text
        return "0"

    def get_hdd_serials(self):
        hdd_serial1 = 'N/A'
        hdd_serial2 = 'N/A'
        hdd_serial3 = 'N/A'
        output = subprocess.check_output(['lsblk', '-o', 'NAME,SERIAL'])
        pattern = re.compile(b'.*sd. .*')
        result = re.findall(pattern, output)
        if len(result) > 2:
            hdd_serial3 = re.sub(' +', ' ', result[2].decode('utf-8').strip()).split(' ')[1]
        if len(result) > 1:
            hdd_serial2 = re.sub(' +', ' ', result[1].decode('utf-8').strip()).split(' ')[1]
        if len(result) > 0:
            hdd_serial1 = re.sub(' +', ' ', result[0].decode('utf-8').strip()).split(' ')[1]
        return hdd_serial1, hdd_serial2, hdd_serial3

    def get_motherboard_serial(self):
        output = subprocess.check_output(['sudo', 'dmidecode', '-t', '2'])
        pattern = re.compile(b'Serial.*')
        result = re.findall(pattern, output)
        return result[0].decode('utf-8').split(':')[1].strip()

    def get_battery(self):
        if "hp" in self.manufacturer.get_value().lower():
            return "HP battery info N/A"
        output = subprocess.check_output(["upower", "-e"])
        battery_pat = re.compile(b'(?:^|\\n).*battery.*(?:$|\\n)')
        battery_try = re.findall(battery_pat, output)
        if battery_try:
            battery = battery_try[0].decode('utf-8').replace("\n", "")
            output2 = subprocess.check_output(["upower", "-i", battery])
            capacity_pat = re.compile(b'([0-9]*[\.\,]?[0-9]*?%)')
            capacity_group = re.findall(capacity_pat, output2)
            health = float(capacity_group[1].decode('utf-8').replace("%", "").replace(",", "."))
            if health < 10:
                return "Does not hold charge"
            elif health < 40:
                return "~30 min."
            elif health < 64:
                return "~40 min."
            elif health <= 100:
                return "~1 h."
            else:
                return "Value does not conform to provided rules: " + str(
                    100 - round(float(capacity_group[1].decode('utf-8').replace("%", "").replace(",", ".")), 2)
                )+"%"
        return "N/A"

    def replace_strings(self, title, string):
        unwanted_strings = []
        if title == "Manufacturer":
            unwanted_strings = self.manufacturer_replacements
        elif title == "Model":
            unwanted_strings = self.model_replacements
        elif title == "CPU":
            unwanted_strings = self.cpu_replacements
        elif title == "GPU":
            unwanted_strings = self.gpu_replacements
        else:
            raise Exception("Invalid title passed for string replacement")
        for replacement in unwanted_strings:
            string = string.replace(replacement[0], replacement[1])
        return re.sub(' +', ' ', string.strip())

    def send_dict(self, dict):
        json_data = json.dumps(dict)
        r = requests.post('http://192.168.8.132:8000/data/', json_data)
        print("Status code: "+str(r.status_code))
        print("Reason: "+str(r.reason))
        print("Content: "+str(r.content))
        return r

    def get_data(self):
        return (
            self.serial,
            self.manufacturer,
            self.model,
            self.cpu,
            self.ram,
            self.gpu,
            self.hdd,
            self.diagonal,
            self.resolution,
            self.category,
            self.license,
            self.camera,
            self.cover,
            self.display,
            self.bezel,
            self.keyboard,
            self.mouse,
            self.sound,
            self.cdrom,
            self.battery,
            self.hdd_cover,
            self.ram_cover,
            self.tester,
            self.other,
        )

    def toString(self):
        return "this method currently is empty"