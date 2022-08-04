"""
{{cookiecutter.short_description}}

{{cookiecutter.long_description}}
"""
import argparse
import os

import mlflow
from strictyaml import load

_steps = ["data_ingest"]


def main(args):

    with open(file=args.config, mode="r", encoding="utf-8") as conf_file:
        config = load(conf_file.read()).data

    os.environ["MLFLOW_TRACKING_URI"] = config["main"]["MLFLOW_TRACKING_URI"]
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = config["main"]["MLFLOW_S3_ENDPOINT_URL"]

    # Steps to execute
    config["main"]["steps"] = args.steps
    steps_par = config["main"]["steps"]
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    if "data_ingest" in active_steps:
        _ = mlflow.run(
            uri=os.path.join("components", "data_ingest"),
            entry_point="main",
            experiment_name=config["main"]["experiment_name"],
            parameters={
                "raw_data": config["data_ingest"]["raw_data"],
            },
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=str,
        help="Configuration environment",
    )

    parser.add_argument(
        "--steps",
        type=str,
        help="Select steps of ML pipeline",
    )

    args = parser.parse_args()

    main(args)
