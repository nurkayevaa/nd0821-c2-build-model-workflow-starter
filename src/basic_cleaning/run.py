#!/usr/bin/env python
"""
downloading sample uploading cleanin artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    
    ######################
    # YOUR CODE HERE     #
    ######################
    run = wandb.init(project="nyc_airbnb", job_type="clean_data")

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_csv(artifact_path)

    # Drop the duplicates
    logger.info("Removing outliers")
    # Drop outliers

    
    # Drop outliers

   
    df.to_csv("clean_sample.csv", index=False)
    
    artifact = wandb.Artifact(
             args.output_artifact,
             type=args.output_type,
             description=args.output_description,
             )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


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
