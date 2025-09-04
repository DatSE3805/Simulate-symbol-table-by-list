# Simulate Symbol Table (Functional Python)

> Build a **list-based Symbol Table simulator** in pure functional style (no loops, no classes, no globals). Implement `simulate(commands: list[str])` to process a tiny command language (`INSERT`, `ASSIGN`, `BEGIN`/`END`, `LOOKUP`, `PRINT`, `RPRINT`) with scope rules and strict error handling. Provide **≥50 tests** in `TestSuite.py`.

## Learning Outcomes
- Rehearse **functional programming** fundamentals.
- Apply **higher-order functions** and **list processing**.
- Model **nested lexical scopes** and **symbol resolution** using lists.

## Problem Overview
You will simulate a compiler-like **symbol table** that tracks identifier names and their types across nested blocks (scopes). The simulator ingests a sequence of textual commands and prints results (or raises the specified errors) exactly as defined below.

### Allowed Types
- `number`
- `string`

### Identifier Lexeme
- Must **start with a lowercase letter**; remaining chars may be lowercase/uppercase letters, digits, or `_`.

## Command Language
Each command occupies **one line**, with **exact single spaces** between tokens (no extra spaces, no missing tokens). Any format violation must **immediately raise `InvalidInstruction`** with the faulty line.

| Command | Format | Meaning | Output | Errors |
|---|---|---|---|---|
| Insert | `INSERT <id> <type>` | Declare a new identifier in the **current scope** | `success` | `Redeclared` if `<id>` already exists **in current scope** |
| Assign | `ASSIGN <id> <value>` | Assign a value to `<id>` | `success` | `Undeclared` if either side references an unknown id; `TypeMismatch` if value type ≠ id type |
| Open/Close Block | `BEGIN` / `END` | Enter/leave a nested scope | *(no output)* | `UnclosedBlock:<level>` at EOF if blocks not closed; `UnknownBlock` if `END` without matching `BEGIN` |
| Lookup | `LOOKUP <id>` | Resolve `<id>` from **innermost** to outer scopes | prints the **level** (0 = global) | `Undeclared` if not found |
| Print (forward) | `PRINT` | Visible ids in **current scope view**, in **declaration order** | `name//level` pairs separated by spaces | *(—)* |
| Print (reverse) | `RPRINT` | Visible ids printed from **child to parent** order | `name//level` pairs separated by spaces | *(—)* |

### Values for `ASSIGN`
- **Number constant**: digits only, e.g., `123` (no signs, no decimal points).
- **String constant**: single-quoted; contains letters, digits, and spaces, e.g., `'hello 123'` (no other punctuation).
- **Identifier**: a previously declared id; its **declared type** is used for type checking.

### Scoping & Resolution
- Global scope is **level 0**; each `BEGIN` increases level by 1; `END` decreases it.
- **Shadowing allowed**: an inner `INSERT` may redeclare a name that exists in an outer scope.
- Lookup/assignment resolves identifiers **from the innermost scope outward**.
- `PRINT` and `RPRINT` show only the **visible** identifiers (inner declarations shadow outers). Output format is `name//level` joined by single spaces.

## Required Files & APIs
You’ll be given:
```
main.py
Symbol.py
SymbolTable.py   # You implement here
TestSuite.py     # You add ≥50 tests here
TestUtils.py
```
Do **not** rename files.

### Entry Point
Implement **at least**:
```python
def simulate(commands: list[str]) -> None:
    ...
```
This function processes a list of raw command strings and performs all printing/exception behavior.

### Import Policy (strict)
Only these are allowed inside `SymbolTable.py`:
```python
from StaticError import *
from Symbol import *
from functools import *
```
Any other imports are **forbidden**.

## Functional Programming Constraints
- **No additional modules** beyond those listed above.
- **Only functions** defined via `def`. **No classes**, **no global variables**.
- **No loops** (`for`, `while`, …). Use **higher-order functions** and **list comprehensions**.
- **Single assignment per variable** inside each function (treat locals as immutable).

Violations cause **automatic rejection** of the submission.

## I/O Contract — Examples (Informal)
- Inserting two distinct ids:
  ```text
  INSERT a1 number
  INSERT b2 string
  → success
  → success
  ```
- Redeclaration in the same scope:
  ```text
  INSERT x number
  INSERT x string
  → Redeclared: INSERT x string
  ```
- Shadowing across blocks and printing:
  ```text
  INSERT x number
  BEGIN
  INSERT x number
  INSERT z number
  PRINT
  END
  → success
  → success
  → success
  → y//0 x//1 z//1   # Example shape: visible ids as name//level
  ```

*(Your outputs must match the exact spec for lines, spaces, and error messages.)*

## Testing Guidance
- Cover **happy paths** and **all error branches**: `Undeclared`, `Redeclared`, `TypeMismatch`, `UnclosedBlock`, `UnknownBlock`, `InvalidInstruction`.
- Stress **shadowing** (`BEGIN/END`), deep nesting, and visibility in `PRINT`/`RPRINT`.
- Validate **strict formatting** (single spaces, exact tokens).
---
