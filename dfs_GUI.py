# coding=utf-8

from dfs import *

from Tkinter import *
from PIL import Image,ImageTk
import tkFileDialog
import ttk
# from threading import Timer
import time
import copy

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
B_open = Button(BF, text='Open', font=('Helvetica','20'))
B_run = Button(BF, text='Run', font=('Helvetica','20'))
B_open.pack(side=LEFT,padx=10)
B_run.pack(side=LEFT,padx=10)

Rcv = Canvas(root,bg='black',width=600,height=440)
Rcv.grid(row=0,column=1,padx=20,pady=15)

Pb = ttk.Progressbar(root, length=600, mode="determinate",maximum=100,orient=HORIZONTAL)
Pb.grid(row=1,column=1,padx=10,pady=10)

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

def Open():
    global path
    path = tkFileDialog.askopenfilenames(filetypes=[("PNG","*.png")])[0]
    
    image = Image.open(path).convert('L')
    image = image.resize((int(750*Scale), int(1334*Scale)),Image.ANTIALIAS)  # 带滤镜缩放 防止失真
    global PI   # Tk Canvas Bug : https://blog.csdn.net/u011320646/article/details/12845761
    PI = ImageTk.PhotoImage(image)
    Lcv.create_image(2,2,anchor=NW, image=PI)  # 2,2 What the Fuck?

    Init(path)
    print_rule()
    print_block()

B_open.configure(command=Open)

def Run():
    dfs(0)

    for vi in vm:
        del vi[:]
    Init(path)

    Pb.configure(maximum=len(deep_list))
    for deep in range(len(deep_list)):
        i = deep_list[deep][0]
        j = deep_list[deep][1]
        pour(i, j)
        print_block()
        print_ring(i,j)
        Pb.configure(value=deep+1)
        root.update()
        time.sleep(0.5)

B_run.configure(command=Run)

root.mainloop()
