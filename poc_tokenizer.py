from tokenizer import *
from utils import *
from collections import Counter
import json
from tqdm import tqdm

"""proof of concept tokenizer to be upgraded"""
class poc_tokenizer(tokenizer):

    def __init__(self, json_name: str):
        """initialize class and create source file"""
        self.json_source = json_name + ".json"
        self.tokens = []
        
        """check for existence of same file"""
        try:
            #with open(self.json_source, "x") as file:
                pass
        except:
            # error handling
            
            pass

    # Add getters and setters

    
    def load(self):
        """load previously analysed configuration"""
        with open(self.json_source, "r") as file:
            self.tokens = json.load(file)
        return self.tokens
    

    def train(self, input_file: str):
        """generates encoding based on the selected input file
           and saves encoding to json source file"""
        tokens = []
        words = self._parse(input_file)

        for _ in tqdm(range(2000)):
            subwords = self._parse_subword(words)
            counterops.scalesubwords(subwords)
            tkn, _ = subwords.most_common(1)[0]

            #Check for code points
            polishedtkn = tkn
            running = True
            strpointer = 0
            while running:
                char = polishedtkn[strpointer]
                if binaryops.iscodepoint(char):
                    print(f"{polishedtkn} -> {char} -> {char.encode().hex()} -> {binaryops.toint(char)}")
                    #polishedtkn = polishedtkn[:strpointer] + tokens[binaryops.toint(char)] + polishedtkn[1+strpointer:]
                    polishedtkn = polishedtkn.replace(char, tokens[binaryops.toint(char)], 1)
                    strpointer += len(tokens[binaryops.toint(char)])
                else:
                    strpointer += 1
                running = strpointer < len(polishedtkn)
            
            #Append token to token list and replace instances in words
            index = len(tokens)
            tokens.append(polishedtkn)
            tknchar = binaryops.toutf(index)
            for elem in list(words.keys()):
                if tkn in elem:
                    words[elem.replace(tkn, tknchar)] = words.pop(elem)
                    #print(f"{elem} -> {elem.replace(tkn, tknchar)} with index {index}")

        #save list to json
        with open(self.json_source, "w") as file:
            json.dump(tokens, file)
        self.tokens = tokens


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
                #tokens[subword] += tkn[subword]
            tokens.update(tkn)
        return tokens
    
    def encode(self, msg: str) -> list[int]:
        """encodes given string to tokens"""
        encoding = []
        for word in msg.split(" "):
            encoding += self._encodeword(word) + [self.tokens.index(" ")]
        return encoding[:-1]
    
    def _encodeword(self, word: str):
        """path piece encoding of a word"""
        #populate graph
        vertices = list(range(len(word)+1))
        adjmap = [[0 for _ in range(len(vertices))]
                   for _ in range(len(vertices))]
        tokenmap = [[0 for _ in range(len(vertices))]
                   for _ in range(len(vertices))]
        tokenpath = [[] for _ in range(len(vertices))]
        for i in range(len(word)):
            for j in range(i+1, len(word)+1):
                if word[i:j] in self.tokens:
                    adjmap[i][j] = 1
                    tokenmap[i][j] = self.tokens.index(word[i:j])
        #check for missing characters and assign special token number
        
        sptSet = [False] * len(vertices)
        dist = [1e7] * len(vertices)
        dist[0] = 0
        for _ in range(len(vertices)):
            #get min distance vertex
            min = 1e7
            u = 0
            for i in range(len(dist)):
                if dist[i] < min and not sptSet[i]:
                    min = dist[i]
                    u = i
            
            sptSet[u] = True

            for v in range(len(vertices)):
                if adjmap[u][v] > 0 and not sptSet[v] and dist[v] > dist[u] + adjmap[u][v]:
                    # update distances
                    dist[v] = dist[u] + adjmap[u][v]
                    # update tokens
                    tokenpath[v] = tokenpath[u] + [tokenmap[u][v]]
            
            if sptSet[-1]:
                break
        return tokenpath[-1]
    
    def decode(self, tokenlist):
        res = ""
        for i in tokenlist:
            res += self.tokens[i]
        return res
                
        


tk = poc_tokenizer("poc_tk")
tk.load()

string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
string2 = ''.join(chr(i) for i in range(256))

print(tk.encode("Hello world!"))

print(tk.decode(tk.encode("Hello World!")))
print(tk.tokens[32])