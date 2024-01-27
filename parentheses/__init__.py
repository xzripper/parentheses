"""Light parentheses parser in Python."""

from re import findall


_p_v: str = '1.0.0-pypi-reupload'

ParenthesesSymbol = str

ParseFlag = int

PARENTHESES_ALL: ParseFlag = 1
PARENTHESES_OPEN: ParseFlag = 2
PARENTHESES_CLOSE: ParseFlag = 3

PARENTHESES_ROUND_OPEN: ParenthesesSymbol = '('
PARENTHESES_ROUND_CLOSE: ParenthesesSymbol = ')'

PARENTHESES_SQUARE_OPEN: ParenthesesSymbol = '['
PARENTHESES_SQUARE_CLOSE: ParenthesesSymbol = ']'

PARENTHESES_CURLY_OPEN: ParenthesesSymbol = '{'
PARENTHESES_CURLY_CLOSE: ParenthesesSymbol = '}'

PARENTHESES_DOUBLE_QUOTE: ParenthesesSymbol = '"'

PARENTHESES_SINGLE_QUOTE: ParenthesesSymbol = '\''

PARENTHESES_OPEN_SYMBOLS: list[ParenthesesSymbol] = [
    PARENTHESES_ROUND_OPEN,
    PARENTHESES_SQUARE_OPEN,
    PARENTHESES_CURLY_OPEN
]

PARENTHESES_CLOSE_SYMBOLS: list[ParenthesesSymbol] = [
    PARENTHESES_ROUND_CLOSE,
    PARENTHESES_SQUARE_CLOSE,
    PARENTHESES_CURLY_CLOSE
]

PARENTHESES_SYMBOLS = PARENTHESES_OPEN_SYMBOLS + PARENTHESES_CLOSE_SYMBOLS

PARENTHESES_REGEX = r'\(.*?\)|\[.*?\]|\{.*?\}'

class PPString:
    """Parsed parentheses string."""

    def __init__(self, string: str) -> None:
        # Not supposed to be called by user.

        self.string = string

    def valid_proc(self) -> bool:
        """Get is parentheses in string valid. (Slower but gives more accurate result)."""
        open_braces = []

        for char in self.string:
            if char in PARENTHESES_OPEN_SYMBOLS:
                open_braces.append(True)

            if char in PARENTHESES_CLOSE_SYMBOLS:
                if open_braces.count(True) <= 0:
                    return False

                open_braces[open_braces.index(True)] = False

        return not any(open_braces)

    def valid(self) -> bool:
        """Get is parentheses in string valid. (Faster but gives less accurate result)."""
        return self.count() % 2 == 0 and self.count(PARENTHESES_OPEN) == self.count(PARENTHESES_CLOSE)

    def valid_quotes(self, _escaping: bool=False) -> bool:
        """Get is quoted parentheses valid."""
        quote_open = False

        escaping = False

        for char in self.string:
            for q_sym in [PARENTHESES_DOUBLE_QUOTE, PARENTHESES_SINGLE_QUOTE]:
                if char == q_sym:
                    if _escaping:
                        if not escaping:
                            quote_open = not quote_open

                        else:
                            escaping = False

                    else:
                        quote_open = not quote_open

                if _escaping:
                    escaping = char == '\\'

        return not quote_open

    def count(self, flag: ParseFlag=PARENTHESES_ALL) -> int:
        """Count braces in string."""
        symbols = PARENTHESES_SYMBOLS \
            if flag == PARENTHESES_ALL \
                else (PARENTHESES_OPEN_SYMBOLS \
                    if flag == PARENTHESES_OPEN \
                        else (PARENTHESES_CLOSE_SYMBOLS \
                            if flag == PARENTHESES_CLOSE \
                                else []))

        return sum([self.string.count(p_sym) for p_sym in symbols])

    def autoclose(self) -> str:
        """Autoclose brackets."""
        if self.valid_proc():
            return self.string

        close_with = []

        for char in self.string:
            if char in PARENTHESES_OPEN_SYMBOLS:
                close_with.append(PARENTHESES_CLOSE_SYMBOLS[PARENTHESES_SYMBOLS.index(char)])

            if char in PARENTHESES_CLOSE_SYMBOLS:
                close_with.pop(-1)

        return self.string + ''.join(reversed(close_with))

    def find(self, remove_braces: bool=False) -> list:
        """Get content in braces."""
        if not self.valid_proc():
            return []

        def _close(_str):
            _parsed = parse(_str)

            if remove_braces:
                return _parsed.remove_braces()

            if not remove_braces:
                return _parsed.autoclose()

        return [_close(_str) for _str in findall(PARENTHESES_REGEX, self.string)]

    def remove_braces(self) -> str:
        """Remove braces in string."""
        string = self.string

        for parentheses_symbol in PARENTHESES_SYMBOLS:
            string = string.replace(parentheses_symbol, '')

        return string

    def remove(self, keep_braces: bool=False) -> str:
        """Remove everything in parentheses."""
        for content in self.find(keep_braces):
            self.string = self.string.replace(content, '')

        return self.string

    def as_str(self) -> str:
        """Get string."""
        return self.string

def _gen_re(o_s: str, c_s: str) -> str:
    return fr'|\{o_s}.*?\{c_s}'

def parse(string: str) -> PPString:
    """Parse string."""
    return PPString(string)

def new_parentheses_symbols(open_symbol: ParenthesesSymbol, close_symbol: ParenthesesSymbol) -> None:
    """Add new parentheses symbols."""
    global PARENTHESES_REGEX

    PARENTHESES_OPEN_SYMBOLS.append(open_symbol)
    PARENTHESES_CLOSE_SYMBOLS.append(close_symbol)

    PARENTHESES_REGEX += _gen_re(open_symbol, close_symbol)

def remove_parentheses_symbols(open_symbol: ParenthesesSymbol, close_symbol: ParenthesesSymbol) -> None:
    """Remove parentheses symbols."""
    global PARENTHESES_REGEX

    try:
        PARENTHESES_OPEN_SYMBOLS.pop(PARENTHESES_OPEN_SYMBOLS.index(open_symbol))
        PARENTHESES_CLOSE_SYMBOLS.pop(PARENTHESES_CLOSE_SYMBOLS.index(close_symbol))

        PARENTHESES_REGEX = PARENTHESES_REGEX.replace(_gen_re(open_symbol, close_symbol), '')
    except (ValueError, IndexError):
        pass
