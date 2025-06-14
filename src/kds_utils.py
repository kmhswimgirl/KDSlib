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
        """Open serial connection."""
        try:
            self.ser = serial.Serial(**self.config)
            return True
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        """Close serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_line(self, command: str, read: bool = False) -> Optional[str]:
        """
        Send command and optionally read response.
        
        Args:
            command (str): Command to send
            read (bool): Whether to read response
            
        Returns:
            Optional[str]: Response if read=True, None otherwise
        """
        if not self.ser or not self.ser.is_open:
            return None
            
        try:
            # Send command
            self.ser.write(f"{command}\r\n".encode(self.config['encoding']))
            
            # Return response if requested
            if read:
                return self.ser.readline().decode(self.config['encoding']).strip()
            return None
            
        except (serial.SerialException, UnicodeError) as e:
            print(f"Communication error: {e}")
            return None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def __del__(self):
        """Cleanup on deletion."""
        self.disconnect()

def testing():
    kds = KdsUtil()
    kds.connect()
    kds.send_line("config")

if __name__ == "__main__":
    testing()