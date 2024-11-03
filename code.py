# code.py
import board
import digitalio
import usb_hid
import usb_midi
import struct
import time
import neopixel
from adafruit_debouncer import Debouncer
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn

# Define the GPIO pins connected to the buttons
button_pins = [board.GP2, board.GP3, board.GP4]

# Map buttons to MIDI note numbers
button_notes = [50, 51, 52]  # Note numbers for buttons 1, 2, and 3

# Initialize NeoPixel
pixel = neopixel.NeoPixel(board.GP16, 1)
pixel.brightness = 0.05

# Initialize buttons with Debouncer
buttons = []
for pin in button_pins:
    pin_input = digitalio.DigitalInOut(pin)
    pin_input.direction = digitalio.Direction.INPUT
    pin_input.pull = digitalio.Pull.UP
    debounced_button = Debouncer(pin_input, interval=0.05)
    buttons.append(debounced_button)

# Prepare the HID report (2-byte report)
report = bytearray(2)

# Get the custom HID device (ensure it's the correct one)
hid_device = usb_hid.devices[0]  # Only one HID device is enabled

# Initialize MIDI
midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print("ClickoPico ready!")

while True:
    # Update debouncer for each button
    for button in buttons:
        button.update()

    # Check for transitions
    send_report = False
    button_state = 0
    for i, button in enumerate(buttons):
        if button.rose or button.fell:
            send_report = True

            # Send MIDI messages on transitions
            note = button_notes[i]
            if button.rose:
                # Button released: Send Note On with velocity 0 (Note Off)
                print("Button", i, "released")
                midi.send(NoteOn(note, 0))
                pixel.fill((0, 0, 0))
            elif button.fell:
                # Button pressed: Send Note On with velocity 127
                print("Button", i, "pressed")
                midi.send(NoteOn(note, 127))
                pixel.fill((255, 0, 0))

        if not button.value:
            # Button is pressed
            button_state |= 1 << i  # Set bit i
        else:
            # Button is released
            button_state &= ~(1 << i)  # Clear bit i

    if send_report:
        # Pack the button_state into the report as two bytes
        report[0] = button_state & 0xFF
        report[1] = (button_state >> 8) & 0xFF
        hid_device.send_report(report)
        print("Sent HID report: ", report)

    time.sleep(0.005)
