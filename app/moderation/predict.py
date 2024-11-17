import re
from pathlib import Path

import numpy as np
import onnxruntime as ort
import demoji

from app.moderation.tokenizer.WPTokenizer import WordPieceTokenizer
from app.config import MODEL_PATH, VOCAB_PATH


current_file = Path(__file__)


def clean_text(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub("", text)
    text = demoji.replace(text)
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9.,\-()!?: ]', '', text)
    return text


onnx_path = current_file.parent / MODEL_PATH
vocab_path = current_file.parent / VOCAB_PATH
ort_session = ort.InferenceSession(onnx_path)

tokenizer = WordPieceTokenizer(vocab_path=vocab_path)


def onnx_predict(sample_text):
    sample_text = clean_text(sample_text)
    inputs = tokenizer.tokenize(sample_text, max_length=500, pad_to_max_length=True, truncation=True, return_tensors='np')
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]
    
    ort_inputs = {
        ort_session.get_inputs()[0].name: input_ids,
        ort_session.get_inputs()[1].name: attention_mask,
        ort_session.get_inputs()[2].name: token_type_ids
        }
    ort_outs = ort_session.run(None, ort_inputs)
    
    logits = ort_outs[0]
    predicted_class_id = np.argmax(logits)
    
    return predicted_class_id
