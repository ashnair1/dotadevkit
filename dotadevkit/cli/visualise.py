import click
from dotadevkit.ops.Visualise import DOTA


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.option("-cat", "--categories", multiple=True, help="Specify categories")
def visualise(src, categories):
    """
    \b
    Visualise annotations.

    \b
    Args:
        src (str): Source directory
        categories (str): Categories

    Returns:
        None
    """
    dota = DOTA(src)
    imgids = dota.getImgIds(catNms=categories)
    imgs = dota.loadImgs(imgids)
    if imgs:
        for imgid in imgids:
            try:
                anns = dota.loadAnns(imgId=imgid)
                dota.showAnns(anns, imgid)
            except KeyboardInterrupt:
                break
