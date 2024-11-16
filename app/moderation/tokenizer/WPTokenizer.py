import numpy as np


class WordPieceTokenizer():
    def __init__(self, vocab = None, vocab_path = None):
        self.vocab = []
        
        if (vocab):
            self.vocab = vocab
        if (vocab_path):
            with open(vocab_path, encoding='utf8') as f:
                vocab = f.readlines()
                self.vocab = [token[:-1] for token in vocab]
                
        self.punct = '!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    def tokenize(self, text_samples, pad_to_max_length=False, truncation=False, max_length=None, return_tensors=None):
        if (type(text_samples) == str):
            text_samples = [text_samples]

        if (self.vocab == []):
            raise ValueError("Vocabulary is empty")

        if not(max_length):
            if (pad_to_max_length):
                raise ValueError("Asking to pad to max_length but no maximum length is provided and\
                the model has no predefined maximum length. Default to no padding.")
            if (truncation):
                raise ValueError("Asking to truncate to max_length but no maximum length is provided\
                and the model has no predefined maximum length. Default to no truncation.")

        token_samples = []
        attention_mask_samples = []
        token_type_ids = []

        for k, text in enumerate(text_samples):
            if (text == ""):
                token_samples.append([101, 102])
                attention_mask_samples.append([1, 1])
                token_type_ids([k, k])

            basic_tokenize = text.split()
            wp_tokens = []

            for i in range(len(basic_tokenize)):
                word = basic_tokenize[i]
                word_tokens = self.tokenize_word(word)
                wp_tokens += word_tokens

            attention_mask = [1 for i in range(len(wp_tokens))]

            tokens = [self.vocab.index(token) for token in wp_tokens]
            token_samples.append(tokens)
            attention_mask_samples.append(attention_mask)

        for i in range(len(token_samples)):
            if (truncation):
                token_samples[i] = token_samples[i][:max_length - 2]
                attention_mask_samples[i] = attention_mask_samples[i][:max_length - 2]

            token_samples[i] = [101] + token_samples[i] + [102]
            attention_mask_samples[i] += [1, 1]
            if (pad_to_max_length):
                token_samples[i] += [0 for _ in range(max_length - len(token_samples[i]))]
                attention_mask_samples[i] += [0 for _ in range(max_length - len(attention_mask_samples[i]))]

            token_type_ids.append([i for _ in range(len(token_samples[i]))])
        if (return_tensors):
            if (return_tensors=="np"):
                token_samples = np.asarray(token_samples).astype('int64')
                attention_mask_samples = np.asarray(attention_mask_samples).astype('int64')
                token_type_ids = np.asarray(token_type_ids).astype('int64')

        output = {'input_ids' : token_samples, 'attention_mask' : attention_mask_samples, 'token_type_ids' : token_type_ids}

        return output

    def tokenize_word(self, word):
        word_tokens = []
        while len(word) > 0:
            i = len(word)
            while i > 0 and word[:i] not in self.vocab:
                i -= 1
            if i == 0:
                return ["[UNK]"]

            word_tokens.append(word[:i])
            
            prev_was_punct = False
            if (len(word[:i]) == 1):
                if (word[:i] in self.punct):
                    prev_was_punct = True
                
            word = word[i:]
            if len(word) > 0:
                while ((word != "") and (word[0] in self.punct) and (word[0] != '#')):
                    word_tokens.append(word[0])
                    word = word[1:]
                    prev_was_punct = True
                if not(prev_was_punct):
                    word = f"##{word}"
        return word_tokens
