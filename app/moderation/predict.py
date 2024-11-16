from torch import no_grad
from transformers import BertForSequenceClassification, BertTokenizer

from app.config import MODEL_PATH


model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)


def predict(input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    with no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = logits.argmax(dim=1).item()

    return predicted_class
