"""split.py
Split the raw data into a train set and a test set
"""
import os
import click
import pandas as pd
from sklearn import model_selection

@click.command()
@click.argument("test_ratio", type=click.FLOAT)
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("train_file", type=click.Path())
@click.argument("test_file", type=click.Path())
@click.option("--seed", type=click.INTEGER, default=7, help="Random # seed")
def split(test_ratio, input_file, train_file, test_file, seed):
    """
    Randomly split INPUT_FILE into TRAIN_FILE and TEST_FILE
    with TEST_RATIO between 0.0 and 1.0
    """
    logger = logging.getLogger(__name__)
    logger.info("Reading %s", input_file)
    df = pd.read_csv(input_file)
    logger.info("Splitting off %.2f of %s as test data", test_ratio, input_file)
    test = df.sample(frac=ratio, random_state=seed)
    train = df.drop(test.index)
    logger.info("Writing train data to %", train_file)
    train.to_csv(train_file, index=False)
    logger.info("Writing test data to %", test_file)
    test.to_csv(test_file, index=False)

def main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    dotenv.load_dotenv(dotenv.find_dotenv())
    split()

if __name__ == "__main__":
    main()
