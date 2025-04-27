from tokenizer import *
from utils import *
from collections import Counter

"""proof of concept tokenizer to be upgraded"""
class poc_tokenizer(tokenizer):

    def __init__(self, json_name: str):
        """initialize class and create source file"""
        self.json_source = json_name
        
        """check for existence of same file"""
        try:
            with open(self.json_source + ".json", "x") as file:
                pass
        except:
            # error handling
            pass
    
    def train(self, input_file: str):
        """generates encoding based on the selected input file
           and saves encoding to json source file"""
        c = self._parse(input_file)
        return self._parse_subword(c)


    def _parse(self, input_file: str) -> Counter:
        """parse input file into word Counter"""
        words = Counter()
        with open(input_file, "r") as f:
            for word in f.read().split():
                words[word] += 1
        return words
        
    def _parse_subword(self, words: Counter) -> Counter:
        """parse word counter into subwords"""
        tokens = Counter()
        for word in words:
            cnt = words[word]
            tkn = Counter(wordops.subwords(word))
            for subword in tkn:
                tkn[subword] *= cnt
            tokens.update(tkn)
        return tokens


tk = poc_tokenizer("poc_tk")
C = tk.train("input.txt")
print(C.most_common(100))
counterops.scalesubwords(C)
print(C.most_common(100))
