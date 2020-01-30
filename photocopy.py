import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import date
from datetime import datetime
import os.path
import platform, subprocess
import shutil
import re


class PhotocopyManager:            
    current_log_file = None
    total = 0
    current_user = "Marta"
    current_print_type = "Blanco y Negro"
    initial_value_in_the_box = 0
    def init_logger(self):
        print("Init")
        if not os.path.isdir("./datos"):
            os.mkdir("./datos")

        today = date.today()
        label_date = builder.get_object("label_date")
        label_date.set_text(str(today))
        filepath = "./datos/" + str(today) + ".txt" 
        print(filepath)
        if os.path.isfile(filepath):
            print("file exist")
            readed_file = open("./datos/"+str(today)+".txt","r")
            lines = readed_file.readlines()
            position = lines[0].find("TOTAL: ")
            #print(lines[0][position+7])
            offset1=position+7
            offset2=len(lines[0])-4
            result=lines[0][offset1:offset2]
            intresult=result.replace(",", "")
            new_string = ''.join(e for e in intresult if e.isalnum())
            re.sub('[^A-Za-z0-9]+', '', new_string)
            self.total=int(new_string)
        else:
            print("NO FILE")
            new_file = open("./datos/"+str(today)+".txt","w+")
            new_file.write("Fecha: ")
            new_file.write(str(today) + "                                ")
            new_file.write("TOTAL: 0 Gs\n")
            new_file.write("Hora                 Cantidad                Tipo\n")
            new_file.close()
    def calculate_half_of_total(self, total):
        print("half")

class Handler:
    manager = None 
    total = 0
    dialog = None
    def __init__(self, manager):
        manager.init_logger()    
        self.manager = manager 
        self.total = manager.total
        self.update_total_label()

        button1 = builder.get_object("rb_1")
        button1.connect("toggled",self.on_radio_button_marta_select)

        button2 = builder.get_object("rb_2")
        button3 = builder.get_object("rb_3")
        button2.connect("toggled",self.on_radio_button_oski_select)
        button3.connect("toggled",self.on_radio_button_pancha_select)

    def update_total_label(self):
        formated_total = "{:,}".format(self.total) + " Gs"
        label_total = builder.get_object("label_total")
        label_total.set_text(formated_total)
        label_total_in_the_box = builder.get_object("label_total_in_the_box")
        label_total_in_the_box.set_text(str(self.manager.initial_value_in_the_box)) 

    def print_total_to_inform_file(self):
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

    def print_total(self, price, data_type):
        today = date.today()
        current_log_file = open("./datos/"+str(today)+".txt","a")
        self.total = self.total + price
        self.update_total_label() 
        current_time = datetime.now().strftime("%H:%M:%S")
        formated_price =  "{:,}".format(price)
        current_log_file.write(current_time + 
                "                " + formated_price + 
                "                " + data_type + "\n" )
        current_log_file.close() 
        self.print_total_to_inform_file()
   

   ###########################################
    ############       Buttons      ###########
    ###########################################
    def button_input_value_in_box_pressed(self , button):
        input_box = builder.get_object("input_value_in_box")
        value = input_box.get_text()
        value = int(value)
        self.manager.initial_value_in_the_box = value
        self.update_total_label()

    def button_SET_pressed(self, button):
        self.print_total(8000,"Certificado Contribuyente / No Contributente")

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

    def button_retire_pressed(self, button):
        print("retire") 
        self.dialog = builder.get_object("retire_dialog")
        response = self.dialog.run()
    
    def on_dialog_delete_event(self, dialog, event):
        dialog.hide()
        return True

    def button_retire_accept_pressed(self, button):
        input_retire_mount = builder.get_object("dialog_mount_input")
        input_value = input_retire_mount.get_text()
        print(input_value)
        print("accept")
        
        today = date.today()
        out_log_file= open("./datos/"+str(today)+"_out"+".txt","w+")
        out_log_file.write(self.manager.current_user+": ") 
        out_log_file.write(input_value) 
        out_log_file.write("\n") 
        out_log_file.close()
        self.dialog.hide()

    def on_radio_button_select(self, widget , data=None):
        print("radio button changed")
    def on_radio_button_marta_select(self,widget):
        print("marta")
        self.manager.current_user = "Marta"

    def on_radio_button_pancha_select(self,widget):
        print("pacha")
        self.manager.current_user = "Pancha"

    def on_radio_button_oski_select(self,widget):
        print("oski")
        self.manager.current_user = "Oski"

    def button_print_pressed(self, button):
        print("printing")
        today = date.today()
        if platform.system() == 'Windows':    # Windows
            filepath = "datos/" + str(today) + ".txt" 
            relative_path = os.path.abspath(filepath) 
            os.startfile(relative_path, "print") 

    def button_cancel_clicked(self, button):
        print("cancel")
        self.dialog.hide()

    def button_show_data_pressed(self, button):
        today = date.today()
        if platform.system() == 'Windows':    # Windows
            filepath = "datos/" + str(today) + ".txt" 
            relative_path = os.path.abspath(filepath) 
            os.startfile(relative_path)
        else:
            filepath = "./datos/" + str(today) + ".txt" 
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

window = builder.get_object("window1")
window.set_icon_from_file('cat_logo.png')
window.connect("destroy",Gtk.main_quit)
window.show_all()
Gtk.main()
