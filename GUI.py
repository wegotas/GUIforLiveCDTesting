from tkinter import *
from InfoCollectorClass import *
import graphics as gx
from screeninfo import get_monitors
import time
import os


class App:
    textbox_dict = {}
    finishing_data_dict = {}
    license_value = None
    camera_value = None
    tester_value = None

    def __init__(self, master):
        upperframe = Frame(master)
        self.add_menubar(upperframe)
        self.add_labels(upperframe)
        upperframe.pack()

    def add_labels(self, upperframe):
        data = infocollector.get_data()
        self.form_specs_frame(upperframe)
        self.form_screen_frame(upperframe)
        self.form_rest_frame(upperframe)
        self.form_independent_fields(upperframe)


    def form_specs_frame(self, frame):
        label = Label(frame, text="Specs: ", font="bold").grid(column=0, row=0, pady=(6, 0), sticky="s")
        middleframe = Frame(frame, borderwidth=1, relief=GROOVE)
        middleframe.grid(column=0, row=1, sticky="n", padx=6, pady=(0, 6), rowspan=3)
        self.form_GUI_object(middleframe, infocollector.serial, 0, 0)
        self.form_GUI_object(middleframe, infocollector.manufacturer, 0, 2)
        self.form_GUI_object(middleframe, infocollector.model, 0, 4)
        self.form_GUI_object(middleframe, infocollector.camera, 0, 6)
        self.form_GUI_object(middleframe, infocollector.cpu, 1, 0)
        self.form_GUI_object(middleframe, infocollector.ram, 1, 2)
        self.form_GUI_object(middleframe, infocollector.hdd, 1, 4)
        self.form_GUI_object(middleframe, infocollector.gpu, 1, 6)

    def form_screen_frame(self, frame):
        label = Label(frame, text="Screen: ", font="bold").grid(column=1, row=0, pady=(6, 0), sticky="s")
        middleframe = Frame(frame, borderwidth=1, relief=GROOVE)
        middleframe.grid(column=1, row=1, sticky="n", padx=6, pady=(0, 6))
        self.form_GUI_object(middleframe, infocollector.diagonal, 0, 0)
        self.form_GUI_object(middleframe, infocollector.resolution, 0, 2)
        self.form_GUI_object(middleframe, infocollector.category, 0, 4)

    def form_rest_frame(self, frame):
        label = Label(frame, text="Rest: ", font="bold").grid(column=0, row=4, pady=(6, 0), sticky="s", columnspan=2)
        middleframe = Frame(frame, borderwidth=1, relief=GROOVE)
        middleframe.grid(column=0, row=5, sticky="n", padx=6, pady=(0, 6), columnspan=2)
        self.form_GUI_object(middleframe, infocollector.cover, 0, 0, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.display, 0, 2, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.bezel, 0, 4, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.keyboard, 0, 6, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.mouse, 0, 8, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.sound, 1, 0, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.cdrom, 1, 2, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.battery, 1, 4, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.hdd_cover, 1, 6, textbox_width=40)
        self.form_GUI_object(middleframe, infocollector.ram_cover, 1, 8, textbox_width=40)

    def form_independent_fields(self, frame):
        self.form_GUI_object(frame, infocollector.license, column=1, row=2)
        label = Label(frame, text=infocollector.bios.get_title()+": ") \
            .grid(column=0, row=6, columnspan=2, sticky="s", padx=(0, 60), pady=(6, 0))
        label2 = Label(frame, text=infocollector.bios.get_value(), fg="cyan") \
            .grid(column=0, row=7, columnspan=2, sticky="s", padx=6)
        self.form_GUI_object(frame, infocollector.other, column=0, row=8, textbox_width=30)
        self.textbox_dict[infocollector.bios.get_title()] = infocollector.bios.get_value()

    def form_GUI_object(self, frame, infoholder, column, row, textbox_width=24):
        label = Label(frame, text=infoholder.get_title() + ": ") \
            .grid(column=column, row=row, sticky="sw", padx=6)
        if (infoholder.get_title() == "License"):
            inner_frame = Frame(frame)
            inner_frame.grid(column=column, row=row + 1, sticky="nw")
            license_var = StringVar()
            checkbox1 = Radiobutton(inner_frame, text='W7', variable=license_var, value="W7", command=lambda: self.set_license("W7")).grid(column=0, row=0)
            checkbox2 = Radiobutton(inner_frame, text='W8', variable=license_var, value="W8", command=lambda: self.set_license("W8")).grid(column=0, row=1)
            checkbox3 = Radiobutton(inner_frame, text='W10', variable=license_var, value="W10", command=lambda: self.set_license("W10")).grid(column=1, row=0)
            checkbox4 = Radiobutton(inner_frame, text='N/A', variable=license_var, value="N/A", command=lambda: self.set_license("N/A")).grid(column=1, row=1)
        elif (infoholder.get_title() == "Camera"):
            inner_frame = Frame(frame)
            inner_frame.grid(column=column, row=row + 1, sticky="nw")
            camera_var = StringVar()
            checkbox10 = Radiobutton(inner_frame, text='Yes', variable=camera_var, value="Yes", command=lambda: self.set_camera("Yes")).pack(side=LEFT)
            checkbox11 = Radiobutton(inner_frame, text='No', variable=camera_var, value="No", command=lambda: self.set_camera("No")).pack(side=LEFT)
        elif (infoholder.get_title() == "Other"):
            text = Text(frame, height=4, width=textbox_width*3)
            text.insert(END, infoholder.get_value())
            text.grid(column=column, row=row + 1, padx=6, pady=(0, 6), sticky="n", columnspan=2)
            self.textbox_dict[infoholder.get_title()] = text
        else:
            text = Text(frame, height=1, width=textbox_width)
            text.insert(END, infoholder.get_value())
            text.grid(column=column, row=row + 1, padx=6, pady=(0, 6), sticky="n")
            self.textbox_dict[infoholder.get_title()] = text

    def set_license(self, value):
        self.license_value = value

    def set_camera(self, value):
        self.camera_value = value

    def get_grid_coordinate(self, index):
        rowlimit=10
        return (math.floor(index/rowlimit), (index%rowlimit)*2)

    def clear_frame_grid(self, frame):
        for label in frame.grid_slaves():
            if int(label.grid_info()["row"]) > 1 and int(label.grid_info()["column"]) > 5:
                label.grid_forget()

    def cheese_camera(self):
        subprocess.Popen("cheese")

    def display_inspection(self):
        subprocess.check_output(
            ["dconf", "write", "/org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode", "1"])
        time.sleep(1)
        monitor = get_monitors()[0]

        window = gx.GraphWin("Window Test", monitor.width, monitor.height)
        window.setBackground(gx.color_rgb(0, 0, 0))

        window.getMouse()
        window.setBackground(gx.color_rgb(255, 0, 0))

        window.getMouse()
        window.setBackground(gx.color_rgb(0, 0, 255))

        window.getMouse()
        window.setBackground(gx.color_rgb(255, 255, 255))

        window.getMouse()
        window.close()
        subprocess.check_output(
            ["dconf", "write", "/org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode", "0"])

    def sound_inspection(self):
        subprocess.Popen(["unity-control-center", "sound"])

    def sound_interface_control(self):
        subprocess.Popen(["pavucontrol"])

    def stui(self):
        os.system("gnome-terminal -e 'bash -c \"s-tui; exec bash\"'")

    def glmark2(self):
        subprocess.Popen(["glmark2"])

    def lshwgtk(self):
        subprocess.Popen(["sudo", "lshw-gtk"])

    def inex(self):
        subprocess.Popen(["i-nex"])

    def kinfocenter(self):
        subprocess.Popen(["kinfocenter"])

    def hardinfo(self):
        subprocess.Popen(["hardinfo"])

    def sysinfo(self):
        subprocess.Popen(["sysinfo"])

    def check_data_filling(self):
        warning_text = ""
        if self.license_value == None:
            warning_text += "License has not been selected \r\n"
        if self.camera_value == None:
            warning_text += "Camera option has not been selected \r\n"
        for key, textbox in self.textbox_dict.items():
            if key == "BIOS":
                if textbox == "":
                    warning_text += "BIOS label is empty \r\n"
            elif key == "Other":
                continue
            else:
                text = textbox.get("1.0", "end-1c").rstrip()
                if text == "":
                    warning_text += key + " has not been filled in \r\n"
        return warning_text

    def last_step(self):
        warning = self.check_data_filling()
        if warning != "":
            self.warning_popup(warning)
        else:
            self.employee_id()

    def warning_popup(self, text):
        toplevel = Toplevel()
        scrollbar = Scrollbar(toplevel)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = Label(toplevel, text=text, fg="red")
        label.pack()


    def employee_id(self):
        toplevel = Toplevel()
        label = Label(toplevel, text="Enter your identity:", fg="blue")
        label.pack()
        text = Text(toplevel, height=1, width=20)
        text.pack()
        button = Button(toplevel, text="Send data", command=lambda: self.set_tester(text.get("1.0", "end-1c").rstrip(), toplevel))
        button.pack()

    def set_tester(self, tester, popup):
        popup.destroy()
        if tester == "":
            self.warning_popup("No employee tab no. entered")
        else:
            self.tester_value = tester
            self.form_finishing_data_dict()

    def form_finishing_data_dict(self):
        for key, value in self.textbox_dict.items():
            if key == "BIOS":
                self.finishing_data_dict[key] = value
            else:
                self.finishing_data_dict[key] = value.get("1.0", "end-1c").rstrip()
        self.finishing_data_dict["License"] = self.license_value
        self.finishing_data_dict["Camera"] = self.camera_value
        self.finishing_data_dict["Tester"] = self.tester_value
        request = infocollector.send_dict(self.finishing_data_dict)
        if request.status_code == 200:
            self.succesful(request.content)
        else:
            self.warning_popup(request.content)

    def succesful(self,text):
        toplevel = Toplevel()
        label = Label(toplevel, text=text, fg="green", font="bold")
        label.pack(side=TOP)

    def print_gui_objects(self):
        index = 0
        for key, textbox in self.textbox_dict.items():
            if key == "BIOS":
                print(str(index) + " - " + key + ": " + textbox)
            else:
                print(str(index)+" - "+key + ": "+textbox.get("1.0", "end-1c").rstrip())
            index += 1
        print(str(index)+" - License: "+str(self.license_value))
        index += 1
        print(str(index)+" - Camera: "+str(self.camera_value))
        index += 1
        print(str(index) + " - Tester: " + str(self.tester_value))

    def add_menubar(self, frame):
        menubar = Menu(frame)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sound Interfaces", command=self.sound_interface_control)
        file_menu.add_command(label="Debug option", command=self.print_gui_objects)
        file_menu.add_command(label="[Placeholder]")
        menubar.add_cascade(label="File", menu=file_menu)

        testing_menu = Menu(menubar, tearoff=0)
        testing_menu.add_command(label="Camera", command=self.cheese_camera)
        testing_menu.add_command(label="Display", command=self.display_inspection)
        testing_menu.add_command(label="Sound", command=self.sound_inspection)
        testing_menu.add_command(label="Temperature monitor", command=self.stui)
        testing_menu.add_command(label="glmark2", command=self.glmark2)
        menubar.add_cascade(label="Tests", menu=testing_menu)

        program_menu = Menu(menubar, tearoff=0)
        program_menu.add_command(label="lshw-gtk", command=self.lshwgtk)
        program_menu.add_command(label="i-nex", command=self.inex)
        program_menu.add_command(label="kinfocenter", command=self.kinfocenter)
        program_menu.add_command(label="hardinfo", command=self.hardinfo)
        program_menu.add_command(label="sysinfo", command=self.sysinfo)
        menubar.add_cascade(label="Programs", menu=program_menu)

        menubar.add_command(label="Last step", command=self.last_step)

        root.config(menu=menubar)


infocollector = InfoCollectorClass()
root = Tk()

app = App(root)

root.mainloop()
root.destroy()