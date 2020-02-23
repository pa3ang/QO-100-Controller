# PA3ANG, February - 2020
# version 1.0
#
# This program connects to a FT817/818 transceiver and reads the RX frequency and calculate the TX frequency for
# the working on the QO-100 transponder. The TX frequency is calculated based on the LNB TCXO offset, the
# uplink transvertor IF frequency. Both have + or - delta figures. The Frequency is in 10Hz size.
#

import serial
import time
from tkinter import *

# Constants  (choose based on platform)
SERIAL_PORT = "/dev/ttyUSB0"
#SERIAL_PORT = "COM8"

# User presets  (Frequency *10Hz)
Home_frequency = 1048968000
Beacon_frequency = 1048975000

# Up and Down link offsets (Frequency *10Hz)
LNB_OFFSET = 1005697900
LNB_CALIBRATE = -16
UPLINK_LO_FREQUENCY = 196800000 - 23

# Serial port settings
SERIAL_SPEED = 34800
SERIAL_STOPBITS = serial.STOPBITS_TWO
SERIAL_TIMEOUT = 1.0
SERIAL_POLLING = 500   # in milliseconds

# Transceiver commands
CMD_READ_FREQ = [0x00, 0x00, 0x00, 0x00, 0x03]
CMD_READ_PTT = [0x00, 0x00, 0x00, 0x00, 0xF7]
CMD_TOGGLE_VFO = [0x00, 0x00, 0x00, 0x00, 0x81]
CMD_SET_PSK = [0x0C, 0x00, 0x00, 0x00, 0x07]
CMD_SET_USB = [0x01, 0x00, 0x00, 0x00, 0x07]
CMD_SET_CW = [0x02, 0x00, 0x00, 0x00, 0x07]
CMD_START_TX = [0x00, 0x00, 0x00, 0x00, 0x08]
CMD_STOP_TX = [0x00, 0x00, 0x00, 0x00, 0x88]

# Default vaiables
QO_frequency = 0
RX_frequency = 0
TX_frequency = 0
M1_frequency = 0
M2_frequency = 0
M3_frequency = 0
Return_frequency=0
mode = "01"

# boolean for program flow
updatetx = False
pulse = False
setfreq = False
setmode = False
setcal = False
tune_status = 0

# make a TkInter Window
window = Tk()
window.geometry("430x130")
window.wm_title(""+SERIAL_PORT+" : "+str(SERIAL_SPEED)+" Bd")

# functions
def update_tx ():
    global updatetx
    updatetx = True

def calibrate_down ():
    global LNB_CALIBRATE
    LNB_CALIBRATE = LNB_CALIBRATE - 1

def calibrate_up ():
    global LNB_CALIBRATE
    LNB_CALIBRATE = LNB_CALIBRATE + 1

def set_home ():
    global setfreq, updatetx, Home_frequency, New_frequency
    setfreq = True
    updatetx = True
    New_frequency = Home_frequency

def set_bcn ():
    global setfreq, setcal,  Beacon_frequency, New_frequency, QO_freqency, Return_frequency
    setcal = True
    Return_frequency = QO_frequency
    setfreq = True
    New_frequency = Beacon_frequency
    button_bcn.configure(text="SET", command= calibrate, bg="red")
    button_funct.configure(text="ESC", command= esc_function, bg="green")

def toggle_mode ():
    global setmode, mode
    if mode == "01":
       mode = "02"
       button_mode.configure(text="USB")
    else:
       mode = "01"
       button_mode.configure(text="CW")
    setmode = True
    esc_function()

def calibrate ():
    global mode, QO_frequency, LNB_CALIBRATE, Beacon_frequency
    LNB_CALIBRATE = LNB_CALIBRATE - (QO_frequency -Beacon_frequency)
    button_bcn.configure(text="BCN", command= set_bcn, bg=window["bg"])
    # mode back in USB for safety and return to old frequency via esc_function sub
    mode = "02"
    toggle_mode()

def store_m1 ():
    global QO_frequency, M1_frequency
    M1_frequency = QO_frequency
    button_m1.configure(fg="red")
    button_m1.configure(command = restore_m1)
    esc_function()

def restore_m1 ():
    global setfreq, updatetx, M1_frequency, New_frequency
    setfreq = True
    New_frequency = M1_frequency
    updatetx = True
    esc_function()

def store_m2 ():
    global QO_frequency, M2_frequency
    M2_frequency = QO_frequency
    button_m2.configure(fg="red")
    button_m2.configure(command = restore_m2)
    esc_function()

def restore_m2 ():
    global setfreq, updatetx, M2_frequency, New_frequency
    setfreq = True
    New_frequency = M2_frequency
    updatetx = True
    esc_function()

def store_m3 ():
    global QO_frequency, M3_frequency
    M3_frequency = QO_frequency
    button_m3.configure(fg="red")
    button_m3.configure(command = restore_m3)
    esc_function()

def restore_m3 ():
    global setfreq, updatetx, M3_frequency, New_frequency
    setfreq = True
    New_frequency = M3_frequency
    updatetx = True
    esc_function()

