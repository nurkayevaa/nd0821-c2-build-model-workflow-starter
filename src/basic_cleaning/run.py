#!/usr/bin/env python
"""
downloading sample uploading cleanin artifact
"""
import argparse
import logging
import wandb


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
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)
    
    
    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    
    
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
