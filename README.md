## Remote control console for Power amplifier based on R-140 (ПЖ-3, ПЖ-6)

You can read about this device here - https://ra0sms.com/remote-r140/

### Installation

#### Linux

```bash
sudo apt install git pip python
cd ~
git clone https://github.com/ra0sms/R140_remote_control.git
cd R140_remote_control
python ./main.py
```

You might need some python packet

```bash
pip install pyqt5 
```

#### Windows

Copy `main_desigh.ui`, `logo.png` and `R140_remote_control.exe` to your PC. Enjoy!

#### Raspberry py

You need install some python packets
```bash
sudo apt install python3-serial python3-pyqt5
sudo apt install python3-pyqt5.qtserialport
```
