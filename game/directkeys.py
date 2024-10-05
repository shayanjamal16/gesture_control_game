import ctypes
import time

# For Windows, you don't need libX11.so, you can directly access SendInput from user32
user32 = ctypes.windll.user32
SendInput = user32.SendInput

# Define virtual key codes
right_pressed = 0x4D
left_pressed = 0x4B
space_pressed = 0x39  # Hex code for space key

# Define KeyBdInput structure for Windows
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

# Define Input structure for Windows
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", KeyBdInput)]

# Function to press a key
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to release a key
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    while True:
        PressKey(space_pressed)  # Press space key
        time.sleep(1)
        ReleaseKey(space_pressed)  # Release space key
        time.sleep(1)
