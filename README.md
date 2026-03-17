# Atlas Computer Emulator

A Python-based emulator of the Atlas computer, one of the world's first computers with virtual memory. Developed at the University of Manchester in 1962, the Atlas was a pioneering mainframe that introduced innovations like paging, extracodes, and one-level store architecture.

## Features

- **48-bit accumulator** for high-precision calculations
- **128 B-registers** (24-bit each) for address modification and control
- **Virtual memory system** with paging (512 words per page)
- **Full arithmetic operations**: Add, Subtract, Multiply, Divide for both accumulator and B-registers
- **Conditional branching**: JBZ (Jump if B=0) and JBN (Jump if B!=0)
- **Memory management**: Automatic page swapping between core and drum storage
- **Historically accurate instruction set**: Based on Atlas machine instructions
- **1960s-era computing**: Authentic fixed-point arithmetic approach

## Setup

### Requirements
- Python 3.6 or higher
- No external dependencies required

### Installation

1. Clone or download the repository
2. Navigate to the Atlas directory
3. Run test programs:

```bash
# Test basic operations
python test_working.py

# Test all four arithmetic operations
python test_all_operations.py

# Test division specifically
python test_division.py

# Test memory paging
python test_paging.py

# Run the multiplication demo
python main.py
```

## Instructions

### Instruction Format

All Atlas instructions are 48 bits, organized as:

```
┌────┬─────┬─────┬────┐
│ F  │  Ba │  Bm │ S  │
│10b │ 7b  │ 7b  │24b │
└────┴─────┴─────┴────┘
```

- **F** (10 bits): Function code (opcode)
- **Ba** (7 bits): B-register index 1
- **Bm** (7 bits): B-register index 2 (for address modification)
- **S** (24 bits): Signed address field

Effective address is calculated as: `S + B[Bm]`

### Accumulator Instructions

| Opcode | Octal | Name | Description |
|--------|-------|------|-------------|
| 0x0EE | 356 | LDA | Load Accumulator |
| 0x0F2 | 362 | STA | Store Accumulator |
| 0x0D2 | 322 | ADA | Add to Accumulator |
| 0x0D3 | 323 | SBA | Subtract from Accumulator |
| 0x0D5 | 325 | MLA | Multiply Accumulator |
| 0x0D4 | 324 | DIV | Divide Accumulator |

### B-Register Instructions

| Opcode | Octal | Name | Description |
|--------|-------|------|-------------|
| 0x089 | 211 | LDB | Load B-line |
| 0x08D | 215 | STB | Store B-line |
| 0x081 | 201 | ADB | Add to B-line |
| 0x083 | 203 | SBB | Subtract from B-line |
| 0x082 | 202 | MLB | Multiply B-line |
| 0x084 | 204 | DVB | Divide B-line |

### Control Instructions

| Opcode | Octal | Name | Description |
|--------|-------|------|-------------|
| 0x08F | 217 | JBZ | Jump if B[Ba] == 0 |
| 0x091 | 221 | JBN | Jump if B[Ba] != 0 |
| 0x000 | 000 | HALT | Stop execution |

### Extracodes

| Opcode | Octal | Name | Description |
|--------|-------|------|-------------|
| 0x200 | 1000 | PRINT | Print Accumulator value |

## Memory Architecture

### One-Level Store (Virtual Memory)

The Atlas pioneered virtual memory with its "one-level store" concept:

- **Address space**: 24-bit (16 million words)
- **Page size**: 512 words
- **Core store**: Configurable (default: 32 blocks = 16,384 words)
- **Drum store**: Backing storage (default: 1024 pages)

### Address Calculation

Virtual addresses are split into:
- **Page number**: High bits (15 bits)
- **Offset**: Low 9 bits

Page fault handling is automatic - when a page isn't in core, it's loaded from drum, potentially swapping out another page.

## Programming Examples

### Simple Addition

```python
from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

mem = Memory()
cpu = CPU(mem)

# Set up data
mem.write(100, 25)
mem.write(101, 17)

# Program: Add 25 + 17
program = [
    join_instruction(0x0EE, 0, 0, 100),  # Load 25
    join_instruction(0x0D2, 0, 0, 101),  # Add 17
    join_instruction(0x0F2, 0, 0, 102),  # Store result
    join_instruction(0x200, 0, 0, 0),      # Print
    join_instruction(0x000, 0, 0, 0)       # Halt
]

for i, inst in enumerate(program):
    mem.write(i, inst)

cpu.run(0)  # Output: 42
```

### Multiplication Loop (5 × 3)

