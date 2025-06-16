from .kds_utils import KdsUtil
import time
 
class Legato110:

    def __init__(self):
        self.kds = KdsUtil()
    
    # utilities

   

    def load(self, qs: bool, method:str):
        if not qs and method != None:
            self.kds.send_line(f"load {method}")
        if not qs and method == None:
            self.kds.send_line("load")
        if qs:
            self.kds.send_line(f"load qs")


    # set parameters
    def set_syringe_size(self, diameter: float, volume: float, units: str):
        dia = str(diameter)
        vol = str(volume)

        self.kds.send_line(f"diameter {dia}")
        time.sleep(0.01)
        self.kds.send_line(f"svolume {vol} {units}")
    # -----------------SYSTEM COMMANDS--------------------
    def address(self, address_num:int):
        pass

    def ascale(self, scale_value:int):
        pass

    def set_baud(self, baudrate:int):
        pass

    def boot(self):
        pass

    def catalog(self):
        pass

    def command_set(self, set:str):
        pass

    def config(self):
        pass

    def delmethod(self, mathod_name:str):
        pass

    def dim_screen(self, value:int):
        pass

    def echo(self):
        pass

    def free(self):
        pass

    def force(self, force_percent:int):
        pass

    def ftswitch(self, value:int):
        pass

    def mode(self):
        # displays mode, later issue
        pass
    
    def poll(self, mode:str):
        # potential vals are on, off, remote
        pass

    def remote(self, pump_addr:int):
        pass

    def calibrate_tilt(self):
        pass

    def set_time(self, time:int):
        pass

    def get_version(self, verbose:bool):
        pass

    # -----------------RUN COMMANDS--------------------
    def run(self):
        self.kds.send_line("run") 

    def reverse_direction(self):
            self.kds.send_line("rrun")

    def stop(self):
        self.kds.send_line("stp")

    def run_motors(self, direction:str):
        if direction == "infuse":
            self.kds.send_line("irun")
        elif direction == "withdraw":
            self.kds.send_line("wrun")
        else:
            print("[RM]: Invalid input. Requires: [infuse | withdraw]")

    # -----------------VOLUME COMMANDS-----------------
    def set_target_volume(self, volume:int, units:str):
        self.kds.send_line(f"tvolume {volume} {units}")

    def clear_volume(self, parameter:str):
        if parameter == "infuse":
            self.kds.send_line("civolume")
        elif parameter == "target":
            self.kds.send_line("ctvolume")
        elif parameter == "bothDirs":
            self.kds.send_line("cvolume")
        elif parameter == "withdraw":
            self.kds.send_line("cwvolume")
        else:
            print("[CV]: command not recognized")

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
            print("[CT]: command not recognized")
    
    def display_time(self, type:str): # do all display cmds in another issue
        pass

    # -----------------RATE COMMANDS--------------------
    def set_infuse_rate(self, units:str = "", rate:int = 0, setMax:bool = False, setMin:bool = False):
        if setMax:
            self.kds.send_line(f"irate max")
        elif setMin:
            self.kds.send_line(f"irate min")
        elif not setMax or setMin:
            self.kds.send_line(f"irate {rate} {units}")
        else:
            print("[SIRate]: please check documentation. incorrect cmd format")

    def set_withdraw_rate(self, units:str = "",rate:int = 0, setMax:bool = False, setMin:bool = False):
        if setMax:
            self.kds.send_line(f"wrate max")
        elif setMin:
            self.kds.send_line(f"wrate min")
        elif not setMax or setMin:
            self.kds.send_line(f"wrate {rate} {units}")
        else:
            print("[SWRate]: please check documentation. incorrect cmd format")

    def set_infuse_ramp(self, start_rate:str, end_rate:str, start_units:str, end_units:str, time:int):
        if start_rate == "max" or "min":
            self.kds.send_line(f"iramp {start_rate} {end_rate} {end_units} {time}")
        elif end_rate == "max" or "min":
            self.kds.send_line(f"iramp {start_rate} {start_units} {end_rate} {time}")
        elif end_rate == "max" or "min" and start_rate == "max" or "min":
            self.kds.send_line(f"iramp {start_rate} {end_rate} {time}")
        else:
            self.kds.send_line(f"iramp {start_rate} {start_units} {end_rate} {end_units} {time}")