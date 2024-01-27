# Parentheses. V1.0.0
Light parentheses parser in Python. ```pip install parentheses```

## Types (Aliases):
```python
ParenthesesSymbol = str
ParseFlag = int
```

## Constants:
```python
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
```

## <code>PPString</code> class:
### <code>valid_proc() -> bool</code>
Get is parentheses in string valid. (Slower but gives more accurate result).<br><br>
Examples:<br>
`parse('(x)').valid_proc()` => `True`<br>
`parse('(x').valid_proc()` => `False`

### <code>valid() -> bool</code>
Get is parentheses in string valid. (Faster but gives less accurate result).<br><br>
Examples:<br>
`parse('(x)').valid()` => `True`<br>
`parse('(x').valid()` => `False`

### <code>valid_quotes(_escaping: bool=False) -> bool</code>
Get is quoted parentheses valid.<br><br>
Examples:<br>
`parse('"x"').valid_quotes()` => `True`<br>
`parse('"x\""').valid_quotes(True)` => `True`<br>
`parse('"x').valid_quotes()` => `False`<br>
`parse('"x\""').valid_quotes()` => `False`

### <code>count(flag: ParseFlag=PARENTHESES_ALL) -> int</code>
Count braces in string.<br><br>
Examples:<br>
`parse('(x)').count()` => `2`<br>
`parse('(x)').count(PARENTHESES_OPEN)` => `1`<br>
`parse('(x)').count(PARENTHESES_CLOSE)` => `1`

### <code>autoclose() -> str</code>
Autoclose brackets.<br><br>
Examples:<br>
`parse('{[(x').autoclose()` => `{[(x)]}`

### <code>find(remove_braces: bool=False) -> list</code>
Get content in braces.<br><br>
Examples:<br>
`parse('(x) [y] {z}').find()` => `['(x)', '[y]', '{z}']`<br>
`parse('(x) [y] {z}').find(True)` => `['x', 'y', 'z']`

### <code>remove_braces() -> str</code>
Remove braces in string.<br><br>
Examples:<br>
`parse('(x) [y] {z}').remove_braces()` => `'x y z'`

### <code>remove(keep_braces: bool=False) -> str</code>
Remove everything in parentheses.<br><br>
Examples:<br>
`parse('(x) [y] {z}').remove()` => `'   '`<br>
`parse('(x) [y] {z}').remove(True)` => `'() [] {}'`

### <code>as_str() -> str</code>
Get string.<br><br>
Examples:<br>
`parse('x').as_str()` => `'x'`

## Global functions.
### <code>parse(string: str) -> PPString</code>
Parse string.<br><br>
Examples:<br>
`parse('(x)')` => `PPString('x')`

### <code>new_parentheses_symbols(open_symbol: ParenthesesSymbol, close_symbol: ParenthesesSymbol) -> None</code>
Add new parentheses symbols.<br><br>
Examples:<br>
`new_parentheses_symbols('<', '>')` => `None`

### <code>remove_parentheses_symbols(open_symbol: ParenthesesSymbol, close_symbol: ParenthesesSymbol) -> None</code>
Remove parentheses symbols.<br><br>
Examples:<br>
`remove_parentheses_symbols('<', '>')` => `None`
