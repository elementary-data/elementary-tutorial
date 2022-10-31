import click
from pyfiglet import Figlet

from elementary_tutorial.workflows.generate_data import generate_data


f = Figlet(font="slant")
click.echo(f.renderText("Elementary Tutorial"))


@click.group
def cli():
    pass


@cli.command()
def generate_tutorial_data():
    generate_data()


if __name__ == "__main__":
    cli()
