from PIL import Image
import numpy as np
from datetime import datetime

class Picture:

    def __init__(self, width=1, height=1, color=[0,0,0]):
        """
        Initialisation. Takes 2 arguments: width and height.
        self.image - class from PIL;
        self.data - numpy array.
        """
        self.resolution = (height, width)
        self.data = np.full((height, width, 3), color, dtype=np.uint8)
        self.picture = Image.fromarray(self.data, 'RGB')

    def update_image(self):
        """
        Update picture from array, after changes.
        """
        self.picture = Image.fromarray(self.data, 'RGB')

    def show_image(self):
        """
        Show current state of the image
        """
        self.update_image()
        self.picture.show()

    def setPixel(self, x, y, color):
        """
        Insert pixel in (x, y) and setup the color.
        """
        self.data[x][y] = np.array(color, dtype=np.uint8)

    def setMultiplePixels(self, coords, color):
        """
        Draw Pixels in multiple coordinates.
        """
        for x,y in coords:
            self.setPixel(x, y, color)

    def draw_line(self, x1=0, y1=0, x2=0, y2=0, color=[255, 255, 255]):
        """
        Bresenham's line.
        """

        dx = x2 - x1
        dy = y2 - y1

        sign_x = 1 if dx>0 else -1 if dx<0 else 0
        sign_y = 1 if dy>0 else -1 if dy<0 else 0

        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy= sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = x1, y1

        error, t = el/2, 0

        self.setPixel(x, y, color)

        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            self.setPixel(x, y, color)

        self.update_image()

    def draw_straight_line(self, x1=0, y1=0, x2=0, y2=0, color=[255,255,255]):
        """
        For fast paint straight line.
        """
        for y in range(y2,y1):
            self.setPixel(x1, y, color)

    def draw_circle(self, x0=0, y0=0, radius=0, color=[255, 255, 255]):
        """
        Bresenham's circle.
        """

        x, y, error = 0, radius, 0
        delta = 1 - 2*radius

        while(y >= 0):

            self.setMultiplePixels([(x0+x, y0+y), (x0+x, y0-y), (x0-x, y0+y), (x0-x, y0-y)], color)

            error = 2*(delta + y)-1

            if(delta < 0 and error <= 0):
                x += 1
                delta += 2 * x + 1
                continue

            error = 2 * (delta - x) -1

            if(delta>0 and error>0):
                y -= 1
                delta += 1 - 2 * y
                continue

            x += 1
            delta += 2 * (x - y)
            y -= 1

        self.update_image()

    def draw_disc(self, x0=0, y0=0, radius=0, color=[255, 255, 255]):
        """
        If we need to fill a circle, we need to fill the lines from previous algorithm.
        """

        x, y, error = 0, radius, 0
        delta = 1 - 2*radius

        while(y >= 0):

            self.draw_straight_line(x0+x, y0+y, x0+x, y0-y, color)
            self.draw_straight_line(x0-x, y0+y, x0-x, y0-y, color)

            error = 2*(delta + y)-1

            if(delta < 0 and error <= 0):
                x += 1
                delta += 2 * x + 1
                continue

            error = 2 * (delta - x) -1

            if(delta>0 and error>0):
                y -= 1
                delta += 1 - 2 * y
                continue

            x += 1
            delta += 2 * (x - y)
            y -= 1

        self.update_image()

    def draw_square(self, x1=0, y1=0, x2=0, y2=0, color=[255,255,255]):
        """
        If we need to fill a circle, we need to create a circle
        and paint new circles with decreased radius from start to 0.
        """

        for x in range(x1, x2):
            self.draw_straight_line(x, y2, x, y1, color)

        self.update_image()

    def dragon(self, x1,y1,x2,y2,Depth, color=[255,255,255]):
        """
        A dragon curve is any member of a family of self-similar fractal curves.
        This is the recursive algorithm.
        """
        def paint(x1,y1,x2,y2,k, color=[255,255,255]):

            if k==0:
                self.draw_line(x1,y1,x2,y2,color=color)
                return None

            tx = (x1+x2) // 2+(y2-y1) // 2
            ty = (y1+y2) // 2-(x2-x1) // 2
            paint(x2,y2,tx,ty,k-1,color=[i-3 for i in color])
            paint(x1,y1,tx,ty,k-1,color=[i-3 for i in color])

        paint(x1,y1,x2,y2,Depth,color)
