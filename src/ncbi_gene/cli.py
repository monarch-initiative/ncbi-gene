"""Command line interface for NCBI Gene."""
import logging

from pathlib import Path

from kghub_downloader.download_utils import download_from_yaml
from koza.cli_utils import transform_source
import typer

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.callback()
def callback(
        version: bool = typer.Option(False, "--version", is_eager=True),
        verbose: int = typer.Option(True, help="Verbosity level: 0 (warning), 1 (info), 2+ (debug)"),
        quiet: bool = typer.Option(False, help="Suppress logging output")
    ):
    """NCBI Gene CLI."""
    if version:
        from ncbi_gene import __version__
        typer.echo(f"NCBI Gene version: {__version__}")
        raise typer.Exit()


    if verbose:
        logger.setLevel(level=logging.DEBUG)
    elif verbose is None:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    logger.info(f"Logger {logger.name} set to level {logger.level}")


@app.command()
def download(force: bool = typer.Option(False, help="Force download of data, even if it exists")):
    """Download data for NCBI Gene."""
    typer.echo("Downloading data for NCBI Gene...")
    download_config = Path(__file__).parent / "download.yaml"
    download_from_yaml(yaml_file=download_config, output_dir=".", ignore_cache=force)


@app.command()
def transform(
    output_dir: str = typer.Option("output", help="Output directory for transformed data"),
    row_limit: int = typer.Option(None, help="Number of rows to process"),
):
    """Run the Koza transform for NCBI Gene."""
    typer.echo("Transforming data for NCBI Gene...")
    transform_code = Path(__file__).resolve().parent / "transform.yaml"
    transform_source(
        source=str(transform_code),
        output_dir=output_dir,
        output_format="tsv",
        row_limit=row_limit,
        verbose=(logger.level <= logging.INFO),
    )
    

if __name__ == "__main__":
    app()
