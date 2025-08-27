# FM Transceiver (Between Two SDRs)

This project explores the transmission of an audio file from one SDR's transmitter to another SDR's receiver (with no synchronization between SDRs' clocks).

The implementation has been done with two SDRs:  
1. [ADALM-PLUTO](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html) — GRC files are found in [GNU-Radio-Files_ADALM-PLUTO](GNU-Radio-Files_ADALM-PLUTO)  
2. [USRP B200 Mini](https://www.ettus.com/all-products/usrp-b200mini/) — GRC files are found in [GNU-Radio-Files_USRP-B200mini](GNU-Radio-Files_USRP-B200mini)  

**Note:** Please provide an audio file in the same folder as the transmitter’s GRC file, named **`audio.wav`**.  

# Flowgraph Images

1. ## ADALM-PLUTO FM Transmitter  
   ![ADALM-PLUTO FM Transmitter](Images/ADALM-PLUTO-FM-Transmitter.png)

2. ## ADALM-PLUTO FM Receiver  
   ![ADALM-PLUTO FM Receiver](Images/ADALM-PLUTO-FM-Receiver.png)

3. ## USRP B200 Mini FM Transmitter  
   ![USRP B200 Mini FM Transmitter](Images/USRP-B200mini-FM-Transmitter.png)

4. ## USRP B200 Mini FM Receiver  
   ![USRP B200 Mini FM Receiver](Images/USRP-B200mini-FM-Receiver.png)
