
class UWUException(Exception):
    pass

class UWUError(Exception):
    pass

class UWUTokenizerError(Exception):
    def __init__(self, msg: str, tokenizer) -> None:
        composed_msg = f'at char {tokenizer._char} [{tokenizer._line}:{tokenizer._col}] '
        if tokenizer.source_name is not None:
            composed_msg = f'in {tokenizer.source_name} ' + composed_msg
        composed_msg += msg
        super().__init__(composed_msg)
        self.tokenizer = tokenizer
