import tkinter as tk
from PIL import Image, ImageTk, ImageChops
from tkinter import filedialog
import os
import configparser

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -50)
    bbox = diff.getbbox()

    return bbox

def onCanvasMotion(event):
    canv.delete('line')
    linex = canv.create_line(0, event.y, w, event.y , fill="green", tag="line")
    liney = canv.create_line(event.x, 0, event.x, h , fill="green", tag="line")

def onCanvasClick(event):
    global rect, start_x, start_y
    canv.delete('line')
    if not rect == None:
        canv.delete(rect)
    start_x = event.x
    start_y = event.y
    rect = canv.create_rectangle(x, y, 1, 1, outline="red", width=1)
    print('start coordinates: x={0} y={1}'.format(start_x, start_y))

def onCanvasMove(event):
    curX, curY = (event.x, event.y)
    canv.coords(rect, start_x, start_y, curX, curY)

def onCanvasRelease(event):
    print(resize)
    print(resize_factor)
    x0 = start_x
    y0 = start_y
    x1 = event.x
    y1 = event.y
    global w, h, hotspot
    print(x0, y0, x1, y1)
    x = x0
    if x1 < x0:
        x = x1
        x2 = x0
        if x2 > w:
            x2 = w
        print(x, x2, w)
    else:
        x2 = x1
        if x2 > w:
            x2 = w
        print(x, x2, w)
    if x < 0:
        x = 0

    y = y0
    if y1 < y0:
        y = y1
        y2 = y0
        if y2 > h:
            y2 = h
    else:
        y2 = y1
        if y2 > h:
            y2 = h
    if y < 0:
        y = 0
    width = x2 - x
    height = y2 - y
    print(w, h)
    print(x, y, width, height)
    if resize:
        hotspot = "({0},{1},{2},{3})".format(int(x/resize_factor), int(y/resize_factor), int(width/resize_factor), int(height/resize_factor))
    else:
        hotspot = "({0},{1},{2},{3})".format(x, y, width, height)
    print(hotspot)

def close_window():
    print(hotspot)
    win.destroy()

def skip_image():
    global hotspot
    hotspot = None
    win.destroy()

def change_bg(color):
    global canv, config
    canv.config(bg=color)
    config['Colors'] = {'hotspot BG_color' : color}
    with open('app_config.ini','w') as configfile:
        config.write(configfile)

def main(found_file, line_content):

    global win, canv, rect, start_x, start_y, w, h, x, y, hotspot, resize,resize_factor, linex, liney, bg_color,config

    config = configparser.ConfigParser()
    config.read('app_config.ini')
    automated_hotspot = None
    rect = None
    linex = None
    liney = None
    start_x = None
    start_y = None
    x = y = 0
    resize = False
    resize_factor = 1
    if config.has_option('Colors','hotspot BG_color'):
        bg_color = config['Colors']['hotspot BG_color']
    else:
        bg_color = 'blue'


    win = tk.Toplevel()
    win.title(found_file)
    print(found_file)
    try:
        slika = Image.open(found_file)
    except:
        # slika = Image.open("imagenotfound.png")
        open_file = filedialog.askopenfilename(title = "{}".format(found_file))
        print(open_file)
        slika = Image.open(open_file)

    screen_width = win.winfo_screenwidth()
    screen_heigth = win.winfo_screenheight()
    print("screen size : ({0}, {1})".format(screen_width, screen_heigth))
    w, h = slika.size
    print(slika.format,slika.size,slika.mode)
    try:
        imbox = slika.convert("RGBa")

    except ValueError as e:
        print(e)
        imbox = slika
        pass
    automated_hotspot = imbox.getbbox()
    # automated_hotspot = trim(imbox)


    if w > screen_width-30 or h > screen_heigth-70:
        print("Image too big for the screen. Resizing...")
        resize = True
        resize_factor = min((screen_width -70) / w,(screen_heigth -160) / h)
    w = int(w * resize_factor)
    h = int(h * resize_factor)
    print("New size ({0},{1})".format(w,h))

    if automated_hotspot is not None:
        a,b,c,d = automated_hotspot
        e = c-a
        f = d-b

        hotspot = "({0},{1},{2},{3})".format(a, b, e, f)
        print(automated_hotspot)
        print(hotspot)
        c = int(c * resize_factor)
        d = int(d * resize_factor)
        a = int(a * resize_factor)
        b = int(b * resize_factor)
        resized_hotspot = (a,b,c,d)


    if resize:
        slika = slika.resize((w, h), Image.ANTIALIAS)

    win.geometry('+0+0')
    # win.minsize(520, h)
    frame1 = tk.Frame(win, width=w)
    frame1.pack()
    frame2 = tk.LabelFrame(win, width=w, height=h, pady=10, text=line_content)
    frame2.pack()

    quitButton = tk.Button(frame1, text='Save', command=close_window).pack(side=tk.LEFT)
    skipButton = tk.Button(frame1, text='Skip', command=skip_image).pack(side=tk.LEFT)
    space_text = tk.Label(frame1,text="                       ").pack(side=tk.LEFT)
    bg_text = tk.Label(frame1,text="Change background color:").pack(side=tk.LEFT)
    change_blue = tk.Button(frame1, bg="blue",width=2, command=lambda:change_bg("blue")).pack(side=tk.LEFT)
    change_black = tk.Button(frame1, bg='black',width=2, command=lambda:change_bg("black")).pack(side=tk.LEFT)
    change_white = tk.Button(frame1, bg='white',width=2, command=lambda:change_bg("white")).pack(side=tk.LEFT)
    change_red = tk.Button(frame1, bg='red',width=2, command=lambda:change_bg("red")).pack(side=tk.LEFT)

    canv = tk.Canvas(frame2, bg=bg_color, width=w, height=h, cursor='crosshair')

    canv.bind('<ButtonPress-1>', onCanvasClick)
    canv.bind("<B1-Motion>", onCanvasMove)
    canv.bind('<ButtonRelease-1>', onCanvasRelease)
    canv.bind('<Motion>', onCanvasMotion)

    canv.pack()

    tk_im = ImageTk.PhotoImage(slika)
    canv.create_image(0, 0, anchor="nw", image=tk_im)
    if automated_hotspot is not None:
        canv.create_rectangle(resized_hotspot, outline="yellow", width=1.5)

    print("waiting...")
    win.wait_window(win)
    print('konacno')

    return hotspot

if __name__ == '__main__':

    found_file = filedialog.askopenfilename()
    main(found_file, "proba")
