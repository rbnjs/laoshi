import click
from laoshi.converter import Converter


@click.group()
def cli_group():
    pass


@cli_group.command(help="Convert characters")
@click.option(
    "-t",
    "--to",
    type=click.Choice(["traditional", "simplified", "pinyin"]),
)
@click.argument("word")
def cc(to: str, word: str) -> str:
    match to:
        case "traditional":
            return click.echo(Converter.to_traditional(word))
        case "simplified":
            return click.echo(Converter.to_simplified(word))
        case "pinyin":
            return click.echo(Converter.to_pinyin(word))


if __name__ == "__main__":
    cli_group()
