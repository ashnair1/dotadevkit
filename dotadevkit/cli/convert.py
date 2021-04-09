import click
from dotadevkit.ops.CocoConvert import DOTA2COCO
from pathlib import Path


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.option("-v", "--version", default="1.0", type=str)
def convert(src, version):
    """
    \b
    Convert tiled DOTA annotations to COCO format.

    \b
    Args:
        src (str): Source directory containing tiled images & labels
        version (str): Dataset version (1.0, 1.5, 2.0)

    Returns:
        None
    """
    src = Path(src)
    DOTA2COCO(src, src / f"DOTA_{version}.json", version)
