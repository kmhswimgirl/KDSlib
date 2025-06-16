from .kds_utils import KdsUtil
import time
 
class Legato110:

    def __init__(self):
        self.kds = KdsUtil()
    
    # utilities

    def address(self, address_num:int):
        pass

    def load(self, qs: bool, method:str):
        if not qs and method != None:
            self.kds.send_line(f"load {method}")
        if not qs and method == None:
            self.kds.send_line("load")
        if qs:
            self.kds.send_line(f"load qs")

    def stop(self):
        self.kds.send_line("stp")
    
    def run(self):
        """Start the set mothod."""
        self.kds.send_line("run") 

    # set parameters
    def set_syringe_size(self, diameter: float, volume: float, units: str):
        dia = str(diameter)
        vol = str(volume)

        self.kds.send_line(f"diameter {dia}")
        time.sleep(0.01)
        self.kds.send_line(f"svolume {vol} {units}")

    def reverse_direction(self):
        self.kds.send_line("rrun")
    # -----------------VOLUME COMMANDS--------------------

    def set_target_volume(self, mode: str):
        pass

    def clear_volume(self, parameter:str):
        if parameter == "infused":
            self.kds.send_line("civolume")
        elif parameter == "target":
            self.kds.send_line("civol")
        elif parameter == "":
            self.kds.send_line("civolume")


    # -----------------TIME COMMANDS--------------------
    def set_target_time(self, time:int):
        sec = str(time)
        self.kds.send_line(f"ttime {sec}")

    def clear_time(self, type:str):
        if type == "infuse":
            self.kds.send_line("citime")
        elif type == "target":
            self.kds.send_line("cttime")
        elif type == "both":
            self.kds.send_line("ctime")
        elif type == "withdraw":
            self.kds.send_line("cwtime")
        else:
            print("command not recognized")
    
    def display_time(self, type:str): # do all display cmds in another issue
        pass

