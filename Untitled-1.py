from tkinter import *
from tkinter import ttk
import threading
import serial
import serial.tools.list_ports
import inspect
import  sys
 
global serial_com
global ser
port_serial = " "
bitrate_serial = " "
 
"""
串口数据接受线程
"""
def thread_recv():
    global ser
    global text1
    while True:
        read = ser.readall()
        if len(read) > 0:
            print(__file__, sys._getframe().f_lineno, "<--",bytes(read).decode('ascii'))
            text1.insert(END,bytes(read).decode('ascii'))
 
"""
串口打开关闭函数
"""
def  usart_ctrl(var,port_,bitrate_):
    global ser
    print(__file__,sys._getframe().f_lineno,port_,bitrate_,var.get())
 
    if var.get() == "打开串口":
        var.set("关闭串口")
        ser = serial.Serial(
            port = port_,
            baudrate=int(bitrate_),
            parity=serial.PARITY_NONE,
            timeout=0.2,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
 
        #ser.open()
        recv_data = threading.Thread(target=thread_recv)
        recv_data.start()
    else :
        var.set("打开串口")
        #ser.close()
 
"""
串口发送函数
"""
def usart_sent(var):
    print(__file__,sys._getframe().f_lineno,"-->",var)
    x = ser.isOpen()
    if x == True:
        ser.write(var.encode("utf-8"))
    #print("-->",writedata)
 
"""
串口号改变回掉函数
"""
def combo1_handler(var):
    port_serial = var
    print(__file__,sys._getframe().f_lineno,var,port_serial)
 
"""
串口波特率改变回掉函数
"""
def combo2_handler(var):
    bitrate_serial = var
    print(__file__,sys._getframe().f_lineno,var,bitrate_serial)
 
def main():
    init_window = Tk()
    init_window.title('串口调试助手')
    #init_window.geometry("800x600")
 
    frame_root = Frame(init_window)
    frame_left = Frame(frame_root)
    frame_right = Frame(frame_root)
 
    pw1 = PanedWindow(frame_left,orient=VERTICAL)
    pw2 = PanedWindow(frame_left,orient=VERTICAL)
    pw3 = PanedWindow(frame_left,orient=VERTICAL)
 
    frame1 = LabelFrame(pw1,text="串口设置")
    frame2 = Frame(frame_left)
    frame3 = LabelFrame(pw2,text="接收设置")
    frame4 = LabelFrame(pw3,text="发送设置")
 
    pw1.add(frame1)
    pw1.pack(side=TOP)
    frame2.pack(side=TOP)
    pw2.add(frame3)
    pw2.pack(side=TOP)
    pw3.add(frame4)
    pw3.pack()
    frame5 = Frame(frame_right)
    frame5.pack(side=TOP)
    frame6 = Frame(frame_right)
    frame6.pack(side=LEFT)
 
    global text1
    text1 = Text(frame5,width=100,height=30)
    text1.grid(column=0,row=0)
    text2 = Text(frame6,height=10)
    text2.grid(column=0,row=0)
 
    button2 = Button(frame6,text="发送",width=14,height=1)
    button2.bind("<Button-1>",lambda event:usart_sent(var=text2.get("0.0","end")))
    button2.grid(column=1,row=0)
 
    label1 = Label(frame1,text="串口号",height=2)
    label1.grid(column=0,row=0)
    label2 = Label(frame1,text="波特率",height=2)
    label2.grid(column=0,row=1)
    label3 = Label(frame1,text="数据位",height=2)
    label3.grid(column=0,row=2)
    label4 = Label(frame1,text="校验位",height=2)
    label4.grid(column=0,row=3)
    label5 = Label(frame1,text="停止位",height=2)
    label5.grid(column=0,row=4)
 
    port_list = list(serial.tools.list_ports.comports())
    print(len(port_list))
 
    portcnt = 0;
    portcnt = len(port_list)
    serial_com = []
 
    varPort = StringVar()
    combo1 = ttk.Combobox(frame1,textvariable = varPort, width=8,height=2,justify=CENTER)
    for m in range(portcnt):
        port_list_1 = list(port_list[m])
        serial_com.append(port_list_1[0])
 
    serial_com.append("COM0")
    combo1['values'] = serial_com
    print(__file__,sys._getframe().f_lineno,m,serial_com)
 
    combo1.bind("<<ComboboxSelected>>",lambda event:combo1_handler(var=varPort.get()))
    combo1.current(0)
    combo1.grid(column=1,row=0)
    varBitrate  = StringVar()
    combo2 = ttk.Combobox(frame1,textvariable = varBitrate,width=8,height=2,justify=CENTER)
    combo2['values']=("9600","19200","38400","115200")
    combo2.bind("<<ComboboxSelected>>",lambda event:combo2_handler(var=varBitrate.get()))
    combo2.current(0)
    combo2.grid(column=1,row=1)
    combo3 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER)
    combo3['values']=("5 bit","6 bit","7 bit","8 bit")
    combo3.current(3)
    combo3.grid(column=1,row=2)
    combo4 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER)
    combo4['values']=("NONE","ODD","EVEN","MARK","SPACE")
    combo4.current(0)
    combo4.grid(column=1,row=3)
    combo5 = ttk.Combobox(frame1,width=8,height=2,justify=CENTER)
    combo5['values']=("1 bit","1.5 bit","2 bit")
    combo5.current(0)
    combo5.grid(column=1,row=4)
 
    var1 = StringVar()
    var1.set("打开串口")
    button1 = Button(frame2,textvariable=var1,width=18,height=1)
    button1.bind("<Button-1>",lambda event:usart_ctrl(var=var1,port_=combo1.get(),bitrate_=combo2.get()))
    button1.grid(column=0,row=0)
 
    """
    接受设置
    """
    radio1 = Radiobutton(frame3,value=0)
    radio2 = Radiobutton(frame3,value=0)
    radio3 = Radiobutton(frame3,value=0)
    radio4 = Radiobutton(frame3,value=0)
 
    radio1.grid(column=0,row=0)
    radio2.grid(column=0,row=1)
    radio3.grid(column=0,row=2)
    radio4.grid(column=0,row=3)
 
    label6 = Label(frame3,text="Receive to file",width=14,height=1,justify=LEFT)
    label7 = Label(frame3,text="Add line return",width=14,height=1,justify=LEFT)
    label8 = Label(frame3,text="Receive As HEX",width=14,height=1,justify=LEFT)
    label9 = Label(frame3,text="Receive Pause",width=14,height=1,justify=LEFT)
 
    label6.grid(column=1,row=0)
    label7.grid(column=1,row=1)
    label8.grid(column=1,row=2)
    label9.grid(column=1,row=3)
 
    """
    发送设置
    """
 
    radio5 = Radiobutton(frame4)
    radio6 = Radiobutton(frame4)
    radio7 = Radiobutton(frame4)
    radio8 = Radiobutton(frame4)
    radio9 = Radiobutton(frame4)
 
    radio5.grid(column=0,row=0)
    radio6.grid(column=0,row=1)
    radio7.grid(column=0,row=2)
    radio8.grid(column=0,row=3)
    radio9.grid(column=0,row=4)
 
    label10 = Label(frame4,text="Data from file",width=14,height=1,justify=LEFT)
    label11 = Label(frame4,text="Auto Checksum",width=14,height=1,justify=LEFT)
    label12 = Label(frame4,text="Auto Clear Input",width=14,height=1,justify=LEFT)
    label13 = Label(frame4,text="Send As HEX",width=14,height=1,justify=LEFT)
    label14 = Label(frame4,text="Send Recycle",width=14,height=1,justify=LEFT)
 
    label10.grid(column=1,row=0)
    label11.grid(column=1,row=1)
    label12.grid(column=1,row=2)
    label13.grid(column=1,row=3)
    label14.grid(column=1,row=4)
 
    """
    """
 
    frame_left.pack(side=LEFT)
    frame_right.pack(side=RIGHT)
    frame_root.pack()
    init_window.mainloop()
 
 
if __name__ == "__main__":
    main()