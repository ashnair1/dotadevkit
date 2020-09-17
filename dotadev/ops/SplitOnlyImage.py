import copy
import cv2
import numpy as np
from pathlib import Path


class ImgSplitter:
    def __init__(self, srcpath, dstpath, gap=100, subsize=1024, ext=".png"):
        self.srcpath = Path(srcpath)
        self.dstpath = Path(dstpath)
        self.gap = gap
        self.subsize = subsize
        self.slide = self.subsize - self.gap
        self.ext = ext

        if self.dstpath.exists() is False:
            self.dstpath.mkdir()

    def savepatches(self, img, subimgname, left, up, ext=".png"):
        subimg = copy.deepcopy(img[up : (up + self.subsize), left : (left + self.subsize)])
        outdir = self.dstpath / (subimgname + ext)
        cv2.imwrite(str(outdir), subimg)

    def split_single(self, name, rate, extent):
        img = cv2.imread(str(self.srcpath / (name + extent)))
        assert np.shape(img) != ()

        if rate != 1:
            resizeimg = cv2.resize(img, None, fx=rate, fy=rate, interpolation=cv2.INTER_CUBIC)
        else:
            resizeimg = img
        outbasename = name + "__" + str(rate) + "__"

        weight = np.shape(resizeimg)[1]
        height = np.shape(resizeimg)[0]

        left, up = 0, 0
        while left < weight:
            if left + self.subsize >= weight:
                left = max(weight - self.subsize, 0)
            up = 0
            while up < height:
                if up + self.subsize >= height:
                    up = max(height - self.subsize, 0)
                subimgname = outbasename + str(left) + "___" + str(up)
                self.savepatches(resizeimg, subimgname, left, up)
                if up + self.subsize >= height:
                    break
                else:
                    up = up + self.slide
            if left + self.subsize >= weight:
                break
            else:
                left = left + self.slide

    def splitdata(self, rate):
        imagenames = [im.stem for im in self.srcpath.iterdir()]
        for name in imagenames:
            self.split_single(name, rate, self.ext)


if __name__ == "__main__":
    split = ImgSplitter(
        r"/home/ashwin/Desktop/Projects/DOTA_devkit/example/images",
        r"/home/ashwin/Desktop/Projects/DOTA_devkit/example/imagesSplit",
    )
    split.splitdata(1)
