import sys
import torch
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from translate import translate
from schema import InferenceInput
from utils import load_modules


# Initialize API Server
app = FastAPI(
    title="Translation EN-RU",
    description="Seq2Seq transformer",
    version="0.0.1"
)


@app.on_event("startup")
def load_model():
    """
    Load model and text preprocessing modules.
    """

    # Initialize the model, vocab, text transformer
    pkg = load_modules()

    # add model and other preprocess tools too app state
    app.package = {key: pkg[key] for key in pkg}


@app.get('/')
def health():
    """
    Get deployment information
    """
    return "API is working!"


@app.get('/about')
def show_about():
    return {
            "sys.version": sys.version,
            "torch.__version__": torch.__version__,
            "torch.cuda.is_available()": torch.cuda.is_available()
        }


@app.post('/predict')
def predict(body: InferenceInput):
    """
    Perform prediction on input data
    """

    logger.info('API predict called')
    logger.info(f'input in EN: {body}')

    # run model inference
    y = translate(app.package, body.input)

    logger.info(f'output in RU: {y}')

    return {"result": y}


if __name__ == '__main__':
    # server api
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
