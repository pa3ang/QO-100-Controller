# QO-100-Controller
QO-100 Controller for FT817/818 Transceiver

V2.1
Reworked version with new geometric of the presentation window.
Auto update cancelled, now only manuap update by clicking the button on the window Up.TX
Added possibility to use 2 meter as downlink (removed some validation)
Changed the name of the file

V1.2
changed split to button autoTX. Same function but now explicit to tell program to auto update TX frequency
added button to jump direct to CW band frequency 

V1.1
added time delay on TX detect back to RX
added dynamic TX Update after 4 seconds no adjust of RX frequency
added split button to prevent above
changed BCN fucntion will return back to tuned RX frequency in stead of new calculated QO_frequency

V1.0 
This Python program does some usefull control functions for working the QO_100 transponder using a Yaesu FT-817 or 
lookalike transceiver. The program assumes you are using an LNB for 10 GHz reception with downconverts to 70cm and is 
TCXO stabilized. The uplink is generated from either 144 MHz or 432 MHz. 

The development is made with an FT-818 on 70cm and the uplink is done with an transvertor having an IF frequency of 
1968 Mhz, so 432.180 => 2400.180 MHz. The downlink LNB uses 10057 MHz, thus 10489.680 becomes 432.680 MHz. Because 
of the nature of Frequency Cristals there will be some deviation and my LNB IF has about 21 KHz offset. (10056.97900)

The uplink is TXCO controlled as well and with the TXCO controlled FT-818 the frequency is very accurate.

The program has variables to set the different frequencies.

The FT-818 must run in split mode so bot VFO A and B are used.

The main functions are:
1. read receive frequency and calculate the QO-100 transponder frequency.
2. ability to calibrate the calculation against the middle (PSK) Beacon using USB/LSB adjustment.
3. ability to calibrate against a known signal.
4. set the TX frequency based on the calculated QO-100 frequency.
5. change mode of operation either USB or CW.
6. store and recall memory frequency.
7. quick access to home frequency.
8. tune function. Puts FT818 in PSK tx mode with constant carrier.

By nature of Python, the program can run on any platform, but the GUI geometry has been adjusted for using the 
program on a RPi with 7" screen.


