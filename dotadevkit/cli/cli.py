import click
from dotadevkit.cli import merge, split, evaluate


@click.group()
def cli():
    pass


cli.add_command(evaluate)
cli.add_command(merge)
cli.add_command(split)

if __name__ == "__main__":
    cli()
