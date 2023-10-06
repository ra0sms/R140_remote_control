import PyQt5.QtWidgets
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer, QEvent
from PyQt5.QtWidgets import QMessageBox, QWidget


app = QtWidgets.QApplication([])
ui = uic.loadUi("main_design.ui")
ui.setWindowTitle("R-140 Remote Control")
ui.setWindowIcon(QtGui.QIcon("logo.png"))


serial = QSerialPort()
timer = QTimer()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)


TIME_INTERVAL = 100000    # msec between button ON enabled
all_out_off = "AM10000000000000000\r"
check_out_list = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
header = "AM1"
is_push_on_btn = 0


def set_output():
    """Send to COM port data in the format AM10000000000000000\r"""
    out_str = (header + ("".join(check_out_list[0:11])) + "0" + check_out_list[11] + "00" + check_out_list[12] + "\r")
    serial.write(out_str.encode())


def set_all_buttons_off():
    ui.onB.setStyleSheet("background-color : window")
    ui.stbB.setStyleSheet("background-color : gray window")
    ui.fanB.setStyleSheet("background-color : gray window")
    ui.offB.setStyleSheet("background-color : gray window")
    ui.firstB.setStyleSheet("background-color : gray window")
    ui.secondB.setStyleSheet("background-color : gray window")
    ui.thirdB.setStyleSheet("background-color : gray window")
    ui.fourthB.setStyleSheet("background-color : gray window")
    ui.fifthB.setStyleSheet("background-color : gray window")
    ui.sixthB.setStyleSheet("background-color : gray window")
    ui.seventhB.setStyleSheet("background-color : gray window")
    ui.eighthB.setStyleSheet("background-color : gray window")
    ui.stbOnB.setStyleSheet("background-color : gray window")
    ui.stbOffB.setStyleSheet("background-color : gray window")
    ui.OpenB.setStyleSheet("background-color : gray window")
    ui.startB.setStyleSheet("background-color : gray window")
    for k in range(len(check_out_list)):
        check_out_list[k] = '0'


def show_warning_messagebox():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("COM port is not opened!")
    msg.setWindowTitle("Warning")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()


def on_read():
    if not serial.canReadLine():
        return
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')


def on_open():
    if serial.isOpen():
        serial.write(all_out_off.encode())
        serial.waitForBytesWritten(10)
        ui.OpenB.setText("OPEN")
        ui.labelCOM.setText("COM port closed")
        set_all_buttons_off()
        ui.onB.setDisabled(True)
        serial.close()
    else:
        serial.setPortName(ui.comL.currentText())
        serial.open(QIODevice.ReadWrite)
        ui.labelCOM.setText("COM port opened")
        ui.OpenB.setText("CLOSE")
        ui.onB.setDisabled(True)
        set_all_buttons_off()


def on_off():
    if serial.isOpen():
        serial.write(all_out_off.encode())
        serial.waitForBytesWritten(10)
        set_all_buttons_off()
        ui.fanB.setStyleSheet("background-color : gray window")
        ui.stbB.setStyleSheet("background-color : gray window")
        ui.onB.setStyleSheet("background-color : gray window")
        ui.offB.setStyleSheet("background-color : gray window")
        ui.onB.setDisabled(True)
    else:
        show_warning_messagebox()


def on_fan():
    global is_push_on_btn
    if serial.isOpen():
        check_out_list[8] = "1"
        check_out_list[9] = "0"
        check_out_list[10] = "0"
        ui.fanB.setStyleSheet("background-color : red")
        ui.stbB.setStyleSheet("background-color : gray window")
        ui.onB.setStyleSheet("background-color : gray window")
        ui.offB.setStyleSheet("background-color : gray window")
        ui.stbB.setEnabled(True)
        ui.onB.setDisabled(True)
        set_output()
        is_push_on_btn = 0
        ui.offB.setEnabled(True)
    else:
        show_warning_messagebox()


def set_on_enabled():
    ui.onB.setEnabled(True)
    ui.fanB.setEnabled(True)
    ui.stbB.setEnabled(True)


