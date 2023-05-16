import tkinter as tk
import serial
import modbus_tk
import modbus_tk.defines as cst
import serial.tools.list_ports
from modbus_tk import modbus_rtu

def scan_serial_ports():
    """扫描可用的串口并返回列表"""
    ports = list(serial.tools.list_ports.comports())
    result = []
    for port in ports:
        result.append(port.device)
    return result

def select_port():
    """从下拉列表中选择串口"""
    port = port_var.get()
    if port:
        # 建立Modbus从站
        master = modbus_rtu.RtuMaster(serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)
        # 读取Modbus数据
        try:
            response = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1)
            print("Modbus response:", response)
        except Exception as exc:
            print("Modbus error:", exc)
    else:
        print("Please select a port")

# 创建主窗口
root = tk.Tk()
root.title("Modbus Scanner")

# 创建下拉列表
port_var = tk.StringVar()
port_list = scan_serial_ports()
port_menu = tk.OptionMenu(root, port_var, *port_list)
port_menu.pack()

# 创建按钮
btn_scan = tk.Button(root, text="Scan", command=select_port)
btn_scan.pack()

# 运行主循环
root.mainloop()