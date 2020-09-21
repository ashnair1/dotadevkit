import click
from dotadevkit.ops import DataSplitter, ImgSplitter


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=True))
@click.argument("num_process", default=1, type=int)
@click.argument("size", default=1024, required=False, type=int)
@click.argument("overlap", default=100, required=False, type=int)
@click.argument("threshold", default=0.7, required=False, type=float)
@click.argument("scale", default=1.0, required=False, type=float)
@click.option("--padding", default=True, type=bool, help="Pads tiles to be of same size")
@click.option("--images", is_flag=True, help="Splits only images")
def split(src, dst, size, overlap, threshold, scale, padding, num_process, images):
    """
    \b
    Splits images and annotations.

    \b
    Args:
        src (str): Source directory
        dst (str): Destination directory
        num_process (int): Num of threads.
        size (int): Tile size
        overlap (int): Overlap between tiles.
        threshold (float): Annotations below this threshold are removed.
        scale (float): Scale images to this factor before splitting
        padding (bool): True for padding tiles to be of same size.
        images (bool): True for splitting only images.

    Returns:
        None
    """
    if images:
        splitter = ImgSplitter(
            src,
            dst,
            subsize=size,
            gap=overlap,
            padding=padding,
            num_process=num_process,
        )
    else:
        splitter = DataSplitter(
            src,
            dst,
            subsize=size,
            gap=overlap,
            thresh=threshold,
            padding=padding,
            num_process=num_process,
        )

    splitter.splitdata(scale)


if __name__ == "__main__":
    split()
