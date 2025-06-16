import serial
from typing import Optional

class KdsUtil:
    def __init__(self):
        self.ser: Optional[serial.Serial] = None
        self.port = '/dev/tty.usbmodem11297211'  # Update this to match your port
        self.baudrate = 9600
        self.timeout = 1
        self.connect()  # Automatically connect on initialization
    
    def connect(self) -> bool:
        """Initialize and open the serial connection."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            if not self.ser.is_open:
                self.ser.open()
            return True
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")
            return False

    def send_line(self, command: str) -> None:
        """Send a command to the pump."""
        if not self.ser or not self.ser.is_open:
            self.connect()  # Try to reconnect if not connected
            if not self.ser or not self.ser.is_open:
                raise RuntimeError("Could not establish serial connection.")
        
        command_bytes = f"{command}\r\n".encode('ascii')
        self.ser.write(command_bytes)
        self.ser.flush()

    def __del__(self):
        """Clean up serial connection on object destruction."""
        if self.ser and self.ser.is_open:
            self.ser.close()

def testing():
    kds = KdsUtil()
    kds.connect()
    kds.send_line("config")

if __name__ == "__main__":
    testing()