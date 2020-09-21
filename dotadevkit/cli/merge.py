import click
from dotadevkit.ops import mergebypoly, mergebyrec


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=True))
@click.argument("num_process", default=1, type=int)
@click.argument("nms_thresh", default=0.3, required=False, type=float)
@click.option("--task1/--task2", default=True)
def merge(src, dst, num_process, nms_thresh, task1):
    """
    \b
    Merges annotations according to DOTA Tasks.
    Task 1 = Oriented Bounding Box
    Task 2 = Horizontal Bounding Box

    \b
    Args:
        src (str): Source directory
        dst (str): Destination directory
        num_process (int): Num of threads
        nms_thresh (float): NMS threshold
        task1 (bool): Task1 (Oriented BBox)

    Returns:
        None
    """
    if task1:
        mergebypoly(src, dst, num_process, nms_thresh)
    else:
        mergebyrec(src, dst, nms_thresh)