def up_function ():
    global M1_frequency, M2_frequency, M3_frequency
    if M1_frequency != 0:
       button_m1.configure(fg="green")
       button_m1.configure(command = store_m1)
    if M2_frequency != 0:
       button_m2.configure(fg="green")
       button_m2.configure(command = store_m2)
    if M3_frequency != 0:
       button_m3.configure(fg="green")
       button_m3.configure(command = store_m3)
    button_funct.configure(text="ESC", command= esc_function, bg=window["bg"])

def normal_function ():
    global M1_frequency, M2_frequency, M3_frequency
    if M1_frequency != 0:
       button_m1.configure(fg="red")
       button_m1.configure(command = restore_m1)
    if M2_frequency != 0:
       button_m2.configure(fg="red")
       button_m2.configure(command = restore_m2)
    if M3_frequency != 0:
       button_m3.configure(fg="red")
       button_m3.configure(command = restore_m3)

def esc_function ():
    global setfreq, setcal, mode, tune_status, New_frequency, Return_frequency
    button_bcn.configure(text="BCN", command= set_bcn, bg=window["bg"])
    button_funct.configure(text="F", command= up_function, bg=window["bg"])
    if setcal is True:
       New_frequency = Return_frequency
       setfreq = True
       setcal = False
       mode = "02"
       toggle_mode()
    if tune_status is 2:
       toggle_tune()
       tune_status = 0
       button_tune.configure(bg=window["bg"], command= tune)
    normal_function()

def read_ptt ():
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)
    cmd = CMD_READ_PTT
    ser.write(cmd)
    resp = ser.read()
    ser.close()
    #check if bit 7 is 0
    if ord(resp)&128 == False:
       # transmitting
       label_9.config(text="")
       label_10.config(text=">")
       return True
    else:
       # receiving
       label_9.config(text=">")
       label_10.config(text="")
       return False

def tune ():
    global tune_status
    tune_status = 1

def tx_tune():
    global tune_status
    toggle_tune()
    button_tune.configure(bg="red", command= esc_function)
    button_funct.configure(text="ESC", command= esc_function, bg="green")
    tune_status = 2

def toggle_tune():
    global tune_status
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)
    if tune_status == 2:
        cmd = CMD_STOP_TX
    else:
        cmd = CMD_TOGGLE_VFO
    ser.write(cmd)
    time.sleep(.2)
    if tune_status == 2:
        cmd = CMD_TOGGLE_VFO
    else:
        cmd = CMD_SET_PSK
    ser.write(cmd)
    time.sleep(.2)
    if tune_status == 2:
        cmd = CMD_SET_USB
    else:
        cmd = CMD_TOGGLE_VFO
    ser.write(cmd)
    time.sleep(.2)
    if tune_status == 2:
        cmd = CMD_TOGGLE_VFO
    else:
        cmd = CMD_START_TX
    ser.write(cmd)
    time.sleep(.2)
    ser.close()

def read_frequency ():
    # this is the mainloop and controls the serial port
    global ser, updatetx, pulse, setfreq, setmode, setcal, mode, tune_status
    global QO_frequency, New_frequency
    if tune_status is 1:
       tx_tune()

    if read_ptt() is False:
       label_8.config(fg="black")

       # check if user clicked a menu button
       # these routines go first and do theitr own serial port control
       if setfreq == True:
           set_frequency(New_frequency)
           setfreq = False
       if setmode == True:
           set_mode(mode)
           setmode = False

       # open serial port
       ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)

       # read frequency and convert bytes to frequency, calculate QO frequency based on LNB_OFFSET + LNB_CALIBRATE
       cmd = CMD_READ_FREQ
       ser.write(cmd)
       resp = ser.read(5)
       resp_bytes = (resp[0], resp[1], resp[2], resp[3])
       frequency = "%02x%02x%02x%02x" % resp_bytes
       RX_frequency = int(frequency)
       QO_frequency = RX_frequency + LNB_OFFSET + LNB_CALIBRATE
       RX_frequency = (QO_frequency - LNB_OFFSET - LNB_CALIBRATE)/100000

       # check if user wants to update TX frequency 
       # this routine is embedded in this 'open serial port' routine
       if updatetx == True:
           update_tx_frequency()
           updatetx = False

       # close serial port to clean buffer
       ser.close()

       # display frequencies and make TX red if update click by the user is needed
       label_7.config(text=LNB_CALIBRATE )
       QOF = ('{0:.2f}'.format(QO_frequency/100))
       label_4.config(text=QOF)
       RXF = ('{0:.5f}'.format(RX_frequency))
       label_5.config(text=RXF)
       if (QO_frequency - 808950000 - UPLINK_LO_FREQUENCY) != TX_frequency:
          label_6.config(foreground="red")

    # display pulse
    pulse = not pulse
    if pulse is True:
       label_8.config(text="*")
    else:
       label_8.config(text=" ")

    # keep reading every second
    window.after(SERIAL_POLLING, read_frequency)

