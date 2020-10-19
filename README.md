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
Once installed, you will have access to the `dotadev` CLI. Run `dotadev --help` or `dotadev <command> --help` for further details.
```
Usage: dotadev [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  evaluate  Run evaluation for both tasks on DOTA & DOTA 1.5.
  merge     Merges annotations according to DOTA Tasks.
  split     Splits images and annotations.

```

#### Evaluate
```
 dotadev evaluate \
        /path/to/detections/Task1_{:s}.txt \
        /path/to/dota/val/labelTxt/{:s}.txt \
        /path/to/text/file/of/image/names \
        1.0
```
 
#### Merge

```
 dotadev merge \
        /path/to/dota/data/ \
        /path/to/destination/directory/ \
        8
```

#### Split

Setting the `--images` flag only splits the images. If it is not set, both `images` and `labelTxt` undergo the split process.

```
 dotadev split \
        /path/to/dota/data/images \
        /path/to/destination/directory/ \
        8 \
        --images
```

