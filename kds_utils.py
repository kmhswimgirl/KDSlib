import serial
from typing import Optional

class KdsUtil:

    def __init__(self, port: str = '/dev/tty.usbserial', baud_rate: int = 9600):
        self.ser: Optional[serial.Serial] = None
        self.config = {
            'port': port,
            'baudrate': baud_rate,
            'timeout': 1,
            'encoding': 'ascii'
        }

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(**self.config)
            return True
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_line(self, command: str) -> Optional[str]:
        if not self.ser or not self.ser.is_open:
            return None
        try:
            # Send command
            self.ser.write(f"{command}\r\n".encode(self.config['encoding']))
            return self.ser.readline().decode(self.config['encoding']).strip()

        except (serial.SerialException, UnicodeError) as e:
            print(f"Communication error: {e}")
            return None

    def __enter__(self):
        self.connect()
        return self
    
    def __del__(self):
        self.disconnect()

def testing():
    kds = KdsUtil()
    kds.connect()
    kds.send_line("config")

if __name__ == "__main__":
    testing()