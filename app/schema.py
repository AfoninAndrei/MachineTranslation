from pydantic import BaseModel, Field


class InferenceInput(BaseModel):
    """
    Input to the model
    """
    input: str = Field(..., example="This is text in english", title='Text in English to be translated')


class InferenceResult(BaseModel):
    """
    Inference output from the model
    """
    output: str = Field(..., example='А че где?', title='Translated text of the input in Russian')
