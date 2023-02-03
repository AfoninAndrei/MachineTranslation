from config import CONFIG
from joblib import load
from Model import Seq2SeqTransformer
import torch
from typing import List
import os


def load_modules() -> dict:
    """
    return the absolute path of a relative path
    """
    # load token transformations (spacy tokenizers)
    token_transform = load(abs_path(CONFIG['TOKEN_TRANSFORM_PATH']))

    # load vocabularly block (torchtext.vocab)
    vocab_transform = load(abs_path(CONFIG['VOCAB_PATH']))

    # load model for prediction
    model = Seq2SeqTransformer(2, 2, 128, 2, 84617, 185478, 128)
    model.load_state_dict(torch.load(abs_path(CONFIG['MODEL_PATH']),
                                     map_location=torch.device(CONFIG['DEVICE'])))
    model.eval()

    # full pipeline of text preprocessing
    text_transform = create_text_transform(token_transform, vocab_transform)

    return {'model': model,
            'vocab': vocab_transform,
            'token_transform': token_transform,
            'transform': text_transform}


def create_text_transform(token_transform, vocab_transform):
    # helper function to club together sequential operations
    def sequential_transforms(*transforms):
        def func(txt_input):
            for transform in transforms:
                txt_input = transform(txt_input)
            return txt_input
        return func

    # function to add BOS/EOS and create tensor for input sequence indices
    def tensor_transform(token_ids: List[int]):
        return torch.cat((torch.tensor([CONFIG['BOS_IDX']]),
                        torch.tensor(token_ids),
                        torch.tensor([CONFIG['EOS_IDX']])))
    
    text_transform = {}
    for ln in [CONFIG['SRC_LANGUAGE'], CONFIG['TGT_LANGUAGE']]:
        text_transform[ln] = sequential_transforms(token_transform[ln], #Tokenization
                                                   vocab_transform[ln], #Numericalization
                                                   tensor_transform)    #Add BOS/EOS and create tensor
    
    return text_transform


def abs_path(p: str) -> str:
    """
    return the absolute path of a relative path
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), p)