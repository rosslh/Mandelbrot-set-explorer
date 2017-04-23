import math
import random
import time
import os
import argparse
import progressbar
import sys
from tkinter import *
from PIL import Image, ImageTk


class Mandelbrot(Frame):
    def __init__(self, parent, h, w, x=-0.7, y=0, z=1.5, bailout=100):
        Frame.__init__(self, parent)
        self.h = h
        self.w = w
        self.xCenter = x
        self.yCenter = y
        self.delta = z
        self.xmin = x - z
        self.xmax = x + z
        self.ymin = y - z
        self.ymax = y + z
        self.bailout = bailout
        self.c, self.z = 0, 0
        self.zoomFactor = 0.3
        self.setPalette()
        self.parent = parent
        self.parent.title("Mandelbrot")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.pixels = []
        self.pixelColors = []
        self.draw()
        parent.bind("<Button-1>", self.leftClickEvent)
        parent.bind("<Button-3>", self.rightClickEvent)

    def rightClickEvent(self, event):
        self.setPalette()
        self.pixelColors = []
        self.getColors()
        self.drawPixels()
        self.canvas.create_image(10, 10, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)

    def leftClickEvent(self, event):
        self.xCenter = translate(event.x, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y, self.h, 0, self.ymin, self.ymax)
        self.update(self.zoomFactor)

    def update(self, factor):
        self.delta *= factor
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter + self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter - self.delta
        print('-' * 20)
        self.draw()

    def draw(self):
        start = time.time()
        self.getOrbits()
        self.getColors()
        start = time.time()
        self.drawPixels()
        self.canvas.create_image(10, 10, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)
        print("Current coordinates: ", self.xCenter, self.yCenter, self.delta)

    def getColors(self):
        pixelColors = []
        for p in self.pixels:
            pixelColors.append(self.palette[p[2] % 256])
        self.pixelColors = pixelColors

    def getOrbits(self):
        pixels = []
        with progressbar.ProgressBar(max_value=self.w*self.h) as bar:
            i = 0
            for x in range(self.w):
                for y in range(self.h):
                    self.setC(x, y)
                    escapeTime = self.getEscapeTime(0, self.c, self.bailout)
                    pixels.append((x, y, escapeTime))
                    i += 1
                    bar.update(i)
        self.pixels = pixels

    def setC(self, col, row):
        re = translate(col, 0, self.w, self.xmin, self.xmax)
        im = translate(row, 0, self.h, self.ymax, self.ymin)
        self.c = complex(re, im)

    def drawPixels(self):
        img = Image.new('RGB', (self.w, self.h), "black")
        pixels = img.load()  # create the pixel map
        for index, p in enumerate(self.pixels):
            pixels[p[0], p[1]] = self.pixelColors[index]
        photoimg = ImageTk.PhotoImage(img)
        self.background = photoimg

    def getEscapeTime(self, z, c, bailout):
        for i in range(1, bailout):
            if abs(z) > 2:
                return i
            z = z*z + c
        return 0

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


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = width = round(master.winfo_screenheight()*0.9)
    try:
        parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
        parser.add_argument('-i', '--iterations', type=int, help='The number of iterations done for each pixel.')
        parser.add_argument('-x', type=float, help='The x-center coordinate of the frame.')
        parser.add_argument('-y', type=float, help='The y-center coordinate of the frame.')
        parser.add_argument('-z', '--zoom', type=float, help='The zoom level of the frame.')
        args = parser.parse_args()
        if args.iterations is not None:
            if None not in [args.x, args.y, args.zoom]:
                render = Mandelbrot(master, height, width, x=args.x, y=args.y, z=args.zoom, bailout=args.iterations)
            else:
                render = Mandelbrot(master, height, width, bailout=args.iterations)
        else:
            if None not in [args.x, args.y, args.zoom]:
                render = Mandelbrot(master, height, width, x=args.x, y=args.y, z=args.zoom)
            else:
                render = Mandelbrot(master, height, width)
    except Exception as E:
        print('Error: {}'.format(str(E)))
        render = Mandelbrot(master, height, width)
    master.geometry("{}x{}".format(width, height))
    master.mainloop()

main()
