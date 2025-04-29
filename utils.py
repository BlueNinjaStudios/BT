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


class binaryops:
    """utility class for binary conversion operations on UTF-8 encoding"""

    def toutf(num: int) -> str:
        """returns UTF-8 character in U+F0000 to U+FFFFF band as string"""

        #Check input for 0 <= num >= 65535 
        #Maybe assert
        if num < 0 or num > 65535:
            raise Exception("number to encode out of range")
        #base: f3 b0 80 80
        base = 0xf3b08080
        ans1 = num%(1<<6)
        ans2 = (num%(1<<12) - ans1)<<2
        ans3 = (num//(1<<12))<<16

        return bytes.fromhex(hex(base+ans1+ans2+ans3)[2:]).decode()

    def toint(character: str) -> int:
        """returns int encoded in UTF-8 character in U+F0000 to U+FFFFF band"""
        #add validity checks
        assert len(character) == 1
        base = 0xf3b08080
        byte = int(character.encode().hex(), 16) - base
        ans1 = byte%(1<<6)
        ans2 = ((byte>>8)%(1<<6))<<6
        ans3 = (byte>>16)<<12
        return(ans1+ans2+ans3)
    
    def iscodepoint(character: str) -> bool:
        """true if given character falls into the UTF-8 range: U+F0000 to U+FFFFF"""
        assert len(character) == 1
        num = int(character.encode().hex(), 16)
        return 4088430719 < num and num < 4089429952