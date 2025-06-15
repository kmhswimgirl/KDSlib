from kds_utils import KdsUtil
 
class Legato110:

    def __init__(self):
        self.kds = KdsUtil()
    
    def config(self, ):
        pass

    def load(self, qs: bool, method:str):
        if not qs and method != None:
            self.kds.send_line(f"load {method}")
        if not qs and method is None:
            self.kds.send_line("load")
        if qs:
            self.kds.send_line(f"load qs {method}")

    def stop(self):
        self.kds.send_line("stp")
    
    def run(self):
        self.kds.send_line("run")

    def set_syringe_size(self, diameter: float):
        self.kds.send_line("")
        pass

    def set_target_volume(self, mode: str):
        pass

    def reverse_direction(self, mode: str):
        pass

    def time(self, clear:bool, mode: str, seconds:int):
        pass

    def clear_time(self, mode:str):
        pass

    def infuse(self, ):
        pass
