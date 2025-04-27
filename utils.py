from collections import Counter

class wordops:
    """utility class for operations on words"""
    def subwords(word:str, minlen=2) -> list[str]:
        res = []
        for i in range(len(word)):
            for j in range(i+minlen, len(word)+1):
                res.append(word[i:j])
        return res


class counterops:
    """utility class for operations on counter"""
    
    def scalesubwords(subwords: Counter, factor=1.0):
        for elem in subwords:
            subwords[elem] *= (len(elem)-1) * factor