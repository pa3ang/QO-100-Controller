# PA3ANG, February - 2020
# version 2.0 ala FT991A Controller
# no auto update but manual 


# Libraries
import serial
import time
from tkinter import *

# Port
SERIAL_PORT = "/dev/ttyUSB0"

# User presets  (Frequency *10Hz)
Home_frequency      = 1048968000
Cw_band_frequency   = 1048952500
Beacon_frequency    = 1048975000

# Up and Down link offsets (Frequency *10Hz)
LNB_OFFSET          = 1005697050
LNB_CALIBRATE       = -0
UPLINK_LO_FREQUENCY = 196800000 - 50

SETTLE_TIME         = .2

# Serial port settings
SERIAL_SPEED        = 38400
SERIAL_STOPBITS     = serial.STOPBITS_TWO
SERIAL_TIMEOUT      = 1.0
SERIAL_POLLING      = 500   # in milliseconds

# Transceiver commands
CMD_READ_FREQ       = [0x00, 0x00, 0x00, 0x00, 0x03]
CMD_READ_PTT        = [0x00, 0x00, 0x00, 0x00, 0xF7]
CMD_TOGGLE_VFO      = [0x00, 0x00, 0x00, 0x00, 0x81]
CMD_SET_PSK         = [0x0C, 0x00, 0x00, 0x00, 0x07]
CMD_SET_USB         = [0x01, 0x00, 0x00, 0x00, 0x07]
CMD_SET_LSB         = [0x00, 0x00, 0x00, 0x00, 0x07]
CMD_SET_CW          = [0x02, 0x00, 0x00, 0x00, 0x07]
CMD_START_TX        = [0x00, 0x00, 0x00, 0x00, 0x08]
CMD_STOP_TX         = [0x00, 0x00, 0x00, 0x00, 0x88]
CMD_READ_LOCK       = [0x00, 0x00, 0x00, 0x00, 0x80];
CMD_READ_SPLIT      = [0x00, 0x00, 0x00, 0x00, 0x02];
CMD_READ_CLAR       = [0x00, 0x00, 0x00, 0x00, 0x85];

# Default vaiables
QO_frequency        = 0
RX_frequency        = 0
RX_return_frequency = 0
Return_frequency    = 0
RX_frequency_before = 0

# boolean for program flow
setcal              = False

# make a TkInter Window
window = Tk()
window.geometry("870x44")
window.wm_title("FT-817 -- QO-100 Satellite Mode Controller.  @"+SERIAL_PORT+" : "+str(SERIAL_SPEED)+" Bd")

# functions
def set_home ():
    set_mode(CMD_SET_USB)
    set_frequency(Home_frequency)
    update_tx_frequency()
def set_down_50 ():
    set_frequency(QO_frequency-5000)   
def set_up_50 ():
    set_frequency(QO_frequency+5000)  
def set_down_10 ():
    set_frequency(QO_frequency-1000)
def set_up_10 ():
    set_frequency(QO_frequency+1000)   
def set_cwband ():
    set_mode(CMD_SET_CW)
    set_frequency(Cw_band_frequency)
    update_tx_frequency()

def set_bcn ():
    global setcal, RX_return_frequency, RX_frequency
    setcal = True
    RX_return_frequency = RX_frequency
    button_label_7.configure(command= calibrate, highlightbackground="red")
    set_mode(CMD_SET_LSB)
    set_frequency(Beacon_frequency)
       
def calibrate ():
    global setcal, LNB_CALIBRATE, RX_return_frequency, Return_frequency
    # calculate new offset
    LNB_CALIBRATE = LNB_CALIBRATE - (QO_frequency -Beacon_frequency)
    # back to normal operation and last frequency with USB mode
    setcal = False
    button_label_7.configure(command= set_bcn, highlightbackground=window["bg"])
    RX_frequency = (QO_frequency - LNB_OFFSET - LNB_CALIBRATE)/100000
    Return_frequency= (RX_return_frequency*100000) + LNB_OFFSET + LNB_CALIBRATE
    set_mode(CMD_SET_USB)
    set_frequency(Return_frequency)

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
        return True
    else:
        # receiving
        return False
               
def start_tune():
    set_mode(CMD_SET_PSK)
    # open port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)
    # start transmitting and make tune button red
    cmd = CMD_START_TX
    ser.write(cmd)
    time.sleep(SETTLE_TIME)
    ser.close()
    
    button_tune.configure(highlightbackground="red", command= stop_tune)

