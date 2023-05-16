from tkinter import *
import tkinter as tk
from tkinter import ttk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import serial.tools.list_ports


# 扫描可用串口
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
print("可用串口列表：")
for p in ports:
    print(p.device)

# 选择串口并建立Modbus从站
def connect():
    port = port_var.get()
    baudrate = baudrate_var.get()
    slave_id = slave_id_var.get()
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)
        #master.set_slave(slave_id)
        print("成功连接到从站！")
        # 读取Modbus寄存器0的值并打印出来
        value = master.execute(slave_id, cst.READ_HOLDING_REGISTERS, 0, 2)
        print("寄存器0的值为：", value)
    except Exception as e:
        print("连接失败：", e)

# 创建GUI界面
root = tk.Tk()
root.title("北醒雷达串口调试助手")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('{}x{}+{}+{}'.format(400, 600, width // 3, height // 7))
root.resizable(False, False)

# 串口选择下拉列表
tk.Label(root, text="选择串口：").grid(row=0, column=0)
port_var = tk.StringVar()
port_combobox = ttk.Combobox(root, textvariable=port_var, state="readonly")
port_combobox.grid(row=0, column=1)
port_combobox["values"] = tuple(p.device for p in ports)
port_combobox.current(0)

# 波特率选择下拉列表
tk.Label(root, text="选择波特率：").grid(row=1, column=0)
baudrate_var = tk.IntVar()
baudrate_combobox = ttk.Combobox(root, textvariable=baudrate_var, state="readonly")
baudrate_combobox.grid(row=1, column=1)
baudrate_combobox["values"] = (9600, 19200, 38400, 57600, 115200)
baudrate_combobox.current(0)

# 从站地址输入框
tk.Label(root, text="从站地址：").grid(row=2, column=0)
slave_id_var = tk.IntVar()
slave_id_entry = tk.Entry(root, textvariable=slave_id_var)
slave_id_entry.grid(row=2, column=1)
slave_id_entry.insert(0, "1")

# 连接按钮
tk.Button(root, text="连接", command=connect).grid(row=3, column=0, columnspan=2)

root.mainloop()