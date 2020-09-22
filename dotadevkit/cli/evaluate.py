import click
from dotadevkit.evaluate import task1 as t1, task2 as t2


@click.command()
@click.argument("detections", type=str)
@click.argument("annotations", type=str)
@click.argument("images", type=str)
@click.argument("version", type=str)
@click.option("--task1/--task2", default=True)
def evaluate(detections, annotations, images, version, task1):
    """
    \b
    Run evaluation for both tasks on DOTA & DOTA 1.5.

    \b
    Args:
        detections (str): Merged detections directory
        annotations (str): Ground truth
        images (str): Path to text file of image names
        version (str): DOTA version ["1.0", "1.5"]
        task1 (bool): Task1 (Oriented BBox)

    Returns:
        None
    """
    if task1:
        t1.evaluate(detections, annotations, images, version)
    else:
        t2.evaluate(detections, annotations, images, version)
