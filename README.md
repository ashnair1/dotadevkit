
## DOTA Devkit 

A fork of the original [DOTA_Devkit](https://github.com/CAPTAIN-WHU/DOTA_devkit) that provides a CLI for easier usage. 

## Functions

The code is useful for <a href="http://captain.whu.edu.cn/DOTAweb/">DOTA<a> or
<a href="http://captain.whu.edu.cn/ODAI/">ODAI<a>. The code provide the following function
<ul>
    <li>
        Load and image, and show the bounding box on it.
    </li>
    <li>
        Evaluate the result.
    </li>
    <li>
        Split and merge the picture and label.
    </li>
</ul>

### What is DOTA?
<p>
Dota is a large-scale dataset for object detection in aerial images. 
It can be used to develop and evaluate object detectors in aerial images. 
We will continue to update DOTA, to grow in size and scope and to reflect evolving real-world conditions.
Different from general object detectin dataset. Each instance of DOTA is labeled by an arbitrary (8 d.o.f.) quadrilateral.
For the detail of <strong style="color:blue"> DOTA-v1.0</strong>, you can refer to our 
<a href="https://arxiv.org/abs/1711.10398">paper</a>.
</p>

### What is DOAI?

[DOAI2019](https://captain-whu.github.io/DOAI2019) is a contest of Detecting Objects in Aerial Images on [CVPR'2019]("http://cvpr2019.thecvf.com/"). It is based on DOTA-v1.5.



[DOAI2018](https://captain-whu.github.io/ODAI) is a contest of object detetion in aerial images on [ICPR'2018]("http://www.icpr2018.org/"). It is based on [DOTA-v1]("http://captain.whu.edu.cn/DOTAweb/"). The contest is closed now. 


### Installation
1. Install swig
```
    sudo apt-get install swig
```
2. Setup library 
```
    python setup.py install
```

### Usage
1. Evaluate:

```
 dotadev evaluate \
        /path/to/detections/Task1_{:s}.txt \
        /path/to/dota/val/labelTxt/{:s}.txt \
        /path/to/text/file/of/image/names \
        1.0
```

2. Merge

```
 dotadev merge \
        /path/to/dota/data/ \
        /path/to/destination/directory/ \
        8
```

3. Split

Setting the `--images` flag only splits the images.

```
 dotadev split \
        /path/to/dota/data/images \
        /path/to/destination/directory/ \
        8 \
        --images
```

