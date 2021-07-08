# coding=utf-8

from dfs import *

from Tkinter import *
from PIL import Image,ImageTk
import tkFileDialog
import tkMessageBox
import ttk
from threading import Timer

Scale = 0.5  # 图片显示缩放倍数

# 4元素RGBA值转十六进制字符串
color_Hex = []
for c in color_RGB:
    RGB = '#'
    for i in range(3):
        shex = str(hex(c[i]))[2:]
        if len(shex) == 1:
            RGB += '0'
        RGB += shex
    color_Hex.append(RGB)

root = Tk()
root.resizable(False, False)
root.geometry("1065x775")
root.title('dfs_GUI')

Lcv = Canvas(root,bg='black',width=750*Scale,height=1334*Scale)
Lcv.grid(row=0,column=0,padx=20,pady=15)

BF = Frame(root)
BF.grid(row=1,column=0)
B_open = Button(BF, text='Open', font=('Arial','20'), width=6)
B_run = Button(BF, text='Run', font=('Arial','20'), width=6, state=DISABLED)
B_step = Button(BF, text='Step', font=('Arial','20'), width=6, state=DISABLED)
B_open.pack(side=LEFT,padx=10)
B_run.pack(side=LEFT,padx=10)
B_step.pack(side=LEFT,padx=10)

Rcv = Canvas(root,bg='black',width=600,height=440)
Rcv.grid(row=0,column=1,padx=20,pady=15)

BP = Frame(root)
BP.grid(row=1,column=1)
Pb = ttk.Progressbar(BP, length=600, mode="determinate",maximum=100,orient=HORIZONTAL)
Pl = Label(BP, text="", font=("Arial", 20))
Pl.pack()
Pb.pack()

def print_rule():
    for xl in x:
        Lcv.create_line(xl*Scale,0,xl*Scale,1334*Scale,fill="white")
    for yl in y:
        Lcv.create_line(0,yl*Scale,750*Scale,yl*Scale,fill="white")

def print_block():
    Rcv.delete("block")

    for i in range(len(vm)):
        x = (i%7)*80+40
        y = 200 if i<7 else 400
        vi = vm[i]
        for j in range(len(vi)):
            cur_color = color_Hex[color.index(vi[j])]
            Rcv.create_rectangle(x,y,x+40,y-40,fill=cur_color,tags='block')
            y -= 40

def print_ring(i,j):
    Rcv.delete("ring")

    x = (i%7)*80+20
    y = 220 if i<7 else 420
    Rcv.create_rectangle(x,y,x+80,y-200,outline="white",tags="ring")
    x = (j%7)*80+20
    y = 220 if j<7 else 420
    Rcv.create_rectangle(x,y,x+80,y-200,outline="white",tags="ring")

def clear_vm():
    for vi in vm:
        del vi[:]

def update_PbPl():
    Pb.configure(value=cur_deep)
    Pl.configure(text="{}/{}".format(cur_deep,deep_sum))

def Open():
    select = tkFileDialog.askopenfilenames(filetypes=[("PNG","*.png"),("JPEG","*.jpg;*.jpeg")])
    if len(select) == 0:
        return
    path = select[0]
    
    image = Image.open(path).convert('L')
    image_display = image.resize((int(750*Scale), int(1334*Scale)),Image.ANTIALIAS)  # 带滤镜缩放 防止失真
    global PI   # Tk Canvas Bug : https://blog.csdn.net/u011320646/article/details/12845761
    PI = ImageTk.PhotoImage(image_display)
    Lcv.create_image(2,2,anchor=NW, image=PI)  # 2,2 What the Fuck?

    clear_vm()
    del deep_list[:]     # Fix Bug
    del visit[:]         # Fix Bug
    Init(image=image)
    print_rule()
    Rcv.delete("ring")      # Fix Bug
    Pb.configure(value=0)   # Fix Bug
    print_block()

    if dfs(0) == False:
        tkMessageBox.showerror('GG','You Dead')
        B_run.config(state=DISABLED)
        B_step.config(state=DISABLED)
        return
    clear_vm()
    Init(image=image)

    global cur_deep
    cur_deep = 0
    global deep_sum
    deep_sum = len(deep_list)
    Pb.configure(maximum=deep_sum)
    update_PbPl()
    B_run.config(state=NORMAL)
    B_step.config(state=NORMAL)

B_open.configure(command=Open)

def Step():
    global cur_deep
    if cur_deep < deep_sum:
        i = deep_list[cur_deep][0]
        j = deep_list[cur_deep][1]
        pour(i, j)
        print_block()
        print_ring(i,j)
        cur_deep += 1
        update_PbPl()
        root.update()
    else:
        return False

B_step.configure(command=Step)

run_state = False

def Run(method=0):
    global run_state
    if method == 0:
        run_state = not run_state
        if run_state:
            B_run.configure(text='Paste')
            B_open.config(state=DISABLED)
            B_step.config(state=DISABLED)
        else:
            B_run.configure(text='Run')
            B_open.config(state=NORMAL)
            B_step.config(state=NORMAL)
            return
    else:
        if not run_state:
            return
        if Step() == False:
            Run(0)
            return
    t = Timer(0.5, Run, (1,))
    t.start()

B_run.configure(command=Run)

root.mainloop()
