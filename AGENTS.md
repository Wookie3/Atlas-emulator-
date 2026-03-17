# Atlas Emulator - Agent Guidelines

This file provides guidelines for agentic coding assistants working on this repository.

## Build, Lint, and Test Commands

### Running Tests

**Run all core tests:**
```bash
python test_working.py
python test_all_operations.py
python test_division.py
python test_paging.py
```

**Run a single test:**
```bash
python test_working.py          # Comprehensive validation
python test_all_operations.py   # All four arithmetic operations
python test_division.py        # Division instructions
python test_paging.py          # Memory paging system
python main.py                 # Simple multiplication demo
```

**Debug execution trace:**
```bash
python test_debug.py            # Step-by-step instruction trace
```

**No build step required** - Pure Python project with no external dependencies.

### Linting/Type Checking

This project has no formal linting or type checking configured. When implementing:
- Use `python -m py_compile <file>` to check syntax
- Consider adding flake8/mypy for future code quality enforcement

## Code Style Guidelines

### Imports

- Use relative imports for internal modules: `from .utils import mask_48`
- Absolute imports for test files: `from atlas_emu.memory import Memory`
- Group imports: standard library → third-party → local (if adding dependencies)

```python
# Good - internal module
from .utils import mask_48, mask_24

# Good - test file
from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction
```

### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: No strict limit, but aim for readability
- **Blank lines**: 1 between methods, 2 between class definitions
- **Spaces around operators**: `x + y`, `x == y`, not `x+y` or `x==y`

### Naming Conventions

```python
# Classes: PascalCase
class CPU:
class Memory:
class InstructionSet:

# Functions/Methods: snake_case
def fetch(self):
def decode(self, word):
def _page_fault(self, virtual_page):

# Variables: snake_case
self.accumulator = 0
self.b_store = [0] * 128
virtual_page = addr >> PAGE_BITS

# Constants: UPPER_CASE at module level
PAGE_SIZE = 512
MASK_48 = 0xFFFFFFFFFFFF
ADDRESS_BITS = 24

# Private methods: single underscore prefix
def _get_page_indices(self, virtual_addr):
def _page_fault(self, virtual_page):
```

### Type System

- No type hints currently used in codebase
- Document complex parameters in docstrings
- Maintain consistency with existing style (no migration to type hints unless necessary)

```python
def execute(self, f, ba, bm, s_prime):
    """
    f: 10-bit opcode
    ba: B-index 1
    bm: B-index 2
    s_prime: effective address (s + B[bm])
    """
```

### Error Handling

**Core emulator modules:**
- Use `print()` for runtime errors (division by zero, unknown opcodes)
- Set `self.running = False` on fatal errors
- Don't use exceptions for control flow

```python
# Good
if val != 0:
    self.cpu.b_store[ba] = mask_24(self.cpu.b_store[ba] // val)
else:
    print("Division by zero!")
    self.cpu.running = False
```

**Test files:**
- Use `assert` statements for validation
- Include descriptive failure messages

```python
assert cpu.accumulator == 56, "Multiplication test failed!"
```

### Classes and Structure

**Class initialization:**
- Use `__init__` for setup
- Initialize all instance variables in `__init__`
- Store references to other components (Memory, CPU, etc.)

```python
class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.instruction_set = InstructionSet(self)
        self.accumulator = 0
        self.b_store = [0] * 128
        self.running = False
```

**Properties:**
- Use `@property` for computed attributes
- Use `@name.setter` when validation needed

```python
@property
def pc(self):
    """Program Counter is B127."""
    return self.b_store[127]

@pc.setter
def pc(self, val):
    self.b_store[127] = mask_24(val)
```

### Documentation

- Docstrings for classes and public methods
- Inline comments for complex bitwise operations
- Reference historical Atlas terminology (B-line, accumulator, etc.)

```python
class Memory:
    """
    Simulates Atlas 'One-Level Store' (Virtual Memory).
    """

def _get_page_indices(self, virtual_addr):
    virtual_page = virtual_addr >> PAGE_BITS
    offset = virtual_addr & PAGE_MASK
    return virtual_page, offset
```

### Constants and Magic Numbers

- Define constants at module level
- Avoid hardcoded magic numbers in logic

```python
# Good
PAGE_SIZE = 512
PAGE_BITS = 9
MASK_24 = 0xFFFFFF

virtual_page = virtual_addr >> PAGE_BITS
offset = virtual_addr & PAGE_MASK

# Avoid
virtual_page = virtual_addr >> 9
offset = virtual_addr & 0x1FF
```

### Bitwise Operations

- Use bit shifting and masking for instruction manipulation
- Define helper functions in `utils.py` for common operations

```python
# Instruction construction
def join_instruction(f, ba, bm, s):
    word = (f & 0x3FF) << 38
    word |= (ba & 0x7F) << 31
    word |= (bm & 0x7F) << 24
    word |= (s & MASK_24)
    return word

# Bit masking
def mask_48(val):
    return val & MASK_48
```

### Instruction Set Extension

When adding new instructions to `atlas_emu/instructions.py`:

1. Add opcode to appropriate section (Accumulator, B-Register, Control)
2. Include both hex and octal values in comments
3. Include historical name if known
4. Follow existing pattern for implementation

```python
elif f == 0x0D5: # 325 octal (MLA - Multiply Accumulator)
    val = self.memory.read(s_prime)
    self.cpu.accumulator = mask_48(self.cpu.accumulator * val)
```

### Test Structure

Test files should:
- Create fresh Memory/CPU instances for each test case
- Use descriptive print statements
- Include expected values in output
- Use assertions for validation

```python
def test_example():
    print("1. Test Description...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 10)
    
    program = [...]
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 20)")
    assert cpu.accumulator == 20, "Test failed!"
    print("   [PASS]")
```

## Historical Accuracy

This emulator aims to be historically accurate to the Atlas computer (1962). When adding features:
- Research actual Atlas instruction set if possible
- Preserve Atlas terminology (B-line, B-store, accumulator, extracode)
- Maintain the one-level store concept in memory management
- Reference Manchester University Atlas documentation when in doubt

## File Organization

```
atlas_emu/
├── __init__.py
├── cpu.py           # CPU core, fetch-decode-execute cycle
├── memory.py        # Virtual memory with paging
├── instructions.py  # Instruction set implementation
└── utils.py        # Bitwise utilities, masking

*.py                # Test files and demos
```

Keep core emulator in `atlas_emu/`. Tests can be in root directory.
