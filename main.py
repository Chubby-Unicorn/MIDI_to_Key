import sys
import time
from rtmidi.midiutil import open_midiinput
from pynput.keyboard import Key, Controller
from pynput.mouse import Button
from pynput.mouse import Controller as mController

def mapKey(midi_key:int, kState:bool):
    """Maps a midi device key to a keyboard or mouse key.
    returns (keyboard(False) / mouse(True), action)"""
    mvector = ((0, 5), (0, -5), (-5, 0), (5, 0))

    match midi_key:
        case 36: sendKey(Key.esc, kState)       # C3
        case 40: sendKey(Key.ctrl_l, kState)    # E3
        case 41: sendKey(Key.shift_l, kState)   # F3
        case 42: sendKey('q', kState)           # F3#
        case 43: sendKey('a', kState)           # G3
        case 44: sendKey('w', kState)           # G3#
        case 45: sendKey('s', kState)           # A3
        case 46: sendKey('e', kState)           # A3#
        case 47: sendKey('d', kState)           # 
        case 48: sendKey(Key.space, kState)     # C4
        # mouse controlls
        case 89: moveMouse(mvector[2])          # cc  MOVE_LEFT
        case 89: sendMButton(Key.space, kState) # cc  BUTTON_LEFT
        case 91: moveMouse(mvector[1], kState)  # cc  MOVE_DOWN
        case 92: moveMouse(mvector[0], kState)  # cc  MOVE_UP
        case 93: moveMouse(mvector[3], kState)  # cc  MOVE_RIGHT
        case 94: sendMButton(Key.space, kState) # cc  BUTTON_RIGHT
        case _: return False

    return True

def sendKey(_ascii, down:bool):
    keyboard = Controller()
    if down:
        keyboard.press(_ascii)
        return
    keyboard.release(_ascii)
    return

def sendMButton(button, down:bool):
    pass

def moveMouse(vector, down:bool):
    pass

def main():
    getMidiKey()

def getMidiKey():
    port = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")

    try:
        while True:
            msg = midiin.get_message()
            if msg:
                [key_state, key, *_], *_ = msg
                mapKey(key, key_state == 144)
                print(f"{key_state}, {key}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin

if __name__ == "__main__": main()