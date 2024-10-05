import tkinter as tk
from tkinter import messagebox, Menu, StringVar
from tkinter import ttk
from controller import menu_controller, category_controller, dishes_controller

win = tk.Tk()
win.title("每日菜单")
win.geometry("400x200")


def gen_daily_menu():
    success, msg = menu_controller.MenuController().gen_menu()
    if success:
        messagebox.showinfo(title="每日菜单生成成功！", message=f'{msg}')
    else:
        messagebox.showerror(title='每日菜单生成失败！', message=f'{msg}')


def add_menu():
    category_values = category_controller.get_category()
    category_dict = {each[-1]: each[0] for each in category_values}
    value = StringVar()
    combobox = ttk.Combobox(
        master=win,  # 父容器
        height=5,  # 高度,下拉显示的条目数量
        width=5,  # 宽度
        state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=('', 10),  # 字体
        textvariable=value,  # 通过StringVar设置可改变的值
        values=[i[-1] for i in category_values],  # 设置下拉框的选项
    )
    L1 = tk.Label(win, text="菜单名:", width=10)
    entry1 = tk.Entry(win, width=50)

    def go():
        category_id = category_dict.get(value.get())
        dishes_name = entry1.get()
        success, msg = dishes_controller.add_dishes(dishes_name, category_id)
        if success:
            messagebox.showinfo(title="添加菜单成功！", message=f'{msg}')
        else:
            messagebox.showerror(title='添加菜单失败！', message=f'{msg}')

    frequency = tk.Button(win, text='确认', font=('Arial', 12), width=10, height=1, command=go)
    frequency.place(x=150, y=150)
    entry1.place(x=100, y=10)
    L1.place(x=100, y=10)
    L1.pack(side=tk.LEFT)
    entry1.pack(side=tk.RIGHT)
    combobox.place(x=100, y=50)


def main():
    menubar = Menu(win)
    daily_menu = Menu(menubar, tearoff=0)
    daily_menu.add_command(label="生成每日菜单", command=gen_daily_menu)
    daily_menu.add_command(label="增加菜单", command=add_menu)
    daily_menu.add_separator()  # 下拉菜单的分隔线
    daily_menu.add_command(label="退出", command=win.quit)
    menubar.add_cascade(label="菜单", menu=daily_menu)
    # 显示菜单
    win.config(menu=menubar)
    win.mainloop()


if __name__ == '__main__':
    main()
