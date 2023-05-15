# 导入tkinter库
import tkinter as tk

# 导入ttkbootstrap库
from tkinter import ttk
from ttkbootstrap import Style

# 创建主窗口，并使用minty主题
style = Style(theme='minty')
window = style.master
window.title('简易计算器')
window.geometry('300x400')

# 定义一个字符串变量，用于显示计算结果
result = tk.StringVar()
result.set(0)

# 创建一个标签，用于显示结果
label = tk.Label(window, bg='lightgreen', width=25, textvariable=result)
label.place(x=5, y=5)

# 定义一个列表，存储按钮的文本
buttons = ['Clear', 'Del', '%', '/',
           '7', '8', '9', '*',
           '4', '5', '6', '-',
           '1', '2', '3', '+',
           '.', '0', '=']

# 定义一个函数，用于处理按钮的点击事件
def click(event):
    global result # 声明全局变量
    value = event.widget['text'] # 获取按钮的文本
    if value == '=': # 如果是等号，就计算表达式的值，并显示结果
        try:
            result.set(result.get() + '=' + str(eval(result.get())))
        except:
            result.set('Error')
    elif value == 'Clear': # 如果是清除键，就清空结果
        result.set(0)
    elif value == 'Del': # 如果是删除键，就删除最后一个字符
        if result.get() != 0:
            result.set(result.get()[:-1])
    else: # 其他情况，就在结果后面追加字符
        if result.get() == '0':
            result.set(value)
        else:
            result.set(result.get() + value)

# 循环创建按钮，并绑定点击事件，并设置按钮的形状和大小为圆角和大号（rounded-lg）
x = 5 # 按钮的初始横坐标
y = 50 # 按钮的初始纵坐标

for i in range(len(buttons)):
    button = ttk.Button(window, text=buttons[i], width=6, style='success.TButton') # 创建按钮对象，并指定样式为rounded-lg.TButton 
    button.place(x=x, y=y) # 放置按钮对象到窗口上 
    button.bind('<Button-1>', click) # 绑定点击事件到函数click上
    
    x += 70 # 更新横坐标
    
    if (i + 1) % 4 == 0: # 如果是每行的最后一个按钮，就换行，并重置横坐标和纵坐标 
        x = 5 
        y += 50

# 启动主循环        
window.mainloop()
