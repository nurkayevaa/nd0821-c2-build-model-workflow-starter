#!/usr/bin/env python
import argparse
import logging
import os

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="clean_data")

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_parquet(artifact_path)

    # Drop the duplicates
    logger.info("Removing outliers")
    # Drop outliers

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging artifact")
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--output_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Description for the artifact",
        required=True,
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
