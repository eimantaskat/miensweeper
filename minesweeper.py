import pygetwindow
import win32gui
import ctypes
import pyautogui
from PIL import Image, ImageGrab, ImageOps
import cv2
import numpy as np
import time

class Minesweeper():
    def __init__(self):
        if not self._running():
            raise self.Error("Minesweeper not running")

        pyautogui.PAUSE = 0

        self.tile_im = self._get_tile_img()
        self.sz = self.tile_im.shape[0]

        self.region = self._geometry()
        
        self._bring_to_front()
        self.minesweeper_img = self._get_ms_window_img()
        self.tiles = self._get_tiles()
        if not self.tiles:
            # TODO restart the game
            pass

        self.begin, self.end = self.tiles[0], self.tiles[-1]
        self.width = self.end[0] - self.begin[0] + self.sz
        self.heigth = self.end[1] - self.begin[1] + self.sz
        self.grid_region = *self.begin, self.width, self.heigth

        self.ref_tiles = []
        for i in range(10):
            self.ref_tiles.append(Image.open(f"images/{self.sz}/{i}.png").load())

    def _get_tiles(self):
        res = cv2.matchTemplate(self.minesweeper_img, self.tile_im, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)

        tiles = [(self.region[0] + x, self.region[1] + y) for x, y in zip(*loc[::-1])] # Switch collumns and rows

        # image = pyautogui.screenshot()
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # for pt in tiles:
        #     cv2.circle(image, pt, radius=0, color=(0, 0, 255), thickness=-1)

        # cv2.imshow("img", image)
        # cv2.waitKey(0)
        # quit()
        return tiles

    def _get_ms_window_img(self):
        window_image = ImageGrab.grab(bbox=self.region, all_screens=True)
        cv_tile_image = np.array(window_image)
        cv_grayscale_window_image = cv2.cvtColor(cv_tile_image, cv2.COLOR_BGR2GRAY)
        cv_grayscale_window_image = cv2.cvtColor(cv_tile_image, cv2.COLOR_BGR2GRAY)
        return cv_grayscale_window_image

    def _get_tile_img(self):
        tile_image = cv2.imread('images/tile.png')
        grayscale_tile_img = cv2.cvtColor(tile_image, cv2.COLOR_BGR2GRAY)
        return grayscale_tile_img

    def _running(self):
        return ('Minesweeper X' in pygetwindow.getAllTitles())

    def _bring_to_front(self):
        try:
            minesweeper = pygetwindow.getWindowsWithTitle('Minesweeper X')[0]
            minesweeper.activate()
            return True
        except pygetwindow.PyGetWindowException:
            return False

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
        grid_sc = pyautogui.screenshot(region=self.grid_region)
        grid = self.Grid(grid_sc, self.width//self.sz, self.heigth//self.sz, self.sz)

        t = [ [0]*grid.width for _ in range(grid.height)]

        for x in range(grid.width):
            for y in range(grid. height):
                box = (x * grid.tile_size, y * grid.tile_size, (x + 1) * grid.tile_size, (y + 1) * grid.tile_size)
                t[y][x] = grid.image.crop(box)


        for x in range(grid.width):
            for y in range(grid.height):
                # t[y][x].save('im/'+str(y)+'_'+str(x)+'.png')
                t[y][x] = self._get_tile_value(t[y][x])

        print(np.matrix(t))
        return t

    def click(self, x, y, safe):
        x_offset = self.begin[0] + self.sz // 2
        y_offset = self.begin[1] + self.sz // 2

        x_coord = x_offset + self.sz * x
        y_coord = y_offset + self.sz * y

        if safe:
            pyautogui.click(x_coord, y_coord)
        else:
            pyautogui.rightClick(x_coord, y_coord)

    def game_over(self):
        ms_window = pyautogui.screenshot(region=self.region)
        pass