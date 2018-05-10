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
                          ("ProBook", ""),
                          ("Aspire", ""),
                          ("ThinkPad", "")]

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
        # Laptop's server IP
        self.domain = "http://192.168.8.132:8000/"

        # Server computer's IP
        # self.domain = "http://192.168.2.1:8000/"
        self.message = ""
        self.is_connectable = False
        self.provide_message = False
        self.succesful_connection = False
        self.aux_data = self.get_aux_data()

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

        cover, display, bezel, keyboard, mouse, sound, cdrom, hdd_cover, ram_cover, other, license, camera = self.get_data_from_server()
        self.license = InfoHolderClass("License", license)
        self.camera = InfoHolderClass("Camera", camera)
        self.cover = InfoHolderClass("Cover", cover)
        self.display = InfoHolderClass("Display", display)
        self.bezel = InfoHolderClass("Bezel", bezel)
        self.keyboard = InfoHolderClass("Keyboard", keyboard)
        self.mouse = InfoHolderClass("Mouse", mouse)
        self.sound = InfoHolderClass("Sound", sound)
        self.cdrom = InfoHolderClass("CD-ROM", cdrom)
        self.hdd_cover = InfoHolderClass("HDD Cover", hdd_cover)
        self.ram_cover = InfoHolderClass("RAM Cover", ram_cover)
        self.other = InfoHolderClass("Other", other)

        self.tester = InfoHolderClass("Tester", "")
        self.comouter_type = InfoHolderClass("Computer type", "")
        self.bios = InfoHolderClass("BIOS", "N/A")
        hdd_serial1, hdd_serial2, hdd_serial3 = self.get_hdd_serials()
        self.hdd_serial1 = InfoHolderClass('hdd_serial1', hdd_serial1)
        self.hdd_serial2 = InfoHolderClass('hdd_serial2', hdd_serial2)
        self.hdd_serial3 = InfoHolderClass('hdd_serial3', hdd_serial3)
        self.motherboard_serial = InfoHolderClass('motherboard_serial', self.get_motherboard_serial())
        ram_serial_list = self.get_ram_serials()
        self.ram_serial1 = InfoHolderClass('ram_serial1', ram_serial_list[0])
        self.ram_serial2 = InfoHolderClass('ram_serial2', ram_serial_list[1])
        self.ram_serial3 = InfoHolderClass('ram_serial3', ram_serial_list[2])
        self.ram_serial4 = InfoHolderClass('ram_serial4', ram_serial_list[3])
        self.ram_serial5 = InfoHolderClass('ram_serial5', ram_serial_list[4])
        self.ram_serial6 = InfoHolderClass('ram_serial6', ram_serial_list[5])
        bt1_wear, bt1_expected_time, bt1_serial, bt2_wear, bt2_expected_time, bt2_serial = self.get_batteries_info()
        self.bat1_wear = InfoHolderClass('Bat1 wear', str(bt1_wear))
        self.bat1_expected_time = InfoHolderClass('Bat1 expected time', bt1_expected_time)
        self.bat1_serial = InfoHolderClass('Bat1 serial', bt1_serial)
        self.bat2_wear = InfoHolderClass('Bat2 wear', str(bt2_wear))
        self.bat2_expected_time = InfoHolderClass('Bat2 expected time', bt2_expected_time)
        self.bat2_serial = InfoHolderClass('Bat2 serial', bt2_serial)

    def get_aux_data(self):
        try:
            # response = requests.get('http://192.168.8.132:8000/if/aux_data/')
            # response = requests.get('http://192.168.2.1:8000/if/aux_data/')
            response = requests.get(self.domain + 'if/aux_data/')
            return response.json()
        except Exception as e:
            self.message = "Failed to fetch auxiliary data\n"
            self.provide_message = True
            self.is_connectable = False
            self.succesful_connection = False
            return None

    def get_data_from_server(self):
        request_dict = dict()
        request_dict[self.serial.get_title()] = self.serial.get_value()
        try:
            json_dump = json.dumps(request_dict)
            # response = requests.get('http://192.168.8.132:8000/if/data/', json_dump)
            # response = requests.get('http://192.168.2.1:8000/if/data/', json_dump)
            response = requests.get(self.domain + 'if/data/', json_dump)
            print("status_code is " + str(response.status_code))
            if response.status_code == 200:
                json_data = response.json()
                self.message = "Existing record has been found and data filled in form"
                self.is_connectable = True
                self.provide_message = True
                self.succesful_connection = True
                return json_data["Cover"], json_data["Display"], json_data["Bezel"], json_data["Keyboard"], \
                       json_data["Mouse"], json_data["Sound"], json_data["CD-ROM"], json_data["HDD Cover"], \
                       json_data["RAM Cover"], json_data["Other"], json_data["License"], json_data["Camera"]
            else:
                self.is_connectable = True
                if response.content.decode('utf-8') == "No such computer":
                    self.is_connectable = True
                    self.succesful_connection = True
                    self.provide_message = False
                    return "", "", "", "", "", "", "", "", "", "", "", ""
                else:
                    self.is_connectable = True
                    self.succesful_connection = False
                    self.provide_message = True
                    self.message = "Failure on the server side:\n" + response.content.decode('utf-8')
                    return "", "", "", "", "", "", "", "", "", "", "", ""
        except Exception as e:
            self.is_connectable = False
            self.succesful_connection = False
            self.provide_message = True
            self.message = "Failed to connect to the server.\n" \
                           "Check if server is running and all cables are connected\n" \
                           "Or error on the server side.\nError message:\n\n"+str(e)
            return "", "", "", "", "", "", "", "", "", "", "", ""

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
        text = "N/A"
        if self.manufacturer.get_value().upper() == "LENOVO":
            variable = subprocess.check_output(["sudo", "dmidecode", "|", "grep", "Version"])
            pattern = re.compile(b'Version: (.+?)\\n\\t')
            text = re.findall(pattern, variable)[1].decode("utf-8")
        else:
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

    def get_ram_serials(self):
        ram_serial_list = []
        output = subprocess.check_output(['sudo', 'lshw', '-C', 'memory'])
        pattern = re.compile(b'serial:.*')
        result = re.findall(pattern, output)
        for i in range(6):
            if i < len(result):
                ram_serial_list.append(self.process_serial_ramstring(result[i]))
            else:
                ram_serial_list.append('N/A')
        return ram_serial_list

    def process_serial_ramstring(self, ramstring):
        if b'empty' in ramstring.lower():
            return 'N/A'
        else:
            return ramstring.decode('utf-8').split(':')[1].strip()

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
            elif "RADEON" in gpustring.upper():
                gpuPattern = re.compile('[0-9]+[A-Za-z]?')
                lowerGPU = re.findall(gpuPattern, gpustring)[0]
                text += "Radeon " + lowerGPU
            elif 'ATI' in gpustring:
                text += 'ATI'
            elif ('NVIDIA' in gpustring) and ('[' in gpustring) and (']' in gpustring):
                gpu_strings_list = self.replace_strings(title, gpustring).split("[")
                text += "NVIDIA " + gpu_strings_list[len(gpu_strings_list)-1].replace("GeForce", "").replace("]", "")\
                    .replace("NVIDIA", "").strip()
            else:
                text += self.replace_strings(title, gpustring)
        return text

    def form_display_dict(self):
        display_dict = {}
        variable = subprocess.check_output(["xrandr"])
        pattern = re.compile(b'.* connected.*')
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

    def get_batteries_info(self):
        bat1_wear = 'N/A'
        bat2_wear = 'N/A'
        bat1_expected_time = 'N/A'
        bat2_expected_time = 'N/A'
        bat1_serial = 'N/A'
        bat2_serial = 'N/A'
        output = subprocess.check_output(['upower', '-e'])
        pattern = re.compile(b'.*batt.*')
        result = re.findall(pattern, output)
        if len(result) > 0:
            bat1_wear, bat1_expected_time, bat1_serial = self.process_battery(result[0])
        if len(result) > 1:
            bat2_wear, bat2_expected_time, bat2_serial = self.process_battery(result[1])
        return bat1_wear, bat1_expected_time, bat1_serial, bat2_wear, bat2_expected_time, bat2_serial

    def process_battery(self, battery):
        output = subprocess.check_output(['upower', '-i', battery])
        capacity_pat = re.compile(b'([0-9]*[\.\,]?[0-9]*?%)')
        capacity = re.findall(capacity_pat, output)[1].decode('utf-8').replace("\n", "")
        wear = 100 - float(capacity.replace("%", "").replace(",", "."))
        expected_time = 'N/A'
        if wear < 36:
            expected_time = "~1h."
        elif wear < 60:
            expected_time = '~40min.'
        elif wear < 90:
            expected_time = '~30min.'
        elif wear <= 100:
            expected_time = "Does not hold charge"
        else:
            expected_time = "Wear out is wrong. Can't determine expected time"
        serial_pat = re.compile(b'.*serial.*')
        serial_string = re.findall(serial_pat, output)
        serial = "N/A"
        if len(serial_string) > 0:
            serial = serial_string[0].decode('utf-8').split(':')[1].strip()
        if "hp" in self.manufacturer.get_value().lower():
            wear = "HP battery wear is unreliable"
            expected_time = "HP expected battery operation time is unreliable"
        return wear, expected_time, serial

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
        dict[self.motherboard_serial.get_title()] = self.motherboard_serial.get_value()
        dict[self.hdd_serial1.get_title()] = self.hdd_serial1.get_value()
        dict[self.hdd_serial2.get_title()] = self.hdd_serial2.get_value()
        dict[self.hdd_serial3.get_title()] = self.hdd_serial3.get_value()
        dict[self.ram_serial1.get_title()] = self.ram_serial1.get_value()
        dict[self.ram_serial2.get_title()] = self.ram_serial2.get_value()
        dict[self.ram_serial3.get_title()] = self.ram_serial3.get_value()
        dict[self.ram_serial4.get_title()] = self.ram_serial4.get_value()
        dict[self.ram_serial5.get_title()] = self.ram_serial5.get_value()
        dict[self.ram_serial6.get_title()] = self.ram_serial6.get_value()
        dict[self.bat1_wear.get_title()] = self.bat1_wear.get_value()
        dict[self.bat1_expected_time.get_title()] = self.bat1_expected_time.get_value()
        dict[self.bat1_serial.get_title()] = self.bat1_serial.get_value()
        dict[self.bat2_wear.get_title()] = self.bat2_wear.get_value()
        dict[self.bat2_expected_time.get_title()] = self.bat2_expected_time.get_value()
        dict[self.bat2_serial.get_title()] = self.bat2_serial.get_value()
        json_data = json.dumps(dict)
        print(json_data)
        # r = requests.post('http://192.168.8.132:8000/if/data/', json_data)
        # r = requests.post('http://192.168.2.1:8000/if/data/', json_data)
        r = requests.post(self.domain + 'if/data/', json_data)
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
            self.bat1_expected_time,
            self.hdd_cover,
            self.ram_cover,
            self.tester,
            self.other,
        )

    def toString(self):
        return "this method currently is empty"