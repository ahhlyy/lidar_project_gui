from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
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

    def lidarui(self):
        # 窗口配置
        self.window.title("北醒雷达串口调试助手")
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        print(width, height)
        # {}x{} 窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.window.geometry('{}x{}+{}+{}'.format(400, 700, width // 3, height // 15))
        self.window.resizable(False, False) # 不允许调整窗口大小
        
        ########################################################################
        ################### 串口选择group_serial_select ########################
        ########################################################################
        group_serial_select = Frame(self.window)
        group_serial_select.grid(row=0, padx=5, pady=5, sticky=W)
        # 串口设置标签serial_label
        serial_label = Label(group_serial_select, text="选择串口", justify='left', relief='flat')
        serial_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.serial_combobox = ttk.Combobox(group_serial_select, width=20)
        self.serial_combobox['value'] = lidar_serial.getSerialPort()
        self.serial_combobox.grid(row=0, column=1, padx=35, pady=10)        

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew", padx=10, pady=0)

        ########################################################################
        ################## 设备测距group_device_distance #######################
        ########################################################################
        # 设备测距group_device_distance
        group_device_distance = LabelFrame(self.window, text="设备测距", relief='flat')
        group_device_distance.grid(row=2, padx=10, pady=10, sticky=W)
        # 波特率标签selectbaud_label
        selectbaud_label = Label(group_device_distance, text="选择波特率", justify='left', relief='flat')
        selectbaud_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.selectbaud_combobox = ttk.Combobox(group_device_distance, width=20, justify='left')
        self.selectbaud_combobox['value'] = ("9600", "19200", "38400", "57600", "115200")
        self.selectbaud_combobox.grid(row=1, column=1, padx=0, pady=0, sticky=W)
        # id标签selectid_label
        selectid_label = Label(group_device_distance, text="选择id(1-255)")
        selectid_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.SlaveID_var = tk.IntVar()
        selectid_input = Entry(group_device_distance, width=23, textvariable=self.SlaveID_var, justify='left')
        selectid_input.delete(0)
        selectid_input.grid(row=2, column=1, padx=0, pady=10, sticky=W)
        # 连接按钮self.serial_btn
        self.serial_btn = Button(group_device_distance, text="连接", width=8, command=self.connectSerialPort)
        self.serial_btn.grid(row=3, column=2, padx=35, pady=0, sticky=E)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=3, column=0, sticky="ew", padx=10, pady=0)

        ########################################################################
        ################### 测距显示group_distance_display ######################
        ########################################################################
        # 测距显示group_distance_display
        group_distance_display = Frame(self.window, relief='groove')
        group_distance_display.grid(row=4, padx=10, pady=5, sticky=W)
        # 距离标签distance_label
        distance_label = Label(group_distance_display, text="距离(cm):")
        distance_label.grid(row=0, column=0, padx=5, pady=0, sticky=W)
        # 强度标签strength_label
        strength_label = Label(group_distance_display, text="强度:")
        strength_label.grid(row=0, column=1, padx=140, pady=0, sticky=W)
        # 距离值显示标签self.displaydis_label
        self.displaydis_label = Label(group_distance_display, text="   ", relief='flat')
        self.displaydis_label.grid(row=1, column=0)
        # 强度值显示标签self.displaystr_label
        self.displaystr_label = Label(group_distance_display, text="   ", relief='flat')
        self.displaystr_label.grid(row=1, column=1)
        #绘图按钮self.paint_btn
        self.paint_btn = Button(group_distance_display, text="制图", width=8, command=self.paint)
        self.paint_btn.grid(row=2, column=1, padx=10, pady=10, sticky=E)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=5, column=0, sticky="ew", padx=10, pady=0)

        ########################################################################
        ################### 雷达配置group_lidar_configure ######################
        ########################################################################
        # 雷达配置group_lidar_configure
        group_lidar_configure = LabelFrame(self.window, text="雷达配置", relief='flat')
        group_lidar_configure.grid(row=6, padx=10, pady=10, sticky=W)
        # 修改波特率标签modifybaud_label
        modifybaud_label = Label(group_lidar_configure, text="修改波特率", justify='left', relief='flat')
        modifybaud_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.modifybaud_combobox = ttk.Combobox(group_lidar_configure, width=20, justify='left')
        self.modifybaud_combobox['value'] = ("9600", "19200", "38400", "57600", "115200")
        self.modifybaud_combobox.grid(row=0, column=1, padx=0, pady=0, sticky=W)
        # 修改波特率设置按钮modifybaud_btn
        modifybaud_btn = Button(group_lidar_configure, text="设置", width=8, command=self.modify_baud, justify='left')
        modifybaud_btn.grid(row=0, column=2, padx=35, pady=0)
        # 修改id标签modifyid_label
        modifyid_label = Label(group_lidar_configure, text="修改id(1-255)")
        modifyid_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.modifyid_var = tk.IntVar()
        modifyid_input = Entry(group_lidar_configure, width=23, textvariable=self.modifyid_var, justify='left')
        modifyid_input.delete(0)
        modifyid_input.grid(row=1, column=1, padx=0, pady=10, sticky=W)
        # 修改id设置按钮modifyid_btn
        modifyid_btn = Button(group_lidar_configure, text="设置", width=8, command=self.modify_id, justify='left')
        modifyid_btn.grid(row=1, column=2, padx=35, pady=0)
        # 恢复出厂标签restore_label
        restore_label = Label(group_lidar_configure, text="恢复出厂")
        restore_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        empty_label = Label(group_lidar_configure, text="---", justify='center')
        empty_label.grid(row=2, column=1, padx=10, pady=10)
        # 恢复出厂设置按钮restore_btn
        restore_btn = Button(group_lidar_configure, text="设置", width=8, command=self.restore_factory, justify='left')
        restore_btn.grid(row=2, column=2, padx=35, pady=0)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=7, column=0, sticky="ew", padx=10, pady=0)

        ########################################################################
        ##################### 设备查找group_device_find #########################
        ########################################################################
        # 设备查找group_device_find
        group_device_find = LabelFrame(self.window, text="设备查找", relief='flat')
        group_device_find.grid(row=8, padx=10, pady=10, sticky=W)
        # 波特率标签findbaud_label
        findbaud_label = Label(group_device_find, text="当前波特率为:")
        findbaud_label.grid(row=0, column=0, padx=15, pady=0, sticky=W)
        # id标签findid_label
        findid_label = Label(group_device_find, text="当前 id 为(DEC):")
        findid_label.grid(row=0, column=1, padx=100, pady=0, sticky=W)
        # 波特率显示标签self.displaybaud_label
        self.displaybaud_label = Label(group_device_find, text="  ")
        self.displaybaud_label.grid(row=1, column=0)
        # id显示标签self.displayid_label
        self.displayid_label = Label(group_device_find, text="  ")
        self.displayid_label.grid(row=1, column=1)
        # 开始查找按钮self.findstart_btn
        self.findstart_btn = Button(group_device_find,text="开始", width=8, command=self.find_lidar)
        self.findstart_btn.grid(row=2, column=1, padx=40, pady=10, sticky=E)

        # 添加一条分割线
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=9, column=0, sticky="ew", padx=10, pady=0)

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

    def connectSerialPort(self):
        # global master
        selected_port = self.serial_combobox.get()
        BAUDRATE = self.selectbaud_combobox.get()
        SlaveID = self.SlaveID_var.get()
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
            master.set_timeout(0.05)  # 50ms
            master.set_verbose(True)
            
            read = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                                  quantity_of_x=2)
            print("成功连接到从站！")
            print("寄存器0的值为:", read)
            print("距离:", read[0], "强度：", read[1])
            self.displaydis_label.config(text=read[0])
            self.displaystr_label.config(text=read[1])
            master.close()
        except Exception as e:
            print("连接失败：", e)
        
        self.serial_btn.config(activebackground="yellow")

    def find_lidar(self):
        print("开始扫描当前雷达站号和波特率,全部扫描结束时间为90S左右")
        print("雷达站号范围:1-255,波特率:9600、19200、38400、57600、115200")
        print("----------------------------------------------------------")
        # 设备查找时弹出新的提示窗口
        new_window = tk.Toplevel(self.window)
        new_window.title("提示")
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        new_window.geometry('{}x{}+{}+{}'.format(400, 100, width // 3, height // 3))
        new_window_label1 = Label(new_window, text="扫描中,全部扫描结束时间为90S左右")
        new_window_label1.grid(row=0, column=0, padx=90, pady=15)
        new_window_label2 = Label(new_window, text="请等待......")
        new_window_label2.grid(row=1, column=0, padx=90, pady=0)
        new_window.resizable(False, False) # 不允许调整窗口大小
        # 设备轮询并记录波特率和id值
        baudrate = 0
        id = 0
        begin_time = time.time()
        flag = False
        for x in range(5):
            for y in range(1, 5):
                z = self.mod_lidar(Baudrate[x], y)
                baudrate = Baudrate[x]
                id = y
                new_window.update()

                if z == '正常':
                    print("测距成功")
                    print("当前波特率：", Baudrate[x], "当前站号：", y)
                    baudrate = Baudrate[x]
                    id = y
                    self.displaybaud_label.config(text=baudrate)
                    self.displayid_label.config(text=id)
                    flag = True
                    break
            if flag:
                break
        new_window.destroy()

        end_time = time.time()
        run_time = end_time - begin_time
        print("查询运行时间：", run_time, "\n")

        return baudrate, id

    def mod_lidar(self, BAUDRATE, SlaveID):
        red = []
        alarm = ""
        selected_port = self.serial_combobox.get()
        master = self.establish_serial(selected_port, BAUDRATE)
        master.open()
        master.set_timeout(0.05)
        master.set_verbose(True)
        try:
            # 读保持寄存器
            red = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                                quantity_of_x=2)  # 这里可以修改需要读取的功能码
            master.set_timeout(0.05)
            print(red)
            alarm = "正常"

            return alarm

        except Exception as exc:
            alarm = (str(exc))
        master.close()

        return red, alarm

    def establish_serial(master, selected_port, BAUDRATE):
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=selected_port,
                        baudrate=BAUDRATE,
                        bytesize=8,
                        parity='N',
                        stopbits=1,
                        timeout=0.05))
        master.set_timeout(0.05)  # 50ms
        master.set_verbose(True)

        return master

    def modify_baud(self):
        red = []
        alarm = ""
        selected_port = self.serial_combobox.get()
        BAUDRATE = self.selectbaud_combobox.get()
        New_BAUDRATE = self.modifybaud_combobox.get()
        SlaveID = self.SlaveID_var.get()

        master = self.establish_serial(selected_port, BAUDRATE)
        master.open()
        master.set_timeout(0.5)
        try:
            # 将十进制转换为十六进制，并用0填充成8位
            New_BAUDRATE_hex = hex(int(New_BAUDRATE))[2:].zfill(8)
            # 将十六进制字符串转换为两个字节的波特率高位和波特率低位
            New_BAUDRATE_H = hex(int(New_BAUDRATE_hex[:4], 16))
            NH = int(New_BAUDRATE_H, 16)
            New_BAUDRATE_L = hex(int(New_BAUDRATE_hex[4:], 16))
            NL = int(New_BAUDRATE_L, 16)
            # 写保持寄存器
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x83,
                                output_value=NH)  # 修改波特率高字节指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x84,
                             output_value=NL)  # 修改波特率低字节指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x80,
                             output_value=0)  # 保存设备指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x81,
                             output_value=1)  # 重启设备指令
            master.set_timeout(0.5)
            # 读保持寄存器
            read = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                                  quantity_of_x=2)
            print("成功连接到从站！")
            print("寄存器0的值为:", read)
            print("距离:", read[0], "强度：", read[1])
            self.displaydis_label.config(text=read[0])
            self.displaystr_label.config(text=read[1])

            alarm = "正常"

            return alarm

        except Exception as exc:
            alarm = (str(exc))
        master.close()

        return red, alarm        
    
    def modify_id(self):
        red = []
        alarm = ""
        selected_port = self.serial_combobox.get()
        BAUDRATE = self.selectbaud_combobox.get()
        SlaveID = self.SlaveID_var.get()
        New_SlaveID = self.modifyid_var.get()
        
        master = self.establish_serial(selected_port, BAUDRATE)
        master.open()
        master.set_timeout(0.5)
        try:
            # 写保持寄存器
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x85,
                                output_value=New_SlaveID)  # 修改id指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x80,
                             output_value=0)  # 保存设备指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x81,
                             output_value=1)  # 重启设备指令
            master.set_timeout(0.5)
            # 读保持寄存器
            read = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                                  quantity_of_x=2)
            print("成功连接到从站！")
            print("寄存器0的值为:", read)
            print("距离:", read[0], "强度：", read[1])
            self.displaydis_label.config(text=read[0])
            self.displaystr_label.config(text=read[1])

            alarm = "正常"

            return alarm

        except Exception as exc:
            alarm = (str(exc))

        master.close()

        return red, alarm

    def restore_factory(self):
        red = []
        alarm = ""
        selected_port = self.serial_combobox.get()
        BAUDRATE = self.selectbaud_combobox.get()
        SlaveID = self.SlaveID_var.get()
        master = self.establish_serial(selected_port, BAUDRATE)
        master.open()
        master.set_timeout(0.5)
        try:
            # 写保持寄存器
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x89,
                                output_value=0)  # 恢复出厂指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x80,
                             output_value=0)  # 保存设备指令
            master.set_timeout(0.5)
            red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x81,
                             output_value=1)  # 重启设备指令
            master.set_timeout(0.5)

            alarm = "正常"

            return alarm

        except Exception as exc:
            alarm = (str(exc))

        master.close()

        return red, alarm

    def save_reset_cmd(self):
        print('Saving reset cmd...')

    def paint(self):
        print('Paint...')

if __name__ == "__main__":
    mySerial = lidar_serial()
    mySerial.lidarui()