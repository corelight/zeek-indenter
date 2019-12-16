# Zeek Indenter

Zeek indenter is a python package to indent Zeek scripts per the Whitesmiths coding style.

## Software Requirement

* Python 3.6
* PyPy3 (recommended)
* Lark parser (>= v0.7.7)
* Zeek (required for verification)

# Installation

```
python3.6 setup.py install
```

or if using PyPy3

```
pypy3 setup.py install
```

## Execution
```
python3.6 example/indent.py -f filename -o out_dir -v -t 20
```
or
```
pypy3 example/indent.py -f filename -o out_dir -v -t 20
```
There are seven operational switches:
* ```-f``` specifies a single input file
* ```-d``` specifies an input directory of Zeek files for batch processing
* ```-v``` allows verbose output for debugging
* ```-o``` specifies an output directory to store results
* ```-t``` sets the per execution timeout (default is 10s)
* ```-e``` sets the parsing algorithm to Earley (default is LALR)
* ```-p``` returns the root of the parse tree after only parsing (and not indenting) the single input file specified by ```-f```

Each execution can result in one of the following five outcomes:
1) The execution failed due to a parse error, which indicates an issue with the Zeek grammar as implemented in Lark (our parser generator).
2) The execution of the file took too long and resulted in a timeout error. Currently, the timeout is set at 10s. Note that the use of PyPy and LALR together may significantly reduce the number of such timeout errors.
3) The indenting transformation resulted in an exception.
4) The verification of the indented code failed (via ```zeek -a```).
5) The indented code is verified.

At the end of execution, the tool creates two directories --- *verified* and *error*, with the former containing all indented and verified code,
while the latter includes the files that resulted in the four error scenarios. Note that for the first three error cases no indented code is
produced; only an empty file with the corresponding filename is generated.

## Formatting Convention

### 1) Declaration
Declarations such as ```@load``` and ```module``` are formatted in a single line.

### 2) Statements
Each statement is formatted in a separate line, and two statements are separated by a blank line. Further, some statements, such as ```switch``` and ```for```, can span multiple lines.

### 3) Expressions
Unlike a statement, an expression never spans multiple lines, i.e., it is always formatted in a single line and wraps around if the expression overflows column width. All subsequent lines (after the wrap-around) are indented by the default indentation. Consequently, the current version of the indenter does not support comments within expression lists.

### 4) Type Declarations
Type declarations follow formatting similar to expressions and span a single line only, except constructs such as ```enum```, ```record```, ```set``` and ```table```, which span multiple lines for ease of comprehension.

### 5) Comments
Comments between statements are grouped and formatted in a separate line that can be wrapped around if required. Comments within a statement, i.e., if they are part of an expression, are removed for the sake of simplifying the parsing. All newlines within a comment are removed.

## Known Issues

- Expression lists are not formatted and currently span a single line. Consequently, comments in expression lists are not allowed.
- Comments can exist at many different locations in the source code. While the majority of these locations, including comments before statements, declarations, enum values, etc., are supported, the current grammar does not support all possible comment locations.
- The operators for logical OR ```|``` and absolute value ```| |``` cause a grammar error during a reduction in LALR parsing. A workaround would be to wrap the absolute value ```|a + 4| > 10``` as ```(|(a + 4)|) > 10```, which should parse fine, or use Earley.
- All possible operator precedence combinations have not yet been verified.