import copy
import cv2
import numpy as np
from functools import partial
from multiprocessing import Pool
from pathlib import Path


def split_single_warp(name, split_base, rate, extent):
    split_base.split_single(name, rate, extent)


class ImgSplitter:
    def __init__(
        self,
        srcpath,
        dstpath,
        gap=100,
        subsize=1024,
        ext=".png",
        padding=True,
        num_process=32,
    ):
        self.srcpath = Path(srcpath)
        self.dstpath = Path(dstpath)
        self.gap = gap
        self.subsize = subsize
        self.slide = self.subsize - self.gap
        self.ext = ext
        self.padding = padding
        self.pool = Pool(num_process)

        if not self.dstpath.exists():
            self.dstpath.mkdir()

    def saveimagepatches(self, img, subimgname, left, up, ext=".png"):
        subimg = copy.deepcopy(img[up : (up + self.subsize), left : (left + self.subsize)])
        outdir = self.dstpath / (subimgname + ext)
        h, w, c = np.shape(subimg)
        if self.padding:
            outimg = np.zeros((self.subsize, self.subsize, 3))
            outimg[0:h, 0:w, :] = subimg
            cv2.imwrite(str(outdir), outimg)
        else:
            cv2.imwrite(str(outdir), subimg)

    def split_single(self, name, scale, ext):
        img = cv2.imread(str(self.srcpath / (name + ext)))
        assert np.shape(img) != ()

        if scale != 1:
            resizeimg = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        else:
            resizeimg = img
        outbasename = name + "__" + str(scale) + "__"

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
                self.saveimagepatches(resizeimg, subimgname, left, up)
                if up + self.subsize >= height:
                    break
                else:
                    up = up + self.slide
            if left + self.subsize >= weight:
                break
            else:
                left = left + self.slide

    def splitdata(self, scale):
        imagenames = [im.stem for im in self.srcpath.iterdir()]
        worker = partial(split_single_warp, split_base=self, rate=scale, extent=self.ext)
        self.pool.map(worker, imagenames)

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict["pool"]
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)


if __name__ == "__main__":
    split = ImgSplitter(
        r"/home/ashwin/Desktop/Projects/DOTA_devkit/example/images",
        r"/home/ashwin/Desktop/Projects/DOTA_devkit/example/imagesSplit2",
        num_process=32,
    )
    split.splitdata(1)
