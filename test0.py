import tkinter as tk
from tkinter import messagebox
root = tk.Tk()  # 创建窗口
root.title('演示窗口')
root.geometry("300x100+630+80")  # (宽度x高度)+(x轴+y轴)

btn1 = tk.Button(root)  # 创建按钮，并且将按钮放到窗口里面
btn1["text"] = "点击"  # 给按钮一个名称
btn1.pack()  # 按钮布局


def test(e):
    '''创建弹窗'''
    messagebox.showinfo("窗口名称", "点击成功")


btn1.bind("<Button-1>", test)  # 将按钮和方法进行绑定，也就是创建了一个事件
root.mainloop()  # 让窗口一直显示，循环

