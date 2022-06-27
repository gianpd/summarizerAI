import torch
import intel_extension_for_pytorch as ipex
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from transformers import logging as T_LOGGER
T_LOGGER.set_verbosity_error()


class InferenceModel:
    def __init__(self, checkpoint: str, quantize: bool = False):
        torch.set_num_threads(1) # manage threads with gunicorn 
        torch.set_grad_enabled(False) # inference mode: do not need grad

        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)