def set_frequency (frequency):
    # calculate RX frequency based on 680_frequency  LNB_OFFSET - LNB_CALIBRATE
    RX_frequency = (frequency - LNB_OFFSET - LNB_CALIBRATE)
    RX_frequencyStr = str(RX_frequency)
    RX_P1 = "%02d" % int(RX_frequencyStr[0:2], 16)
    RX_P2 = "%02d" % int(RX_frequencyStr[2:4], 16)
    RX_P3 = "%02d" % int(RX_frequencyStr[4:6], 16)
    RX_P4 = "%02d" % int(RX_frequencyStr[6:8], 16)

    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)

    # write TX frequency and wait processing
    cmd = [int(RX_P1), int(RX_P2), int(RX_P3), int(RX_P4), 1]
    ser.write(cmd)
    ser.close()
    time.sleep(.2)

def set_mode (mode):
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)

    # write frequency and new in both VFO
    for _ in range(2):
    	cmd = [int(mode), 0, 0, 0, 7]
    	ser.write(cmd)
    	time.sleep(.2)

    	# toggle VFO and wait for processing
    	cmd = CMD_TOGGLE_VFO
    	ser.write(cmd)
    	time.sleep(.2)

    ser.close()

def update_tx_frequency ():
    global TX_frequency

    # read current frequency again
    cmd = CMD_READ_FREQ
    ser.write(cmd)
    resp = ser.read(5)
    resp_bytes = (resp[0], resp[1], resp[2], resp[3])
    frequency = "%02x%02x%02x%02x" % resp_bytes
    RX_frequency = int(frequency)
    QO_frequency = ((RX_frequency + LNB_OFFSET + LNB_CALIBRATE ))

    # calculate TX frequency based on QO frequency - Transponder offset - UPLINK_LO_FREQUENCY and convert into bytes
    TX_frequency = (QO_frequency - 808950000 - UPLINK_LO_FREQUENCY)
    TX_frequencyStr = str(TX_frequency)
    TX_P1 = "%02d" % int(TX_frequencyStr[0:2], 16)
    TX_P2 = "%02d" % int(TX_frequencyStr[2:4], 16)
    TX_P3 = "%02d" % int(TX_frequencyStr[4:6], 16)
    TX_P4 = "%02d" % int(TX_frequencyStr[6:8], 16)

    # toggle VFO and wait for processing
    cmd = CMD_TOGGLE_VFO
    ser.write(cmd)
    time.sleep(.2)

    # write TX frequency and wait processing
    cmd = [int(TX_P1), int(TX_P2), int(TX_P3), int(TX_P4), 1]
    ser.write(cmd)
    time.sleep(.2)

    # toggle VFO again
    cmd = CMD_TOGGLE_VFO
    ser.write(cmd)

    # write fequency into window
    TXF = ('{0:.5f}'.format(TX_frequency/100000))
    label_6.config(text=TXF)
    label_6.config(foreground="black")

# write information in Tkinter Window
label_1 = Label(window, text="QO-100", font=('Arial', 16, 'bold'), width=8).grid(column=1, row=1)
label_2 = Label(window, text="Rx", font=('Arial', 16, 'bold')).grid(column=1, row=2)
label_3 = Label(window, text="Tx", font=('Arial', 16, 'bold')).grid(column=1, row=3)
label_4 = Label(window, font=('Arial', 16, 'bold'), width=14)
label_4.grid(column=2, row=1)
label_5 = Label(window, font=('Arial', 16, 'bold'))
label_5.grid(column=2, row=2)
label_6 = Label(window, text="------", font=('Arial', 16, 'bold'))
label_6.grid(column=2, row=3)
label_7 = Label(window, font=('Arial', 14, 'bold'))
label_7.grid(column=3, row=1)
label_8 = Label(window, font=('Arial', 14, 'bold'))
label_8.place(x=100, y=6)
label_9 = Label(window, text=">", font=('Arial', 14, 'bold'))
label_9.place(x=14, y= 34)
label_10 = Label(window, text="", font=('Arial', 14, 'bold'))
label_10.place(x=14, y= 65)

Button(window, text = "Update TX", command = update_tx, width=14).grid(column=3, row=3)
button_tune = Button(window, text = "Tune", command = tune, width=5)
button_tune.grid(column=3, row=2, sticky="E")
button_bcn = Button(window, text = "BCN", command = set_bcn, width=5)
button_bcn.grid(column=3, row=2, sticky="W")
Button(window, text = "<", command = calibrate_down).grid(column=3, row=1, sticky="W")
Button(window, text = ">", command = calibrate_up).grid(column=3, row=1, sticky="E")

Button(window, text = "HOME", command = set_home, width=8).grid(column=1, row=4)
button_mode = Button(window, text = "CW", command = toggle_mode, width=3)
button_mode.grid(column=2, row=4)
button_funct = Button(window, text = "F", command = up_function, width=3)
button_funct.grid(column=2, row=4, sticky="E")
button_m1 = Button(window, text = "M1", command = store_m1, width=2)
button_m1.grid(column=3, row=4, sticky="W")
button_m2 = Button(window, text = "M2", command = store_m2, width=2)
button_m2.grid(column=3, row=4)
button_m3 = Button(window, text = "M3", command = store_m3, width=2)
button_m3.grid(column=3, row=4, sticky="E")

read_frequency()
window.mainloop()
