import click
from pipelines import KlookActivityPipeline, KlookReviewPipeline


@click.command()
@click.option("--contry_id")
@click.option("--size", default="default")
@click.option("--schema_path")
@click.option("--host")
@click.option("--port")
@click.option("--db")
def klook_activity_pipeline(contry_id, size, schema_path, host, port, db, username=None, password=None):
    scp = KlookActivityPipeline(
        contry_id, size, schema_path, host, port, db, username=None, password=None
    )
    scp.execute()
    click.echo(f"crawl loaded to mongo successfully")
