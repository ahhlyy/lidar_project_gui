import tkinter as tk

root = tk.Tk()

# 创建菜单栏
menubar = tk.Menu(root)

# 创建File菜单
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open")
filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# 将File菜单添加到菜单栏
menubar.add_cascade(label="File", menu=filemenu)

# 将菜单栏添加到主窗口
root.config(menu=menubar)

root.mainloop()