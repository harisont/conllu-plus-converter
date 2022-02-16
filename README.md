# conllu-plus-converter
Convert CoNLL-U Plus files to ordinary CoNLL-u and vice versa.

## Dependencies
- `conllu`
- `argparse`

## Installation
Assuming you have Python installed, installation goes as for most other Python programs:

1. install the missing dependencies (e.g. `pip install conllu`)
2. clone this reporitory and move inside, e.g.:
   ```
   git clone https://github.com/harisont/conllu-plus-converter && cd conllu-plus-converter
   ```
3. mark the Python file as executable (`chmod +x conllu-plus-converter.py`)
4. add, as the file's first line, the path to your Python interpreter (e.g. `#!/usr/bin/env python`)
5. copy or move the file to a folder in your `PATH`, e.g. `usr/bin`
6. optionally, you can rename it to something short and extensionless, like `conllup`. This will allow you to invoke the program by simply typing `conllup [args]`

## Usage

### CoNLL-U Plus to plain CoNLL-U
```
connlup from_plus PATH
```

This can be useful also to normalize "simplified" CoNLL-U files (i.e. files where some columns have been omitted). To do that, add your simplified CoNNL-U file a comment line such as:

```
# global.columns = ID FORM LEMMA UPOS HEAD DEPREL DEPS MISC
```

indicating what columns your file actually contains (in the example, all but XPOS and FEATS).

### Plain CoNLL-U to CoNLL-U Plus
```
conllup to_plus=FIELD1,FIELD2... PATH
```

You can use this also to "simplify" CoNLL-U files by passing `to_plus` a subset of the standard fields.