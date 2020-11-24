# --------------------------------------------------------
# Modified by Ashwin Nair
# Written by Jian Ding for DOTA_Devkit
# --------------------------------------------------------

from collections import defaultdict
from pathlib import Path
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
from dotadevkit.misc.dota_utils import parse_dota_poly

import cv2
import matplotlib.pyplot as plt
import numpy as np


def _isArrayLike(obj):
    if type(obj) == str:
        return False
    return hasattr(obj, "__iter__") and hasattr(obj, "__len__")


class DOTA:
    def __init__(self, basepath):
        basepath = Path(basepath)
        self.basepath = basepath
        self.labelpath = basepath / "labelTxt"
        self.imagepath = basepath / "images"
        self.imgpaths = [lbl for lbl in self.labelpath.iterdir()]
        self.imglist = [x.stem for x in self.imgpaths]
        self.catToImgs = defaultdict(list)
        self.ImgToAnns = defaultdict(list)
        self.createIndex()

    def createIndex(self):
        for filename in self.imgpaths:
            objects = parse_dota_poly(filename)
            imgid = filename.stem
            self.ImgToAnns[imgid] = objects
            for obj in objects:
                cat = obj["name"]
                self.catToImgs[cat].append(imgid)

    def getImgIds(self, catNms=[]):
        """Get Image Ids

        Args:
            catNms ([str], optional): Category Names. Defaults to [].

        Returns:
            [dict]: Image ids that contain categories specified (catNms)
        """
        catNms = catNms if _isArrayLike(catNms) else [catNms]
        if len(catNms) == 0:
            return self.imglist
        else:
            imgids = []
            for i, cat in enumerate(catNms):
                if i == 0:
                    imgids = set(self.catToImgs[cat])
                else:
                    imgids &= set(self.catToImgs[cat])
        return list(imgids)

    def loadAnns(self, catNms=[], imgId=None, difficult=None):

        """Load annotations

        TODO: Currently only supports loading via category names

        Args:
            catNms ([str], optional): Category names. Defaults to [].
            imgId (str, optional): Image Id. Defaults to None.
            difficult ([type], optional): [description]. Defaults to None.

        Returns:
            [dict]: Annotations
        """
        catNms = catNms if _isArrayLike(catNms) else [catNms]
        objects = self.ImgToAnns[imgId]
        if len(catNms) == 0:
            return objects
        outobjects = [obj for obj in objects if (obj["name"] in catNms)]
        return outobjects

    def showAnns(self, objects, imgId):
        """Show annotations

        Args:
            objects ([dict]): objects to show
            imgId (str): img to show
        """
        img = self.loadImgs(imgId)[0]
        plt.imshow(img)
        plt.axis("off")

        ax = plt.gca()
        ax.set_autoscale_on(False)
        polygons = []
        color = []
        circles = []
        r = 5
        for obj in objects:
            c = (np.random.random((1, 3)) * 0.6 + 0.4).tolist()[0]
            poly = obj["poly"]
            polygons.append(Polygon(poly))
            color.append(c)
            point = poly[0]
            circle = Circle((point[0], point[1]), r)
            circles.append(circle)
        p = PatchCollection(polygons, facecolors=color, linewidths=0, alpha=0.4)
        ax.add_collection(p)
        p = PatchCollection(polygons, facecolors="none", edgecolors=color, linewidths=2)
        ax.add_collection(p)
        p = PatchCollection(circles, facecolors="red")
        ax.add_collection(p)
        plt.show()

    def loadImgs(self, imgids=[]):
        """Load images

        Args:
            imgids (list, optional): Integer image ids. Defaults to [].

        Returns:
            [numpy.ndarray]: Loaded images
        """
        imgids = imgids if _isArrayLike(imgids) else [imgids]
        print("imgids:", imgids)
        imgs = []
        for imgid in imgids:
            filename = self.imagepath / (imgid + ".png")
            print("filename:", filename)
            img = cv2.imread(str(filename))
            imgs.append(img)
        return imgs


if __name__ == "__main__":
    examplesplit = DOTA("/home/ashwin/Desktop/Projects/dotadevkit/example_split")
    imgids = examplesplit.getImgIds(catNms=["plane"])
    imgs = examplesplit.loadImgs(imgids)
    if imgs:
        for imgid in imgids:
            anns = examplesplit.loadAnns(imgId=imgid)
            examplesplit.showAnns(anns, imgid)
