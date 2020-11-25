import click
from dotadevkit.cli import merge, split, evaluate, visualise, convert


@click.group()
def cli():
    pass


cli.add_command(convert)
cli.add_command(evaluate)
cli.add_command(merge)
cli.add_command(split)
cli.add_command(visualise)

if __name__ == "__main__":
    cli()
