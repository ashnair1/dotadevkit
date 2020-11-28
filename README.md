## DOTA Devkit 

![](https://github.com/ashnair1/dotadevkit/workflows/Build/badge.svg)
[![PyPi License](https://img.shields.io/pypi/v/dotadevkit?branch=master&label=PyPi%20Version&logo=PyPi&logoColor=ffffff&labelColor=306998&color=FFD43B&style=flat)](https://pypi.org/project/dotadevkit/)
[![Python Version](https://img.shields.io/pypi/pyversions/dotadevkit?+&label=Python&logo=Python&logoColor=ffffff&labelColor=306998&color=FFD43B&style=flat)](https://pypi.org/project/dotadevkit/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### About
This is a modified version of the original [DOTA_Devkit](https://github.com/CAPTAIN-WHU/DOTA_devkit). The devkit has had some issues regarding ease of installation and usage with the latter being a significant problem. This repo attemps to address these issues by providing a simple CLI for easier usage and cross-platform whls for easier installation. 

**Disclaimer**:  This repo was created post [9938855](https://github.com/CAPTAIN-WHU/DOTA_devkit/commit/99388551054be9a6dabb01c8bb2a7eb562d57b4f). The DOTA authors could update the original repo and/or add support for (possible) new versions of the DOTA dataset. While this repo will try to remain in sync with the original, users should rely on the original should the repos diverge. 

### Installation

```
pip install dotadevkit
```

### Usage
Once installed, you will have access to the `dotadevkit` CLI. Run `dotadevkit --help` or `dotadevkit <command> --help` for further details.
```
Usage: dotadevkit [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert    Convert tiled DOTA annotations to COCO format.
  evaluate   Run evaluation for both tasks on DOTA & DOTA 1.5.
  merge      Merges annotations according to DOTA Tasks.
  split      Splits images and annotations.
  visualise  Visualise annotations.
```

Your dataset directory should look as follows:

```markdown
.
├── example
│   ├── images
│   ├── labelTxt
│   ├── images.txt

``` 

Refer [example](./example) directory in this repo for a concrete example

 
#### Split

1. Split only images with 8 processes

```
 dotadevkit split \
        ./example/images \
        ./example_split/images \
        8 \
        --images
```

2. Split `images` and `labelTxt` into tiles of size 800 x 800 with overlap of 200 pixels with 8 processes

```
 dotadevkit split \
        ./example/ \
        ./example_split/ \
        8 \
        800 \
        200 
```

#### Merge

```
 dotadevkit merge \
        ./example_split/dota_dets \
        ./example_split/merged_dets \
        8
```

#### Evaluate

DOTA evaluation on specific task and dataset version.

```
 dotadevkit evaluate \
        ./example_split/merged_dets/Task1_{:s}.txt \
        ./example/labelTxt/{:s}.txt \
        ./example/images.txt \
        1.0
```

#### Visualise

Visualise images that have `plane` and `helicopter` categories.

```
 dotadevkit visualise \
        ./example_split/ \
        -cat plane -cat helicopter
```

#### Convert

Convert tiled DOTA annotations of specified version to MS-COCO format.

```
 dotadevkit convert \
        ./example_split/ \
        --version 1.0
```
