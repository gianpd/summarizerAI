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
        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
        model.to(ipex.DEVICE).eval()
        model = torch.jit.script(model)

        self.model = model


    def predict(self, message: str): 
        with torch.no_grad():
            input_ids = self.tokenizer.encode(message, return_tensor='pt')
            preds = self.model.generate(
                input_ids,
                do_sample=True,
                max_length=142,
                num_beams=3,
                no_repeate_ngram_size=3,
                early_stopping=True
            )
            
        return self.tokenizer.decode(preds[0], skip_special_tokens=True)


        