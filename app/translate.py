import torch
from config import CONFIG

# During training, we need a subsequent word mask that will prevent 
# model to look into the future words when making predictions.
def generate_square_subsequent_mask(sz):
    mask = (torch.triu(torch.ones((sz, sz), device=CONFIG['DEVICE'])) == 1).transpose(0, 1)
    mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
    return mask


# function to generate output sequence using greedy algorithm
def greedy_decode(model, src, src_mask, max_len, start_symbol):
    src = src.to(CONFIG['DEVICE'])
    src_mask = src_mask.to(CONFIG['DEVICE'])

    memory = model.encode(src, src_mask)
    ys = torch.ones(1, 1).fill_(start_symbol).type(torch.long).to(CONFIG['DEVICE'])
    for i in range(max_len-1):
        memory = memory.to(CONFIG['DEVICE'])
        tgt_mask = (generate_square_subsequent_mask(ys.size(0))
                    .type(torch.bool)).to(CONFIG['DEVICE'])
        out = model.decode(ys, memory, tgt_mask)
        out = out.transpose(0, 1)
        prob = model.generator(out[:, -1])
        _, next_word = torch.max(prob, dim=1)
        next_word = next_word.item()

        ys = torch.cat([ys,
                        torch.ones(1, 1).type_as(src.data).fill_(next_word)], dim=0)
        if next_word == CONFIG['EOS_IDX']:
            break
    return ys


# actual function to translate input sentence into target language
def translate(pkg: dict, src_sentence: str):
    model = pkg['model']
    vocab = pkg['vocab']
    transform = pkg['transform']
    model.eval()
    src = transform[CONFIG['SRC_LANGUAGE']](src_sentence).view(-1, 1)
    num_tokens = src.shape[0]
    src_mask = (torch.zeros(num_tokens, num_tokens)).type(torch.bool)
    tgt_tokens = greedy_decode(
        model,  src, src_mask, max_len=num_tokens + 5, start_symbol=CONFIG['BOS_IDX']).flatten()
    return " ".join(vocab[CONFIG['TGT_LANGUAGE']].lookup_tokens(list(tgt_tokens.cpu().numpy()))).replace("<bos>", "").replace("<eos>", "")