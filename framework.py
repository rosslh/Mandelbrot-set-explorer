import os
import argparse
import sys
import math
import time
import random
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot import Mandelbrot


class Framework(Frame):
    def __init__(self, parent, h, w, x=-0.75, y=0, m=1.5, iterations=None, dimensions=None, save=False, multi=True):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Mandelbrot")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        self.fractal = Mandelbrot(w, x=x, y=y, m=m, iterations=iterations, dimensions=dimensions, multi=multi)
        self.setPalette()
        self.canvasH, self.canvasW = h, w
        self.pixelColors = []
        self.img = None
        self.save = save
        self.draw()

        parent.bind("<Button-1>", self.zoomIn)
        parent.bind("<Button-3>", self.zoomOut)
        parent.bind("<Control-1>", self.shiftView)
        parent.bind("<Control-3>", self.changePalette)
        parent.bind("<Button-2>", self.saveImage)

    def zoomIn(self, event):
        self.fractal.zoomIn(event)
        self.draw()

    def zoomOut(self, event):
        self.fractal.zoomIn(event)
        self.draw()

    def shiftView(self, event):
        self.fractal.zoomIn(event)
        self.draw()

    def draw(self):
        print('-' * 20)
        start = time.time()
        self.fractal.getPixels()
        self.getColors()
        self.drawPixels()
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)
        print("Process took {} seconds".format(round(time.time()-start, 2)))
        print("Current coordinates (x, y, m): {}, {}, {}".format(self.fractal.xCenter, self.fractal.yCenter, self.fractal.delta))

    def setPalette(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
            palette.append((r, g, b))
        self.palette = palette

    def changePalette(self, event):
        self.setPalette()
        self.pixelColors = []
        self.getColors()
        self.drawPixels()
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)

    def getColors(self):
        pixelColors = []
        for p in self.fractal.pixels:
            pixelColors.append(self.palette[p[2] % 256])
        self.pixelColors = pixelColors

    def drawPixels(self):
        img = Image.new('RGB', (self.fractal.w, self.fractal.h), "black")
        pixels = img.load()  # create the pixel map
        for index, p in enumerate(self.fractal.pixels):
            pixels[p[0], p[1]] = self.pixelColors[index]
        self.img = img
        if self.save:
            self.saveImage(None)
        photoimg = ImageTk.PhotoImage(img.resize((self.canvasW, self.canvasH)))
        self.background = photoimg

    def saveImage(self, event):
        self.img.save("output/{}.png".format(time.strftime("%Y-%m-%d-%H:%M:%S")), "PNG", optimize=True)


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = width = round(master.winfo_screenheight()*0.9)
    parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
    parser.add_argument('-i', '--iterations', type=int, help='The number of iterations done for each pixel. Higher is more accurate but slower.')
    parser.add_argument('-x', type=float, help='The x-center coordinate of the frame.')
    parser.add_argument('-y', type=float, help='The y-center coordinate of the frame.')
    parser.add_argument('-m', '--magnification', type=float, help='The magnification level of the frame.')
    parser.add_argument('-d', '--dimensions', type=int, help='The (square) dimensions of the frame.')
    parser.add_argument('-s', '--save', action='store_true', help='Save the generated image.')
    parser.add_argument('-nm', '--noMulti', action='store_false', help="Don't use multiprocessing.")
    args = parser.parse_args()
    if None not in [args.x, args.y, args.magnification]:
        render = Framework(master, height, width, x=args.x, y=args.y, m=args.magnification, multi=args.noMulti,
                           iterations=args.iterations, dimensions=args.dimensions, save=args.save)
    else:
        if not all(arg is None for arg in [args.x, args.y, args.magnification]):
            print("Arguments ignored. Please provide all of x, y, & m.")
        render = Framework(master, height, width, multi=args.noMulti, iterations=args.iterations, dimensions=args.dimensions, save=args.save)
    master.geometry("{}x{}".format(width, height))
    master.mainloop()

main()
