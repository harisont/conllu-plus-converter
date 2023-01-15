# conllu-plus-converter
Convert CoNLL-U Plus files to plain CoNLL-U and vice versa.

When CoNNL-U Plus files have a lot of project-specific extra annotations under [MISC](https://universaldependencies.org/misc.html), using [CoNLL-U Plus](https://universaldependencies.org/ext-format.html) can be much nicer. Unfortunately, many tools for working with CoNNL-U files don't support CoNNL-U Plus  (yet), so it can be useful to convert files between the two formats without loosing any information.

With this converter, for example, a CoNLL-U Plus file lacking XPOS and FEATS and having an extra field CORRECTION, such as this:

```
# global.columns = ID FORM LEMMA UPOS HEAD DEPREL DEPS MISC CORRECTION

# sent_id = 1
# text = dep thoughts
1	dep	deep	ADJ	2	amod	_	_   deep
2	thoughts	thought	NOUN	0	root	_	_   _
```

is converted to plain CoNNL-U by padding the missing columns with underscores and moving the information contained in the extra columns to MISC as `COLUMN_NAME=value` pairs:

```
# sent_id = 1
# text = dep thoughts
1       dep     deep    ADJ     _       _       2       amod    _       _|CORRECTION=deep
2       thoughts        thought NOUN    _       _       0       root    _       _|CORRECTION=_
```

In this way, it is always possible to convert the resulting file to its original CoNNL-U Plus form.

## Dependencies
- `conllu`
- `argparse`

## Installation
Assuming you have Python installed, installation goes as for most other Python programs:

1. install the missing dependencies (e.g. `pip install conllu`)
2. clone this reporitory and move inside it
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
# global.columns = ID FORM LEMMA UPOS XPOS HEAD DEPREL DEPS MISC
```

indicating what columns your file actually contains (in the example, all but XPOS and FEATS).

### Plain CoNLL-U to CoNLL-U Plus
```
conllup to_plus=FIELD1,FIELD2... PATH
```

You can use this also to "simplify" CoNLL-U files by passing `to_plus` a subset of the standard fields.
