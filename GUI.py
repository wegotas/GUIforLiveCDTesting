from tkinter import *
from InfoCollectorClass import *
import graphics as gx
from screeninfo import get_monitors
import time
import os


class App:
    textbox_dict = {}
    finishing_data_dict = {}
    tester_value = None
    computer_type = None


    def __init__(self, master):
        self.camera_var = StringVar(master)
        self.license_var = StringVar(master)

        self.tester_var = StringVar()
        self.type_var = StringVar()
        self.category_var = StringVar()

        self.camera_var.set(infocollector.camera.get_value())
        self.license_var.set(infocollector.license.get_value())
        upperframe = Frame(master)
        self.add_menubar(upperframe)
        self.add_labels(upperframe)
        upperframe.pack()
        if infocollector.message != "":
            self.warning_popup(infocollector.message)

    def add_labels(self, upperframe):
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
        self.form_GUI_object(middleframe, infocollector.bat1_expected_time, 1, 4, textbox_width=40)
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
            checkbox1 = Radiobutton(inner_frame, text="W7", variable=self.license_var, value="W7").grid(column=0, row=0)
            checkbox2 = Radiobutton(inner_frame, text="W8", variable=self.license_var, value="W8").grid(column=0, row=1)
            checkbox3 = Radiobutton(inner_frame, text="W10", variable=self.license_var, value="W10").grid(column=1, row=0)
            checkbox4 = Radiobutton(inner_frame, text="N/A", variable=self.license_var, value="N/A").grid(column=1, row=1)
        elif (infoholder.get_title() == "Camera"):
            inner_frame = Frame(frame)
            inner_frame.grid(column=column, row=row + 1, sticky="nw")
            checkbox10 = Radiobutton(inner_frame, text='Yes', variable=self.camera_var, value="Yes").pack(side=LEFT)
            checkbox11 = Radiobutton(inner_frame, text='No', variable=self.camera_var, value="No").pack(side=LEFT)
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
        #if self.license_value == None:
        #    warning_text += "License has not been selected \r\n"
        # if self.camera_value == None:
        #     warning_text += "Camera option has not been selected \r\n"
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
        scrollbar = Scrollbar(toplevel, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = Label(toplevel, text=text, fg="red")
        label.pack()


    def employee_id(self):
        toplevel = Toplevel()
        label = Label(toplevel, text="Enter your identity:", fg="blue")
        label.pack()
        tester_menu = OptionMenu(toplevel, self.tester_var, *infocollector.aux_data['tes_dict'].values())
        tester_menu.pack()

        label = Label(toplevel, text="Choose computer type:", fg="blue")
        label.pack()
        type_menu = OptionMenu(toplevel, self.type_var, *infocollector.aux_data['typ_dict'].values())
        type_menu.pack()

        label = Label(toplevel, text="Choose category to assign to:", fg="blue")
        label.pack()
        category_menu = OptionMenu(toplevel, self.category_var, *infocollector.aux_data['cat_dict'].values())
        category_menu.pack()

        button = Button(toplevel, text="Send data", command=lambda: self.set_tester(toplevel))
        button.pack()

    def set_tester(self, popup):
        popup.destroy()
        text = ""
        if self.tester_var.get() == "":
            text += "Tester was not selected\n"
        if self.type_var.get() == "":
            text += "Computer type was not selected\n"
        if self.category_var.get() == "":
            text += "Computer category to assign to was not selected"

        if text != "":
            self.warning_popup(text)
        else:
            self.form_finishing_data_dict()

    def form_finishing_data_dict(self):
        for key, value in self.textbox_dict.items():
            if key == "BIOS":
                self.finishing_data_dict[key] = value
            else:
                self.finishing_data_dict[key] = value.get("1.0", "end-1c").rstrip()
        print(self.license_var.get())
        self.finishing_data_dict["License"] = self.license_var.get()
        print(self.camera_var.get())
        self.finishing_data_dict["Camera"] = self.camera_var.get()
        # self.finishing_data_dict["Tester"] = self.tester_value
        # self.finishing_data_dict["Computer type"] = self.computer_type
        self.finishing_data_dict["Tester"] = self.tester_var.get()
        self.finishing_data_dict["Computer type"] = self.type_var.get()
        self.finishing_data_dict["Category"] = self.category_var.get()
        request = infocollector.send_dict(self.finishing_data_dict)
        if request.status_code == 200:
            self.succesful(request.content)
        else:
            self.warning_popup(request.content)

    def succesful(self, text):
        toplevel = Toplevel()
        label = Label(toplevel, text=text, fg="green", font="bold")
        label.pack(side=TOP)

    def add_menubar(self, frame):
        menubar = Menu(frame)

        control_menu = Menu(menubar, tearoff=0)
        control_menu.add_command(label="Sound Interfaces", command=self.sound_interface_control)
        menubar.add_cascade(label="File", menu=control_menu)

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

        menubar.add_command(label="<<Last step>>", command=self.last_step)
        if not infocollector.is_connectable:
            menubar.entryconfig("<<Last step>>", state="disabled")

        root.config(menu=menubar)


infocollector = InfoCollectorClass()
root = Tk()

app = App(root)

root.mainloop()
# root.destroy()
root.quit()