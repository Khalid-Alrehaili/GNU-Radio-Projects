# FM Transceiver (Same SDR)

The goal of this project is to transmit an audio file between the transmitter and receiver of the same SDR (with guaranteed clock synchronization) using frequency modulation (FM).

There are two implementations:  
- One for the [ADALM-PLUTO](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html)  
- Another for the [USRP B200 Mini](https://www.ettus.com/all-products/usrp-b200mini/)  

It can also be implemented with any SDR that is compatible with GNU Radio.

**Note:** Please add an audio file in the same folder as the GRC file, named **`audio.wav`**.

# Flowgraph Image
![Flowgraph Image](image.png)
