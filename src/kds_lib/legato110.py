from .kds_utils import KdsUtil
import time
 
class Legato110:
    def __init__(self, port:str, baud: int):
        self.port = port
        self.baud = baud
        self.kds = KdsUtil(self.port, self.baud)

    def load(self, qs: bool, method:str):
        if not qs and method != None:
            self.kds.send_line(f"load {method}")
        if not qs and method == None:
            self.kds.send_line("load")
        if qs:
            self.kds.send_line(f"load qs")

    # -----------------SYSTEM COMMANDS--------------------
    def address(self, address_num:int):
        self.kds.send_line(f"address {address_num}")

    def ascale(self, scale_value:int):
        self.kds.send_line(f"ascale {scale_value}")

    def set_device_baud(self, baudrate:int):
        valid_baud = [9600, 19200, 38400, 57600, 115200, 128000, 230400, 256000, 460800, 921600]
        if baudrate in valid_baud:
            self.kds.send_line(f"baud {baudrate}")
        else:
            print("[BAUD]: invalid baudrate")

    def boot(self):
        self.kds.send_line("boot")

    def catalog(self):
        # display command, another issue
        pass

    def command_set(self, set:str):
        self.kds.send_line(f"cmd {set}")
        if set != "ultra" or "22" or "44":
            print("[CMD]: invalid command")

    def default_config(self): # can't remember if tested...
        self.kds.send_line("config a400,g1,p2.4,t24,br,n0.1,x33,e100")
        print("[IMPORTANT]: Device needs to be power cycled in order to apply changes!")

    def config(self, param:list, value:list):
        if len(value) != len(param):
            print("[ERR]: must have the same number of parameters as values")
        # ERR --> check if both are equal length
        # zip into one list of tuples
        final_list=[]
        combined_list = list(zip(param, value))
        # index through list matching each to a case

        def value_error():
            print(f"[ERR]: Value outside of range --> {item[0]}")
        
        def reboot_warning():
            print("[IMPORTANT]: Device needs to be power cycled in order to apply changes!")

        for item in combined_list:
            val = item[1]
            match item[0]:
                case "steps_per_rev": # if parameter is steps per rev
                    if val >= 10 or val <= 400:
                        final_list.append(f"a{val}")
                    else:
                        value_error()

                case "gear_ratio": # if parameter is gear ratio
                    if val > 0:
                        final_list.append(f"g{val}")
                    else:
                        value_error()

                case "pulley_ratio": # if parameter is steps per rev
                    if val > 0:
                        final_list.append(f"p{val}")
                    else:
                        value_error()

                case "lead_screw": 
                    final_list.append(f"t{val}")

                case "motor_polarity": 
                    if val == "r" or val == "f":
                        final_list.append(f"b{val}")
                    else:
                        value_error()

                case "encoder":
                    if val > 0 and val < 400:
                        final_list.append(f"e{val}")
                    else:
                        value_error()
                case _:
                    print("[ERR]: Not a valid parameter")
                    return None

        # handle formatting after adding 
        params_string = ','.join(final_list)
        self.kds.send_line(f"config {params_string}")
        reboot_warning()

    def delete_method(self, method_name:str):
        self.kds.send_line(f"delmethod {method_name}")

    def dim_screen(self, brightness:int):
        if brightness < 0 or brightness > 100:
            print("[DIM]: Brightness out of valid range.")
        else:
            self.kds.send_line(f"dim {brightness}")

    def echo(self):
        self.kds.send_line("echo")

    def force(self, force_percent:int):
        self.kds.send_line(f"force {force_percent}")

    def set_footswitch_mode(self, mode:str):
        valid_modes = ["mom", "rise", "fall"]
        if mode in valid_modes:
            self.kds.send_line(f"ftswitch {mode}")
        else:
            print("[SFM]: Not a valid footswitch mode")

    def poll(self, mode:str):
        # potential vals are on, off, remote
        if mode == "on" or "off" or "remote":
            self.kds.send_line(f"poll {mode}")
        else:
            print("[P]: invalid input")

    def remote(self, pump_addr:int):
        if pump_addr > 100 or pump_addr < 0:
            return ("[REM]: Invalid address.")
        else:
            self.kds.send_line(f"remote {pump_addr}")

    def calibrate_tilt(self):
        self.kds.send_line("tilt")

    def set_time(self, date:str, time:str):
        self.kds.send_line(f"time {date} {time}")

    # -----------------SYRINGE COMMANDS--------------------
    def set_syringe_size(self, diameter: float, volume: float, units: str):
        dia = str(diameter)
        vol = str(volume)

        self.kds.send_line(f"diameter {dia}")
        time.sleep(0.01)
        self.kds.send_line(f"svolume {vol} {units}")
    
    def set_syringe_count(self, number:int):
        self.kds.send_line(f"gang {number}")

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
            print("[CT]: command not recognized. Use [infuse | target | both | withdraw]")

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
