## Remote control console for Power amplifier based on R-140 (ПЖ-3, ПЖ-6)

You can read about this device here - https://ra0sms.com/remote-r140/

### Installation

#### Linux

```bash
sudo apt install git pip python
pip install pyqt5
sudo usermod -a -G tty $USER
sudo usermod -a -G dialout $USER
cd ~
git clone https://github.com/ra0sms/R140_remote_control.git
cd R140_remote_control
python ./main.py
```

#### Windows

Copy `main_desigh.ui`, `logo.png` and `R140_remote_control.exe` to your PC. Enjoy!

#### Raspberry py

You need to install some python packets
```bash
sudo apt install python3-serial python3-pyqt5
sudo apt install python3-pyqt5.qtserialport
sudo usermod -a -G tty pi
sudo usermod -a -G dialout pi
```
