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


    # set parameters
    def set_syringe_size(self, diameter: float, volume: float, units: str):
        dia = str(diameter)
        vol = str(volume)

        self.kds.send_line(f"diameter {dia}")
        time.sleep(0.01)
        self.kds.send_line(f"svolume {vol} {units}")

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

    # -----------------VOLUME COMMANDS--------------------
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

    def set_infuse_ramp(self, time:int, start_rate:int = 0, end_rate:int = 0, units:str = "ml", start_rate_max:bool = False, start_rate_min:bool = False, end_rate_max:bool = False, end_rate_min:bool = False):
        # error handling for start rate
        if start_rate_max and start_rate_min:
            print("[SIRamp]: two values set for the same rate")
            return
        elif start_rate_min:
            start_r = "min"
        elif start_rate_max:
            start_r = "max"
        else:
            start_r = str(start_rate)

        # error handling for end rate
        if end_rate_max and end_rate_min:
            print("[SIRamp]: two values set for the same rate")
            return
        elif end_rate_max:
            end_r = "max"
        elif end_rate_min:
            end_r = "min"
        else:
            end_r = str(end_rate)
        
        self.kds.send_line(f"iramp {start_r} {end_r} {units} {time}")
      
    def set_withdraw_ramp(self, start_rate:int, end_rate:int, units:str, time:int, start_rate_max:bool = False, end_rate_max:bool = False):
        pass