def on_stb():
    global is_push_on_btn
    if serial.isOpen():
        check_out_list[8] = "0"
        check_out_list[9] = "1"
        check_out_list[10] = "0"
        ui.stbB.setStyleSheet("background-color : red")
        ui.onB.setStyleSheet("background-color : gray window")
        ui.fanB.setStyleSheet("background-color : gray window")
        ui.offB.setStyleSheet("background-color : gray window")
        set_output()
        if is_push_on_btn == 0:
            timer.singleShot(TIME_INTERVAL, set_on_enabled)
            ui.stbB.setDisabled(True)
            ui.offB.setDisabled(True)
            ui.onB.setDisabled(True)
        else:
            ui.fanB.setEnabled(True)

    else:
        show_warning_messagebox()


def on_on():
    global is_push_on_btn
    if serial.isOpen():
        check_out_list[8] = "0"
        check_out_list[9] = "0"
        check_out_list[10] = "1"
        ui.onB.setStyleSheet("background-color : red")
        ui.stbB.setStyleSheet("background-color : gray window")
        ui.fanB.setStyleSheet("background-color : gray window")
        ui.offB.setStyleSheet("background-color : gray window")
        set_output()
        is_push_on_btn = 1
        ui.fanB.setDisabled(True)
    else:
        show_warning_messagebox()


def on_firstB():
    if serial.isOpen():
        check_out_list[0] = "1"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : red")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


def on_secondB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "1"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : red")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()

def on_thirdB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "1"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : red")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()

def on_fourthB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "1"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : red")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


def on_fifthB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "1"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : red")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


def on_sixthB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "1"
        check_out_list[6] = "0"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : red")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


def on_seventhB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "1"
        check_out_list[7] = "0"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : red")
        ui.eighthB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


def on_eightB():
    if serial.isOpen():
        check_out_list[0] = "0"
        check_out_list[1] = "0"
        check_out_list[2] = "0"
        check_out_list[3] = "0"
        check_out_list[4] = "0"
        check_out_list[5] = "0"
        check_out_list[6] = "0"
        check_out_list[7] = "1"
        ui.firstB.setStyleSheet("background-color : gray window")
        ui.secondB.setStyleSheet("background-color : gray window")
        ui.thirdB.setStyleSheet("background-color : gray window")
        ui.fourthB.setStyleSheet("background-color : gray window")
        ui.fifthB.setStyleSheet("background-color : gray window")
        ui.sixthB.setStyleSheet("background-color : gray window")
        ui.seventhB.setStyleSheet("background-color : gray window")
        ui.eighthB.setStyleSheet("background-color : red")
        set_output()
    else:
        show_warning_messagebox()


def reset_start():
    ui.startB.setStyleSheet("background-color : gray window")
    check_out_list[12] = "0"
    set_output()


def on_startB():
    if serial.isOpen():
        check_out_list[12] = "1"
        ui.startB.setStyleSheet("background-color : red")
        set_output()
        timer.singleShot(800, reset_start)
    else:
        show_warning_messagebox()


def on_stbOnB():
    if serial.isOpen():
        check_out_list[11] = "1"
        ui.stbOnB.setStyleSheet("background-color : red")
        set_output()
    else:
        show_warning_messagebox()


def on_stbOffB():
    if serial.isOpen():
        check_out_list[11] = "0"
        ui.stbOnB.setStyleSheet("background-color : gray window")
        set_output()
    else:
        show_warning_messagebox()


set_output()
serial.readyRead.connect(on_read)   # reading from COM port routine
ui.onB.setDisabled(True)            # disabled button at start
ui.stbB.setDisabled(True)           # disabled button at start
ui.OpenB.clicked.connect(on_open)
ui.offB.clicked.connect(on_off)
ui.fanB.clicked.connect(on_fan)
ui.stbB.clicked.connect(on_stb)
ui.onB.clicked.connect(on_on)
ui.firstB.clicked.connect(on_firstB)
ui.secondB.clicked.connect(on_secondB)
ui.thirdB.clicked.connect(on_thirdB)
ui.fourthB.clicked.connect(on_fourthB)
ui.fifthB.clicked.connect(on_fifthB)
ui.sixthB.clicked.connect(on_sixthB)
ui.seventhB.clicked.connect(on_seventhB)
ui.eighthB.clicked.connect(on_eightB)
ui.startB.clicked.connect(on_startB)
ui.stbOnB.clicked.connect(on_stbOnB)
ui.stbOffB.clicked.connect(on_stbOffB)


ui.show()
app.exec()
