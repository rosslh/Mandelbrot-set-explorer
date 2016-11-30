import math
import random
import time
from tkinter import *


class Mandelbrot(Frame):
    def __init__(self, xCenter, yCenter, delta, h, w, bailout, paletteSize,
                 parent):
        Frame.__init__(self, parent)
        self.h = h
        self.w = w
        self.xCenter = xCenter
        self.yCenter = yCenter
        self.delta = delta
        self.xmin = xCenter - delta  # more of the same...
        self.xmax = xCenter + delta
        self.ymin = yCenter + delta
        self.ymax = yCenter - delta
        self.bailout = bailout
        self.c, self.z = complex(0, 0), complex(0, 0)
        self.zoomFactor = 0.2
        self.paletteSize = paletteSize
        self.palette = self.getPalette()
        self.totalPixels = self.h * self.w

        self.parent = parent
        self.parent.title("Mandelbrot")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.draw()
        parent.bind("<Button-1>", self.clickEvent)

    def clickEvent(self, event):
        self.xCenter = self.translate(event.x, 0, self.w, self.xmin, self.xmax)
        self.yCenter = self.translate(event.y, self.h, 0, self.ymin, self.ymax)
        self.update(self.zoomFactor)
        print("Current canvas center: ", self.xCenter, self.yCenter)

    def update(self, factor):
        self.delta *= factor
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter - self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter + self.delta
        self.draw()

    def draw(self):
        oldSeconds, seconds = 0, 0
        for x in range(self.w):
            for y in range(self.h):
                seconds = int(time.time())
                if seconds != oldSeconds:
                    oldSeconds = seconds
                    completed = round((x * self.h) / self.totalPixels * 100, 2)
                    print("{}% completed".format(completed))
                escapeTime = self.getEscapeTime(complex(0, 0), self.setC(x, y))
                if escapeTime[0]:
                    color = self.palette[escapeTime[1] % self.paletteSize]
                    self.drawPixel(x, y, color)
                else:
                    self.drawPixel(x, y, '#000000')
        self.canvas.pack(fill=BOTH, expand=1)

    def setC(self, col, row):
        re = self.translate(col, 0, self.w, self.xmin, self.xmax)
        im = self.translate(row, 0, self.h, self.ymax, self.ymin)
        self.c = complex(re, im)
        return self.c

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def drawPixel(self, x, y, color):
        self.canvas.create_line(x, y, x+1, y, fill=color)

    def getEscapeTime(self, z, c):
        for i in range(self.bailout):
            z = z * z + c
            if abs(z) > 2:
                return True, i
        return False, self.bailout

    def getPalette(self):
        palette = []
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(self.paletteSize):
            red = int(256 * (0.5 * math.sin(redb * i + redc) + 0.5))
            green = int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5))
            blue = int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5))
            r, g, b = clamp(red), clamp(green), clamp(blue)
            palette.append("#{0:02x}{1:02x}{2:02x}".format(r, g, b))
        return palette


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = width = round(master.winfo_screenheight()*0.9)
    ex = Mandelbrot(-0.7, 0, 1.7, height, width, 90, 256, master)
    master.geometry("{}x{}".format(width, height))
    master.mainloop()

main()
