from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch import load


class RuT5SmallModel(object):

    def __init__(self):
        self.model_name = 'cointegrated/rut5-small'
        self.prefix = 'отгадай: '
        self.ans_pref = 'я думаю отгадка - '

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.model.load_state_dict(load('trained_lm.pth'))
        self.model.eval()

    def preprocess_function(self, examples):
        inputs = [self.prefix + doc or '' for doc in examples["riddle"]]
        model_inputs = self.tokenizer(inputs, max_length=1024, truncation=True)
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer([self.ans_pref + doc for doc in examples["answer"]], max_length=128, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def guess_the_riddle(self, sample):
        tokens = self.tokenizer(self.prefix + sample, return_tensors='pt').input_ids
        outputs = self.model.generate(tokens)
        prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return prediction