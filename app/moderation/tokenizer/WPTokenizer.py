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

    def tokenize(self, text, pad_to_max_length=False, truncation=False, 
                 max_length=None, return_tensors=None, frac = None):
        if (frac == None):
            frac = max_length
        if (self.vocab == []):
            raise ValueError("Vocabulary is empty")
            
        if not(max_length):
            if (pad_to_max_length):
                raise ValueError("Asking to pad to max_length but no maximum length is provided and\
                the model has no predefined maximum length. Default to no padding.")
            if (truncation):
                raise ValueError("Asking to truncate to max_length but no maximum length is provided\
                and the model has no predefined maximum length. Default to no truncation.")
        
        tokens = []
        attention_mask = []
        
        if (text == ""):
            tokens = [101, 102]
            attention_mask = [1, 1]
            return {'input_ids' : tokens,
                    'attention_mask' : attention_mask}
        
        basic_tokenize = text.split()
        wp_tokens = []

        for i in range(len(basic_tokenize)):
            word = basic_tokenize[i]
            word_tokens = self.tokenize_word(word)
            wp_tokens += word_tokens

        attention_mask = [1 for i in range(len(wp_tokens))]
            
        tokens = [self.vocab.index(token) for token in wp_tokens]
        
        batch = {
                'input_ids_batch' : [],
                'attention_mask_batch' : []
                }
        
        batch_size = len(tokens) // frac
        for k in range(batch_size+1):
            if (truncation):
                batch['input_ids_batch'].append([101] + tokens[k * (frac-2) : (k + 1) * frac-2] + [102])
                batch['attention_mask_batch'].append(attention_mask[k * (frac-2) : (k + 1) * frac-2] + [1, 1])
            if (pad_to_max_length):
                batch['input_ids_batch'][k] += [0 for _ in range(max_length - len(batch['input_ids_batch'][k]))]
                batch['attention_mask_batch'][k] += [0 for _ in range(max_length - len(batch['attention_mask_batch'][k]))]
            else:
                batch['input_ids_batch'].append([101] + tokens + [102])
                batch['attention_mask_batch'].append(attention_mask + [1, 1])

        if (return_tensors):
            if (return_tensors=="np"):
                batch['input_ids_batch'] = np.asarray(batch['input_ids_batch']).astype('int64')
                batch['attention_mask_batch'] = np.array(batch['attention_mask_batch']).astype('int64')
               
        return batch
    
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
