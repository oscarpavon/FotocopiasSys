import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import date
from datetime import datetime
import os.path
import platform, subprocess
import shutil
class PhotocopyManager:            
    current_log_file = None 
    def init_logger(self):
        print("Init")
        if not os.path.isfile("./datos"):
            os.mkdir("./datos")

        today = date.today()
        label_date = builder.get_object("label_date")
        label_date.set_text(str(today))
        filepath = "./datos/" + str(today) + ".txt" 
        print(filepath)
        if os.path.isfile(filepath):
            print("file exist")
        else:
            print("NO FILE")
            new_file = open("./datos/"+str(today)+".txt","w+")
            new_file.write("Fecha: ")
            new_file.write(str(today) + "                                ")
            new_file.write("TOTAL: 0\n")
            new_file.write("Hora                 Cantidad                Tipo\n")
            new_file.close()
        def print_log(self):
            print("Print log") 
class Handler:
    manager = None 
    total = 0
    def __init__(self, manager):
        manager.init_logger()    
        self.manager = manager 

    def print_total(self, price, data_type):
        today = date.today()
        current_log_file = open("./datos/"+str(today)+".txt","a")
        self.total = self.total + price
        formated_total = "{:,}".format(self.total) + " Gs"
        label_total = builder.get_object("label_total")
        label_total.set_text(formated_total)
        current_time = datetime.now().strftime("%H:%M:%S") formated_price =  "{:,}".format(price)
        current_log_file.write(current_time + 
                "                " + formated_price + 
                "                " + data_type + "\n" )
        current_log_file.close() 

    def button_1clicked(self, button):
        print ("Hello, World")
    def button_add_ID_count(self, button):
        self.print_total(1000,"Fotocopia de Cedula")
    def button_add_photocopie_count(self, button):
        self.print_total(500,"Fotocopia Simple Blanco y Negro")
    def button_curriculum_pressed(self, button):
        self.print_total(10000,"Curriculum")
    def button_judment_pressed(self, button):
        self.print_total(7000,"Antecedente Judicial")
    def button_folder_pressed(self, button):
        self.print_total(2000,"Carpeta")
    def button_plastic_pressed(self, button):
        self.print_total(500,"Folio")
    def button_undo_pressed(self, button):
        print("undo") 
    def button_print_pressed(self, button):
        print("undo") 
        today = date.today()
        filepath = "./datos/" + str(today) + ".txt"
        from_file = open(filepath) 
        line = from_file.readline()

        # make any changes to line here

        line = "Fecha: "
        line += str(today) + "                               "
        formated_total = "{:,}".format(self.total) + " Gs"
        line += "TOTAL: " + str(formated_total) + "\n"
        to_file = open(filepath,mode="w")
        to_file.write(line)
        shutil.copyfileobj(from_file, to_file)
    def button_show_data_pressed(self, button):
        today = date.today()
        filepath = "./datos/" + str(today) + ".txt" 
        if platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
    def button_input_mount_pressed(self, button):
        input_mount = builder.get_object("input_value")
        self.print_total(int(input_mount.get_text()),"Varios")
    def onDestroy(self, *args):
        print("Close program")
        Gtk.main_quit()

builder = Gtk.Builder()
builder.add_from_file("user_interface.glade")
new_manager = PhotocopyManager()
handler = Handler(new_manager)
builder.connect_signals(handler)

new_button = builder.get_object("button1")
#new_button.set_label("Hello, World!")

window = builder.get_object("window1")
window.show_all()
Gtk.main()
