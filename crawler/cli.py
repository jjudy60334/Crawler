import click
import os
from crawler.pipelines import KlookActivityPipeline, KlookReviewPipeline


@click.group()
def cli():
    pass


@click.command()
@click.option("--country_id")
@click.option("--size", default="default")
@click.option("--schema_path")
@click.option("--schema_path")
@click.option("--mongo_host")
@click.option("--mongo_port")
@click.option("--mongo_db")
@click.option("--mongo_username")
@click.option("--mongo_password")
def klook_activity_pipeline(
        country_id, size, schema_path, mongo_host, mongo_port, mongo_db, mongo_username=None,
        mongo_password=None):

    click.echo(f"{mongo_host}, {mongo_port}, {mongo_username}, {mongo_password}, {mongo_db}")
    scp = KlookActivityPipeline(
        country_id=country_id, size=int(size), schema_path=schema_path, host=mongo_host, port=int(mongo_port),
        username=mongo_username, password=mongo_password, db=mongo_db
    )
    scp.execute()
    click.echo("crawl activity loaded to mongo successfully!")


@click.command()
@click.option("--activity_ids")
@click.option("--size", default="50")
@click.option("--schema_path")
@click.option("--mongo_host")
@click.option("--mongo_port")
@click.option("--mongo_db")
@click.option("--mongo_username")
@click.option("--mongo_password")
def klook_review_pipeline(
        activity_ids, size, schema_path, mongo_host, mongo_port, mongo_db, mongo_username=None,
        mongo_password=None):

    activity_ids = eval(activity_ids)
    scp = KlookReviewPipeline(
        activity_ids=activity_ids, size=int(size), host=mongo_host, port=int(mongo_port),
        username=mongo_username, password=mongo_password, db=mongo_db
    )
    scp.execute()
    click.echo("crawl review loaded to mongo successfully!")


cli.add_command(klook_activity_pipeline)
cli.add_command(klook_review_pipeline)
