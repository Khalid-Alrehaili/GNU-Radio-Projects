# AM Transceiver (Between Two SDRs)

This project explores the transmission of an audio file from the transmitter of one SDR to the receiver of another SDR (without clock synchronization).

<strong><span style="color:red">Note: Since the demodulation technique used is not an envelope detector, the transmitter and receiver need to be highly synchronized.</span></strong>

To address this, we transmit a portion of the carrier signal along with the audio. On the receiver side, we detect the carrier peak and use it to re-center the clock, achieving relatively good synchronization between the two SDRs.

**Note:** Provide an audio file inside the same folder as the GRC files for the transmitters with the name **`audio.wav`**
 
# Table of Contents
- [AM Transmitter & Receiver for ADALM-PLUTO SDR](GNU-Radio-Files_ADALM-PLUTO)
- [AM Transmitter & Receiver for USRP B200 Mini](GNU-Radio-Files_USRP-B200mini)

# Flowgraph Images

1. ## ADALM-PLUTO AM Transmitter  
   ![ADALM-PLUTO AM Transmitter](Images/AM-Transmitter_ADALM-PLUTO.png)

2. ## ADALM-PLUTO AM Receiver  
   ![ADALM-PLUTO AM Receiver](Images/AM-Receiver_ADALM-PLUTO.png)

3. ## USRP B200 Mini AM Transmitter  
   ![USRP B200 Mini AM Transmitter](Images/AM-Transmitter_USRP-B200mini.png)

4. ## USRP B200 Mini AM Receiver  
   ![USRP B200 Mini AM Receiver](Images/AM-Receiver_USRP-B200mini.png)