def stop_tune():
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)
    # stop transmitting 
    cmd = CMD_STOP_TX
    ser.write(cmd)
    time.sleep(SETTLE_TIME)
    
    set_mode(CMD_SET_USB)
     # and update button color 
    button_tune.configure(highlightbackground=window["bg"], command= start_tune)

def read_frequency ():
    # this is the mainloop and controls the serial port
    global setcal
    global QO_frequency, RX_frequency, RX_frequency_before

    # only read and change frequency when in receive
    if read_ptt() is False:
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
        ser.close()
        # check if TX freuency needs update (RX Frequency must be within RX band and not in cal  and will only make button border red)
        if round(RX_frequency,4) != round(RX_frequency_before,4) and RX_frequency > 432.50000 and setcal == False:
            button_update.configure(highlightbackground="red")
        RX_frequency_before = RX_frequency

        # display frequencies and make Sync button boder red 
        button_label_7.config(text=LNB_CALIBRATE )
        QOF = ('{0:.2f}'.format(QO_frequency))
        QOF = QOF[0:2] + "." + QOF[2:5] + "." + QOF[5:8] + "." + QOF[8:10]
        label_4.config(text=QOF)

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

    # write RX frequency and wait processing
    cmd = [int(RX_P1), int(RX_P2), int(RX_P3), int(RX_P4), 1]
    ser.write(cmd)
    time.sleep(SETTLE_TIME)
    ser.close()

def set_mode (mode):
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)

    # write new mode in both VFO
    for _ in range(2):
        cmd = mode
        ser.write(cmd)
        time.sleep(SETTLE_TIME)

        # toggle VFO and wait for processing
        cmd = CMD_TOGGLE_VFO
        ser.write(cmd)
        time.sleep(SETTLE_TIME)

    ser.close()

def update_tx_frequency ():
    global RX_frequency_before
    # open serial port
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_SPEED, stopbits=SERIAL_STOPBITS, timeout=SERIAL_TIMEOUT)

    # read current frequency again
    cmd = CMD_READ_FREQ
    ser.write(cmd)
    resp = ser.read(5)
    resp_bytes = (resp[0], resp[1], resp[2], resp[3])
    frequency = "%02x%02x%02x%02x" % resp_bytes
    RX_frequency = int(frequency)
    QO_frequency = ((RX_frequency + LNB_OFFSET + LNB_CALIBRATE ))
    RX_frequency = (QO_frequency - LNB_OFFSET - LNB_CALIBRATE)/100000

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
    time.sleep(SETTLE_TIME)

    # write TX frequency and wait processing
    cmd = [int(TX_P1), int(TX_P2), int(TX_P3), int(TX_P4), 1]
    ser.write(cmd)
    time.sleep(SETTLE_TIME)

    # toggle VFO again
    cmd = CMD_TOGGLE_VFO
    ser.write(cmd)

    ser.close()

    button_update.configure(highlightbackground="green")
    RX_frequency_before = RX_frequency



# write information in Tkinter Window
# frequency label
label_4 = Label(window, font=('Arial', 30, 'bold'), width=14, fg='blue')
label_4.grid(column=1, row=1)

# function keys
button_label_7 = Button(window, command = set_bcn, width=4, highlightthickness=2)
button_label_7.grid(column=2, row=1)
button_update = Button(window, text = "Up.TX", command = update_tx_frequency, width=4, highlightthickness=2, highlightbackground="red")
button_update.grid(column=3, row=1)
Button(window, text = ".680",command = set_home,    width=4).grid(column=4, row=1)
Button(window, text = ".525",command = set_cwband,  width=4).grid(column=5, row=1)
Button(window, text = "< 50", command = set_down_50, width=4).grid(column=6, row=1)
Button(window, text = "< 10", command = set_down_10, width=4).grid(column=7, row=1)
Button(window, text = "10 >", command = set_up_10,   width=4).grid(column=8, row=1)
Button(window, text = "50 >", command = set_up_50,   width=4).grid(column=9, row=1)

button_tune = Button(window, text = "Tune", command = start_tune, width=4, highlightthickness=2)
button_tune.grid(column=10, row=1)

read_frequency()
window.mainloop()
