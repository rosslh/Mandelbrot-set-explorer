from multiprocessing import Pool


class Mandelbrot():
    def __init__(self, canvasW, x=-0.75, y=0, m=1.5, iterations=None, dimensions=None, zoomFactor=0.05, multi=True):
        self.dimensions = round(canvasW*0.9) if dimensions is None else dimensions
        self.h = self.w = self.dimensions
        self.iterations = 200 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        self.delta = m
        self.multi = multi
        self.xmin = x - m
        self.xmax = x + m
        self.ymin = y - m
        self.ymax = y + m
        self.zoomFactor = zoomFactor
        self.scaleFactor = self.dimensions/canvasW
        self.c, self.z = 0, 0

    def shiftView(self, event):
        self.xCenter = translate(event.x*self.scaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.scaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter + self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter - self.delta

    def zoomOut(self, event):
        self.xCenter = translate(event.x*self.scaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.scaleFactor, self.h, 0, self.ymin, self.ymax)
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter + self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter - self.delta

    def zoomIn(self, event):
        self.xCenter = translate(event.x*self.scaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.scaleFactor, self.h, 0, self.ymin, self.ymax)
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter + self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter - self.delta

    def getPixels(self):
        coordinates = []
        for x in range(self.w):
            for y in range(self.h):
                coordinates.append((x, y))
        if self.multi:
            pool = Pool()
            self.pixels = pool.starmap(self.getEscapeTime, coordinates)
            pool.close()
            pool.join()
        else:
            print("Using 1 core...")
            pixels = []
            for coord in coordinates:
                pixels.append(self.getEscapeTime(coord[0], coord[1]))
            self.pixels = pixels

    def getEscapeTime(self, x, y):
        re = translate(x, 0, self.w, self.xmin, self.xmax)
        im = translate(y, 0, self.h, self.ymax, self.ymin)
        z, c = complex(re, im), complex(re, im)
        for i in range(1, self.iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z*z + c
        return (x, y, 0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
