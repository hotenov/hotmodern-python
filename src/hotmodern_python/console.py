import textwrap

import click
import requests


from . import __version__, wikipedia



@click.command()
@click.version_option(version=__version__)
def main():
    """The hotmodern Python project."""
    try:
        data = wikipedia.random_page()
    except requests.exceptions.HTTPError:
        print("API endpoint is unavailable, check API URL or try later")
    else:
        title = data["title"]
        extract = data["extract"]
        
        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))
