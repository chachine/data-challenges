
import glob
import os
import time
import pickle

from colorama import Fore, Style

from tensorflow import keras
from tensorflow.keras import Model


def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    print(Fore.BLUE + "\nSave model to local disk..." + Style.RESET_ALL)

    suffix = time.strftime("%Y%m%d-%H%M%S")

    # save params
    if params is not None:
        params_path = os.path.join(os.environ.get("LOCAL_REGISTRY_PATH"), "params", suffix + ".pickle")

        print(f"- params path: {params_path}")

        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics
    if metrics is not None:
        metrics_path = os.path.join(os.environ.get("LOCAL_REGISTRY_PATH"), "metrics", suffix + ".pickle")

        print(f"- metrics path: {metrics_path}")

        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # save model
    if model is not None:
        model_path = os.path.join(os.environ.get("LOCAL_REGISTRY_PATH"), "models", suffix + ".pickle")

        print(f"- model path: {model_path}")

        model.save(model_path)

    print("\n✅ data saved locally")


def load_model(stage="None") -> Model:
    """
    load the latest saved model
    """

    print(Fore.BLUE + "\nLoad model from local disk..." + Style.RESET_ALL)

    # get latest model version
    model_directory = os.path.join(os.environ.get("LOCAL_REGISTRY_PATH"), "models")

    model_path = sorted(glob.glob(f"{model_directory}/*"))[-1]
    print(f"- path: {model_path}")

    model = keras.models.load_model(model_path)
    print("\n✅ model loaded from disk")

    return model
