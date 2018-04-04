import subprocess
import re
import math
import os
from graphics import *
from screeninfo import get_monitors
import time

# variable = subprocess.check_output(["sudo", "dmidecode", "-t", "chassis", "|", "grep", "'Serial Number:'"])
# pattern = re.compile(b'Serial Number: (.+?)\\n\\tAsset')
# serial = re.search(pattern, variable).group(1).decode('utf-8')
# print(serial)

#variable = subprocess.check_output(["ls", "-l", "/tmp"])
#variable = subprocess.check_output(["ls", '-l'])


# variable = subprocess.check_output(["sudo", "dmidecode", "-t", "chassis", "|", "grep", "'Manufacturer:'"])
# print(variable)
# pattern = re.compile(b'Manufacturer: (.+?)\\n\\t')
# endresult = re.search(pattern, variable).group(1).decode('utf-8')
# print(endresult)

# 'sudo dmidecode | grep "Product Name: " | head -1'

# variable = subprocess.check_output(["sudo", "dmidecode", "|", "grep", "'Product Name: '"])
# print(variable)
# pattern = re.compile(b'Product Name: (.+?)\\n\\t')
# endresult = re.search(pattern, variable).group(1).decode('utf-8')
# print(endresult)

# variable = subprocess.check_output(["lscpu"])
# print(variable)
# pattern = re.compile(b'Model name: (.+?)\\n')
# endresult = re.search(pattern, variable).group(1).decode('utf-8')
# print(endresult)

# variable = subprocess.check_output(["sudo", "lshw", "-C", "memory"])
# print(variable)
# pattern1 = re.compile(b'size: (.+?)GiB\\n')
# result1 = re.search(pattern1, variable).group(1).decode('utf-8')+"GB"
# print(result1)
# pattern2 = re.compile(b'DDR[0-9]+')
# result2 = re.findall(pattern2, variable)[0].decode('utf-8')
# print(result2)
# endresult = result1 + " " + result2
#print(endresult)

# variable = subprocess.check_output(["lspci"])
# print(variable)
# pattern = re.compile(b' VGA (.+?)\(')
# endresult = re.search(pattern, variable).group(1).decode('utf-8').replace("compatible controller: ", "").replace(" Core processor Graphics Controller", "")
# print(endresult)
"""
variable = subprocess.check_output(["xrandr"])
# print(variable)
pattern = re.compile(b'.*connected.*')
result = re.search(pattern, variable).group(0).decode('utf-8')
print(result)

patdim = '[0-9]+mm x [0-9]+mm'
dimstr = re.search(patdim, result).group(0)
print("Dimmension string: " + dimstr)
dim_arr = dimstr.replace("mm", "").replace(" ", "").split("x")
print("Dimmension array: " + str(dim_arr))
diag = str(
    round(
        math.sqrt(
            (int(dim_arr[0])/25.4)**2 + (int(dim_arr[1])/25.4)**2
        )
        , 1)
)
print("diagonal: " + diag)


respat = " [0-9]+x[0-9]+"
res = re.search(respat, result).group(0)
print("res: " + res)

px = int(res.split('x')[1])
print(px)

cat = None

if (px < 720):
    cat = "N/A"
elif (px < 1080):
    cat = "HD"
elif (px < 1440):
    cat = "Full HD"
elif (px < 1536):
    cat = "Quad HD"
elif (px < 2160):
    cat = "2000"
elif (px < 2540):
    cat = "2160p/4K UHD"
elif (px < 3072):
    cat = "2540p"
elif (px < 4320):
    cat = "4000p"
elif (px >= 4320):
    cat = "4320p/8K UHD"

print("Resolution category: " + cat)
"""
# variable = subprocess.check_output(["sudo", "lshw", "-class", "disk", "-class", "storage"])
# print(variable)
# pattern = re.compile(b'[0-9]+GB')
# result = re.search(pattern, variable).group(0).decode('utf-8')
# print(result)

# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
# subprocess.check_output([])
"""
"dconf write /org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode 1"
subprocess.check_output(["dconf", "write", "/org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode", "1"])
time.sleep(1)
monitor = get_monitors()[0]

window = GraphWin("Window Test", monitor.width, monitor.height)
window.setBackground(color_rgb(0, 0, 0))

window.getMouse()
window.setBackground(color_rgb(255, 0, 0))

window.getMouse()
window.setBackground(color_rgb(0, 0, 255))

window.getMouse()
window.setBackground(color_rgb(255, 255, 255))

window.getMouse()
window.close()
subprocess.check_output(["dconf", "write", "/org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode", "0"])
"""
"""
# subprocess.call(["unity-control-center", "sound"])
output = subprocess.check_output(["upower", "-e"])
# battery_pat = re.compile(b'(?:^|\n)battery(?:$|\n)')
battery_pat = re.compile(b'(?:^|\\n).*battery.*(?:$|\\n)')
battery = re.search(battery_pat, output).group(0).decode('utf-8').replace("\n", "")
print(battery)
output2 = subprocess.check_output(["upower", "-i", battery])
print(output2)
capacity_pat = battery_pat = re.compile(b'([0-9]*[,][0-9]*[%])')
capacity = re.search(capacity_pat, output2).group(0).decode('utf-8').replace("\n", "")
print(capacity)
wear_out = 100 - float(capacity.replace("%", "").replace(",", "."))
print(wear_out)
"""
"""
output = subprocess.check_output(["sudo", "lshw"])
print(output)
pattern = re.compile(b'\\n.*serial.*\\n')
result = re.search(pattern, output).group(0).decode('utf-8').replace("serial:", "").replace("\n", "").replace(" ", "")
print(result)
"""
"""
output = subprocess.check_output(['lsblk', '-o', 'NAME,SERIAL'])
# print(output)
pattern = re.compile(b'\\nsd.*\\n')
result = re.findall(pattern, output)
print(result)
print("Results length is: " + str(len(result)))

hdd_serial1 = 'N/A'
hdd_serial2 = 'N/A'
hdd_serial3 = 'N/A'
if len(result) > 2:
    hdd_serial3 = re.sub(' +', ' ', result[2].decode('utf-8').strip()).split(' ')[1]
if len(result) > 1:
    hdd_serial2 = re.sub(' +', ' ', result[1].decode('utf-8').strip()).split(' ')[1]
if len(result) > 0:
    hdd_serial3 = re.sub(' +', ' ', result[0].decode('utf-8').strip()).split(' ')[1]

# print(re.sub(' +', ' ', result[0].decode('utf-8').strip()).split(' ')[1])
# print(re.sub(' +', ' ', result[1].decode('utf-8').strip()).split(' ')[1])
# print(re.sub(' +', ' ', result[2].decode('utf-8').strip()).split(' ')[1])
"""
"""
output = subprocess.check_output(['sudo', 'dmidecode', '-t', '2'])
print(output)
pattern = re.compile(b'Serial.*')
result = re.findall(pattern, output)
print(result)
print(result[0].decode('utf-8').split(':')[1].strip())
"""
"""
def process_ramstring(ramstring):
    if b'empty' in ramstring.lower():
        return 'N/A'
    else:
        return ramstring.decode('utf-8').split(':')[1].strip()

ram_serial_list = []

output = subprocess.check_output(['sudo', 'lshw', '-C', 'memory'])
print(output)
pattern = re.compile(b'serial:.*')
result = re.findall(pattern, output)
print(result)
for i in range(6):
    print(i)
    if i < len(result):
        ram_serial_list.append(process_ramstring(result[i]))
    else:
        ram_serial_list.append('N/A')

print(ram_serial_list)
"""

bat1_wear = 'N/A'
bat2_wear = 'N/A'
bat1_expected_time = 'N/A'
bat2_expected_time = 'N/A'
bat1_serial = 'N/A'
bat2_serial = 'N/A'

def process_battery(battery):
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
    serial = serial_string[0].decode('utf-8').split(':')[1].strip()
    return wear, expected_time, serial


output = subprocess.check_output(['upower', '-e'])
pattern = re.compile(b'.*batt.*')
result = re.findall(pattern, output)
if len(result) > 0:
    bat1_wear, bat1_expected_time, bat1_serial = process_battery(result[0])
print(str(bat1_wear) +' '+ str(bat1_expected_time) +' '+ str(bat1_serial))
if len(result) > 1:
    bat2_wear, bat2_expected_time, bat2_serial = process_battery(result[1])
print(str(bat2_wear) +' '+ str(bat2_expected_time) +' '+ str(bat2_serial))