# boot.py
import supervisor
import usb_hid
import usb_midi

# Set the USB VID and PID to match the original device
supervisor.set_usb_identification(
    vid=0x05F3,
    pid=0x00FF,
    manufacturer="ClickoPico",
    product="VEC USB Footpedal Emulator"
)

# Define HID report descriptor for a gamepad with 16-bit report
REPORT_DESCRIPTOR = bytes((
    0x05, 0x09,        # Usage Page
    0x09, 0x01,        # Usage (Button)
    0xA1, 0x01,        # Collection (Application)
    0x15, 0x00,        #   Logical Minimum (0)
    0x26, 0xFF, 0x00,  #   Logical Maximum (255)
    0x75, 0x08,        #   Report Size (8 bits)
    0x95, 0x02,        #   Report Count (2)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x03,        #   Usage Maximum (Button 3)
    0x81, 0x02,        #   Input (Data, Var, Abs)
    0xC0               # End Collection
))

# Enable only the custom HID device
usb_hid.enable((
    usb_hid.Device(
        report_descriptor=REPORT_DESCRIPTOR,
        usage_page=0x09,  # Generic Desktop Controls
        usage=0x01,       # Game Pad
        report_ids=(0,),  # No Report ID
        in_report_lengths=(2,),  # 2-byte input report
        out_report_lengths=(0,), # No output reports
    ),
))

# Enable USB MIDI
usb_midi.enable()

