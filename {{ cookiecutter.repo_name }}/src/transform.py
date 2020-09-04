"""transform.py
fit a transformer on test data to transform
test and training data.
"""
import os
import logging
import dotenv
import click
import joblib
from sklearn import preprocessing, impute, pipeline, compose

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path)
@click.option("pipeline_file", type=click.Path)
@click.option("--fit/--no-fit", default=False, help="Fit the transformer")
def transform(input_file, output_file, pipeline_file, fit):
    """
    Transform INPUT_FILE to OUTPUT_FILE using serialized PIPELINE_FILE.
    If --fit specified, a pipeline is created, fitted on the data,
    and written to PIPELINE_FILE.
    Otherwise, a pipeline is read from PIPELINE_FILE and used to transform
    the data only.
    """
    logger = logging.getLogger(__name__)
    logger.info("Reading %s", input_file)

    if fit:
        # create the pipeline, fit_transform it on the data, and
        # save to pipeline_file
        joblib.dump(pipeline, pipeline_file)
    else:
        # read and deserialize the pipeline from pipeline_file
        pipeline = joblib.load(pipeline_file)

def main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    dotenv.load_dotenv(dotenv.find_dotenv())
    transform()

if __name__ == "__main__":
    main()

