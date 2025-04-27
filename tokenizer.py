class tokenizer:
    """Abstract class for tokenizers"""
    json_source: str

    def encode(self, msg: str) -> list[int]:
        """Encodes given string to list of indexes of tokens"""
        pass

    def decode(self, tokens: list[int]) -> str:
        """decodes given list of token indexes"""
        pass