```python
mem.write(100, 3)    # Multiplicand
mem.write(101, 5)    # Counter
mem.write(102, 0)    # Accumulator init
mem.write(103, 1)    # Decrement value

program = [
    join_instruction(0x089, 1, 0, 101),  # B1 = 5
    join_instruction(0x0EE, 0, 0, 102),  # ACC = 0
    join_instruction(0x0D2, 0, 0, 100),  # ACC += 3 (loop start)
    join_instruction(0x083, 1, 0, 103),  # B1 -= 1
    join_instruction(0x091, 1, 0, 2),    # If B1 != 0, jump to loop
    join_instruction(0x200, 0, 0, 0),     # Print result
    join_instruction(0x000, 0, 0, 0)      # Halt
]
```

### Temperature Conversion

```python
# Convert 25°C to Fahrenheit: F = (C × 9/5) + 32
mem.write(100, 25)   # Celsius
mem.write(101, 9)    # Multiply by 9
mem.write(102, 5)    # Divide by 5
mem.write(103, 32)   # Add 32

program = [
    join_instruction(0x0EE, 0, 0, 100),  # Load 25
    join_instruction(0x0D5, 0, 0, 101),  # × 9 = 225
    join_instruction(0x0D4, 0, 0, 102),  # ÷ 5 = 45
    join_instruction(0x0D2, 0, 0, 103),  # + 32 = 77
    join_instruction(0x200, 0, 0, 0),     # Print
    join_instruction(0x000, 0, 0, 0)      # Halt
]
```

## Historical Context

The Atlas computer (1962) was revolutionary for several reasons:

1. **First with Virtual Memory**: Introduced paging and the concept of one-level store
2. **Extracodes**: Software-defined instructions extending the hardware instruction set
3. **Multiprogramming**: Could run multiple programs simultaneously
4. **Compiler Design**: Hosted the development of the Atlas Autocode, an early high-level language
5. **Scientific Computing**: Used for ballistic calculations, nuclear research, and weather prediction

Key applications included:
- Ballistic trajectory analysis (military)
- Nuclear weapons research (Aldermaston, UK)
- Weather prediction and atmospheric modeling
- Business data processing (payroll, inventory)
- Scientific research and engineering calculations

## Architecture Details

### CPU Registers
- **Accumulator**: 48-bit (main arithmetic register)
- **B-store**: 128 × 24-bit registers (address modification)
- **B0**: Always zero (Atlas convention)
- **B127**: Program Counter (PC)

### Memory Units
- **Core Store**: Fast RAM (magnetic core memory)
- **Drum Store**: Backing storage (magnetic drum)
- **PAR** (Page Address Registers): Maps virtual pages to core blocks

### Execution Cycle
1. **Fetch**: Read 48-bit instruction from memory at PC
2. **Decode**: Split into F, Ba, Bm, S components
3. **Modify**: Calculate effective address (S + B[Bm])
4. **Execute**: Perform operation
5. **Update**: Increment PC (or jump)

## File Structure

```
atlas_emu/
├── __init__.py
├── cpu.py          # CPU implementation
├── memory.py       # Virtual memory with paging
├── instructions.py # Instruction set execution
└── utils.py        # Bit manipulation utilities

tests/
├── main.py              # Simple multiplication demo
├── test_paging.py       # Memory paging test
├── test_basic.py        # Basic operations tests
├── test_working.py      # Comprehensive test suite
├── test_division.py     # Division instruction tests
├── test_all_operations.py # All four arithmetic operations
└── test_payroll.py      # Historical business application
```

## Changelog

### Version 1.2 - Arithmetic Operations Extended
**Added:**
- Multiply instruction (MLA/MLB)
- Divide instruction (DIV/DVB)
- Comprehensive arithmetic test suite
- Practical examples: temperature conversion, area calculations

### Version 1.1 - Bug Fixes
**Fixed:**
- ADB and SBB instructions now read from memory instead of using address values
- Corrected loop jump targets in multiplication test
- All arithmetic operations now work correctly with memory operands

### Version 1.0 - Initial Release
**Features:**
- Basic CPU emulation with 48-bit accumulator
- 128 B-registers (24-bit)
- Virtual memory with paging (one-level store)
- Add and subtract operations
- Conditional jumps (JBZ, JBN)
- Load/Store operations
- PRINT extracode
- HALT instruction
- Test programs for validation

## License

This is an educational emulator based on the historical Atlas computer architecture.

## References

- "The Atlas Computer" - Kilburn, Grimsdale, and Sumner (1962)
- "One-Level Storage System" - The innovation that made virtual memory possible
- Manchester University Computer Archive

## Contributing

This emulator is designed for educational purposes. Suggestions for additional historical features or instruction set expansions are welcome.
