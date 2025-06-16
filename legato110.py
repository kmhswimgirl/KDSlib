from .kds_utils import KdsUtil
import time
 
class Legato110:

    def __init__(self):
        self.kds = KdsUtil()
    
    def address(self, address_num:int):
        pass

    def load(self, qs: bool, method:str):
        if not qs and method != None:
            self.kds.send_line(f"load {method}")
        if not qs and method is None:
            self.kds.send_line("load")
        if qs:
            self.kds.send_line(f"load qs")

    def stop(self):
        self.kds.send_line("stp")
    
    def run(self):
        """Start the pump running."""
        self.kds.send_line("run") 

    def set_syringe_size(self, diameter: float, volume: float, units: str):
        dia = str(diameter)
        vol = str(volume)

        self.kds.send_line(f"diameter {dia}")
        time.sleep(0.01)
        self.kds.send_line(f"svolume {vol} {units}")

    def set_target_volume(self, mode: str):
        pass

    def reverse_direction(self):
        self.kds.send_line("rrun")

    def time(self, clear:bool, mode: str, seconds:int):
        pass

    def clear_volume(self, parameter:str):
        if parameter is "iVol" or "iv" or "infused volume":
            self.kds.send_line("civolume")
        elif parameter is "target volume":
            self.kds.send_line("civol")
        elif parameter is "":
            self.kds.send_line("civolume")
        pass

    def clear_time(self, type:str):
        if type is "infuse":
            self.kds.send_line("citime")
        elif type is "target":
            self.kds.send_line("citime")
        elif type is "both":
            self.kds.send_line("ctime")
        elif type is "withdraw":
            self.kds.send_line("cwtime")

    def infuse(self, ):
        pass
