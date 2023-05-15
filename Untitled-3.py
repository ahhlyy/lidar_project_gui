import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# 添加第一个分割线
sep1 = ttk.Separator(root, orient="horizontal")
sep1.pack(fill="x", padx=10, pady=10)

# 添加一些其他小部件
label1 = tk.Label(root, text="Label 1")
label1.pack(padx=10, pady=10)

button1 = tk.Button(root, text="Button 1")
button1.pack(padx=10, pady=10)

# 添加第二个分割线
sep2 = ttk.Separator(root, orient="horizontal")
sep2.pack(fill="x", padx=10, pady=10)

# 添加一些其他小部件
label2 = tk.Label(root, text="Label 2")
label2.pack(padx=10, pady=10)

button2 = tk.Button(root, text="Button 2")
button2.pack(padx=10, pady=10)



e = tk.Entry(root, show='*') #输入框，输入时显示*
e.pack()

t = tk.Text(root,height=2)  #创建文本框，用户可输入内容
t.pack()

root.mainloop()