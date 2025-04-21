import click

from elementary_tutorial.workflows.generate_data import generate_data


ELEMENTARY_LOGO = r"""
    ________                          __                  
   / ____/ /__  ____ ___  ___  ____  / /_____ ________  __
  / __/ / / _ \/ __ `__ \/ _ \/ __ \/ __/ __ `/ ___/ / / /
 / /___/ /  __/ / / / / /  __/ / / / /_/ /_/ / /  / /_/ / 
/_____/_/\___/_/ /_/ /_/\___/_/ /_/\__/\__,_/_/   \__, /  
                                                 /____/   
  ______      __             _       __
 /_  __/_  __/ /_____  _____(_)___ _/ /
  / / / / / / __/ __ \/ ___/ / __ `/ / 
 / / / /_/ / /_/ /_/ / /  / / /_/ / /  
/_/  \__,_/\__/\____/_/  /_/\__,_/_/   
"""
click.echo(f"{ELEMENTARY_LOGO}\n")


@click.group
def cli():
    pass


@cli.command()
def generate_tutorial_data():
    generate_data()


if __name__ == "__main__":
    cli()
