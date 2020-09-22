## DOTA Devkit 

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ashnair1/DOTA_devkit/Build)
![PyPI](https://img.shields.io/pypi/v/dotadevkit)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A fork of the original [DOTA_Devkit](https://github.com/CAPTAIN-WHU/DOTA_devkit) that provides a CLI for easier usage an publically available whls for wasier installation. 

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

