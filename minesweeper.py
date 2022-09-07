import pygetwindow
import win32gui
import ctypes
import pyautogui
from PIL import Image
import time

class Minesweeper():
    def __init__(self):
        if not self._running():
            raise self.Error("Minesweeper not running")

        self.tile_im = Image.open('images/tile.png')
        self.sz, _ = self.tile_im.size

        self.region = self._geometry()
        
        self._bring_to_front()
        self.tiles = list(pyautogui.locateAllOnScreen(self.tile_im, grayscale=True, region=self.region))
        self.begin, self.end = self.tiles[0], self.tiles[-1]

        self.top_left_corner = None

        self.r = self.begin.left, self.begin.top, self.end.left - (self.begin.left) + 16, self.end.top - (self.begin.top) + 16

        pyautogui.PAUSE = 0

        self.ref_tiles = []
        for i in range(10):
            self.ref_tiles.append( Image.open(f"images/{self.sz}/{i}.png").load() )


    def _running(self):
            return ('Minesweeper X' in pygetwindow.getAllTitles())

    def _bring_to_front(self):
        try:
            minesweeper = pygetwindow.getWindowsWithTitle('Minesweeper X')[0]
            minesweeper.activate()
        except pygetwindow.PyGetWindowException:
            pass

    def _geometry(self):
        hwnd = ctypes.windll.user32.FindWindowW(0, 'Minesweeper X')
        rect = win32gui.GetWindowRect(hwnd)
        return rect


    class Grid():
        def __init__(self, im, w, h, sz):
            self.image = im
            self.width = w
            self.height = h
            self.tile_size = sz

    class Error(Exception):
        pass

    def _get_tile_value(self, image):
        image_data = image.load()
        for val in range(10):

            height = self.sz // 2
            y = height

            try:
                while image_data[height, y] == self.ref_tiles[val][height, y]:
                    y += 1
            except IndexError:
                return val

        return -1

    def get_grid(self):
        grid = self.Grid(pyautogui.screenshot(region=self.r), (self.end.left - self.begin.left) // self.sz + 1, (self.end.top - self.begin.top) // self.sz + 1, self.sz)

        t = [ [0]*grid.width for _ in range(grid.height)]

        for x in range(grid.width):
            for y in range(grid. height):
                box = (x * grid.tile_size, y * grid.tile_size, (x + 1) * grid.tile_size, (y + 1) * grid.tile_size)
                t[y][x] = grid.image.crop(box)


        for x in range(grid.width):
            for y in range(grid.height):
                # t[y][x].save('im/'+str(y)+'_'+str(x)+'.png')
                t[y][x] = self._get_tile_value(t[y][x])

        return t

    def click(self, x, y, safe):
        if not self.top_left_corner:
            self.top_left_corner = [self.tiles[0].left, self.tiles[0].top]

        if safe:
            pyautogui.click(self.top_left_corner[0] + self.sz // 2 + self.sz * x, self.top_left_corner[1] + self.sz // 2 + self.sz * y)
        else:
            pyautogui.rightClick(self.top_left_corner[0] + self.sz // 2 + self.sz * x, self.top_left_corner[1] + self.sz // 2 + self.sz * y)