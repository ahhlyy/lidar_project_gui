from tkinter import *
from tkinter import ttk
import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time
import numpy as np
import sys
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

Baudrate = [9600, 115200, 19200, 38400, 57600]


class lidar_serial:
    def __init__(self):
        self.window = Tk()  # 实例化出一个父窗口
        self.com = serial.Serial()
        self.master = serial.Serial()

    def lidarui(self):
        # 窗口配置
        self.window.title("北醒雷达串口调试助手")
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        print(width, height)
        # {}x{} 窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.window.geometry('{}x{}+{}+{}'.format(400, 600, width // 3, height // 7))
        self.window.resizable(False, False) # 不允许调整窗口大小
        
        # 串口设置serial_set
        group_serial_set = LabelFrame(self.window, text="串口选择", relief='flat')
        group_serial_set.grid(row=0, padx=10, pady=10)

        serial_label = Label(group_serial_set, text="端口")
        serial_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.serial_combobox = ttk.Combobox(group_serial_set, width=30)
        self.serial_combobox['value'] = lidar_serial.getSerialPort()
        self.serial_combobox.grid(row=0, column=1, padx=0, pady=0)

        self.serial_btn = Button(group_serial_set, text="连接", width=8, command=self.connectSerialPort)
        self.serial_btn.grid(row=0, column=2, padx=10, pady=0, sticky=E)
        
        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew", padx=10, pady=0)

        # 测距显示distance_display
        group_distance_display = Frame(self.window, relief='groove')
        group_distance_display.grid(row=2, padx=10, pady=5)

        distance_label = Label(group_distance_display, text="距离(cm):")
        distance_label.grid(row=0, column=0, padx=0, pady=0, sticky=W)

        strength_label = Label(group_distance_display, text="强度:")
        strength_label.grid(row=0, column=1, padx=140, pady=0, sticky=E)

        self.displaydis_label = Label(group_distance_display, text="   ", relief='flat')
        self.displaydis_label.grid(row=1, column=0)
   
        self.displaystr_label = Label(group_distance_display, text="   ", relief='flat')
        self.displaystr_label.grid(row=1, column=1)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=3, column=0, sticky="ew", padx=10, pady=0)

        # 菜单menu
        group_menu = LabelFrame(self.window, text="菜单", relief='flat')
        group_menu.grid(row=4, padx=10, pady=10, sticky=W)
        
        var = IntVar()
        rd1 = Radiobutton(group_menu,text="设备查找",variable=var,value=0,command=self.find_lidar)
        rd1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        rd2 = Radiobutton(group_menu,text="设备测距",variable=var,value=1,command=self.distance_lidar)
        rd2.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        menu_btn = Button(group_menu, text="确定", width=8, justify='right')
        menu_btn.grid(row=2, column=1, padx=10, pady=0)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=5, column=0, sticky="ew", padx=10, pady=0)
        
        # 雷达配置lidar_configure
        group_lidar_configure = LabelFrame(self.window, text="雷达配置", relief='flat')
        group_lidar_configure.grid(row=6, padx=10, pady=10, sticky=W)
        # 波特率
        baud_label = Label(group_lidar_configure, text="修改波特率", justify='left', relief='flat')
        baud_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.baud_combobox = ttk.Combobox(group_lidar_configure, width=20, justify='left')
        self.baud_combobox['value'] = ("9600", "19200", "38400", "57600", "115200")
        self.baud_combobox.grid(row=0, column=1, padx=0, pady=0, sticky=W)
        
        baud_btn = Button(group_lidar_configure, text="设置", width=8, command=self.modify_baud, justify='left')
        baud_btn.grid(row=0, column=2, padx=20, pady=0)
        # id
        id_label = Label(group_lidar_configure, text="修改id(1-255)")
        id_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        id_input = Entry(group_lidar_configure, width=23, justify='left')
        id_input.grid(row=1, column=1, padx=0, pady=10, sticky=W)

        id_btn = Button(group_lidar_configure, text="设置", width=8, command=self.modify_id, justify='left')
        id_btn.grid(row=1, column=2, padx=20, pady=0)

        # 恢复出厂
        restore_label = Label(group_lidar_configure, text="恢复出厂")
        restore_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        empty_label = Label(group_lidar_configure, text="---", justify='center')
        empty_label.grid(row=2, column=1, padx=10, pady=10)

        restore_btn = Button(group_lidar_configure, text="设置", width=8, command=self.restore_factory, justify='left')
        restore_btn.grid(row=2, column=2, padx=20, pady=0)
        '''
        var = IntVar()
        rd1 = Radiobutton(group_lidar_configure,text="修改波特率",variable=var,value=0,command=self.modify_baud)
        rd1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        self.baud_combobox = ttk.Combobox(group_lidar_configure, width=30)
        self.baud_combobox['value'] = ("9600", "19200", "38400", "57600", "115200")
        self.baud_combobox.grid(row=0, column=1, padx=0, pady=0)

        rd2 = Radiobutton(group_lidar_configure,text="修改id",variable=var,value=1,command=self.modify_id)
        rd2.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        id_input = Entry(group_lidar_configure, width=33)
        id_input.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        rd3 = Radiobutton(group_lidar_configure,text="恢复出厂",variable=var,value=2,command=self.restore_factory)
        rd3.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        '''

        #configure_btn = Button(group_lidar_configure, text="完成", width=8, command=self.save_reset_cmd)
        #configure_btn.grid(row=3, column=2, padx=10, pady=0, sticky=E)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=7, column=0, sticky="ew", padx=10, pady=0)

        self.window.mainloop()

    def getSerialPort():
        port = []
        portList = list(serial.tools.list_ports.comports())
        # print(portList)

        if len(portList) == 0:
            print("--- 无串口 ---")
            port.append('None')
        else:
            for comport in portList:
                # print(list(comport)[0])
                # print(list(comport)[1])
                port.append(list(comport)[0])
                pass
        return port

    def hit1(self):
        if self.com.is_open():
            print("")


    def connectSerialPort(self):
        #ser = self.getSerialPort()
        global master
        selected_port = self.serial_combobox.get()
        print(selected_port)
        BAUDRATE = 115200
        read = []
        try:
            master = modbus_rtu.RtuMaster(
                serial.Serial(port=selected_port,
                            baudrate=BAUDRATE,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=0.5))
            master.open()
            master.set_timeout(5.0)  # 50ms
            master.set_verbose(True)
            print("成功连接到从站！")
            read = master.execute(slave=1, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)
            print("寄存器0的值为:", read)
            print("距离:", read[0], "强度：", read[1])
            self.displaydis_label.config(text=read[0])
            self.displaystr_label.config(text=read[1])
            master.close()
        except Exception as e:
            print("连接失败：", e)
        #master_thread = threading.Thread(master)
        #master_thread.start()
        
        #ser = serial.Serial(self.baud_combobox.get(), 9600) # 串口连接配置
        self.serial_btn.config(activebackground="yellow")
        # 连接成功后的操作
        print("Serial port connected successfully!")
    
    def disconnect(self):
        global ser
        ser.close()  # 断开串口连接
        self.serial_btn.config(bg="SystemButtonFace")  # 设置按钮背景为默认颜色

    def find_lidar(self):
        print('Finding lidar...')

    def distance_lidar(self):
        print('Distance')

    def modify_baud(self):
        print('Modifying baud...')
    
    def modify_id(self):
        print('Modifying id...')

    def restore_factory(self):
        print('Restoring factory...')

    def save_reset_cmd(self):
        print('Saving reset cmd...')

if __name__ == "__main__":
    mySerial = lidar_serial()
    mySerial.lidarui()