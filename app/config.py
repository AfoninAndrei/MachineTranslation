import torch


# Config that serves all environment
GLOBAL_CONFIG = {
    "MODEL_PATH": "../model/best_model.pt",
    "VOCAB_PATH": "../model/vocab.joblib",
    "TOKEN_TRANSFORM_PATH": "../model/token_transform.joblib",
    "UNK_IDX": 0, 
    "PAD_IDX": 1, 
    "BOS_IDX": 2, 
    "EOS_IDX": 3,
    "SRC_LANGUAGE": "en",
    "TGT_LANGUAGE": "ru",
}


def get_config() -> dict:
    """
    Get config
    """

    config = GLOBAL_CONFIG.copy()
    config['DEVICE'] = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    return config


CONFIG = get_config()

if __name__ == '__main__':
    # for debugging
    import json
    print(json.dumps(CONFIG, indent=4))