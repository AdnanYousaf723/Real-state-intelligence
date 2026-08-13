import click
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reli.database.connection import Base, DATABASE_URL, connect_args
from reli.pipeline.runner import PipelineRunner
from reli.ingestion.csv_source import CSVDataSource
from reli.ingestion.attom_source import ATTOMDataSource

@click.group()
def main():
    """RELI - Real Estate Lead Intelligence CLI"""
    pass

@main.command()
def init_db():
    """Initialize the database"""
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    click.echo("Database initialized.")

@main.command()
@click.option('--source', default='sample_csv', help='Data source to run (sample_csv or attom)')
def pipeline_run(source):
    """Run the pipeline"""
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    runner = PipelineRunner(db)
    if source == 'sample_csv':
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(base_dir, "data", "sample", "properties.csv")
        data_source = CSVDataSource(file_path=file_path)
    elif source == 'attom':
        data_source = ATTOMDataSource()
    else:
        click.echo(f"Unknown source: {source}")
        return
        
    ctx = runner.run(data_source, source)
    click.echo(f"Pipeline completed. Status: SUCCESS. Leads generated: {ctx.leads_generated}")

if __name__ == '__main__':
    main()
