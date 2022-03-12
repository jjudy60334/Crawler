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
def klook_activity_pipeline(country_id, size, schema_path):

    host = os.getenv('MongoHost')
    port = os.getenv('Mongoport')
    db = os.getenv('MongoDb')
    username = os.getenv('MongoUserName', None)
    password = os.getenv('MongoPassword', None)
    click.echo(f"{host}, {port}, {username}, {password}, {db}")
    scp = KlookActivityPipeline(
        country_id=country_id, size=int(size), schema_path=schema_path, host=host, port=int(port),
        username=username, password=password, db=db
    )
    scp.execute()
    click.echo("crawl activity loaded to mongo successfully!")


@click.command()
@click.option("--activity_ids")
@click.option("--size", default="50")
@click.option("--schema_path")
def klook_review_pipeline(activity_ids, size, schema_path):
    host = os.getenv('MongoHost')
    port = os.getenv('Mongoport')
    db = os.getenv('MongoDb')
    username = os.getenv('MongoUserName', None)
    password = os.getenv('MongoPassword', None)
    activity_ids = eval(activity_ids)
    scp = KlookReviewPipeline(
        activity_ids=activity_ids, size=int(size), schema_path=schema_path, host=host, port=int(port),
        username=username, password=password, db=db
    )
    scp.execute()
    click.echo("crawl review loaded to mongo successfully!")


cli.add_command(klook_activity_pipeline)
cli.add_command(klook_review_pipeline)
