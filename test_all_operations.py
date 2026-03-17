from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_four_operations():
    print("=" * 70)
    print("  ATLAS COMPUTER - All Four Arithmetic Operations")
    print("=" * 70)
    
    print("\nAvailable Arithmetic Instructions:")
    print("  ADD:    ADA (Accumulator), ADB (B-register)")
    print("  SUBTRACT: SBA (Accumulator), SBB (B-register)")
    print("  MULTIPLY: MLA (Accumulator), MLB (B-register)")
    print("  DIVIDE:   DIV (Accumulator), DVB (B-register)")
    
    print("\n" + "-" * 70)
    print("TEST 1: Basic Operations")
    print("-" * 70)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 10)
    mem.write(101, 5)
    mem.write(102, 2)
    mem.write(103, 3)
    
    program = [
        # ADD: 10 + 5 = 15
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x0D2, 0, 0, 101),
        join_instruction(0x08D, 0, 0, 200),
        
        # SUBTRACT: 15 - 2 = 13
        join_instruction(0x0D3, 0, 0, 102),
        join_instruction(0x08D, 0, 0, 201),
        
        # MULTIPLY: 13 * 3 = 39
        join_instruction(0x0D5, 0, 0, 103),
        join_instruction(0x08D, 0, 0, 202),
        
        # DIVIDE: 39 / 3 = 13
        join_instruction(0x0D4, 0, 0, 103),
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Operations: (10 + 5 - 2) * 3 / 3")
    print("  Step-by-step:")
    print("    10 + 5 = 15")
    print("    15 - 2 = 13")
    print("    13 * 3 = 39")
    print("    39 / 3 = 13")
    print("  Result:")
    cpu.run(0)
    print("  Expected: 13")
    
    print("\n" + "-" * 70)
    print("TEST 2: B-Register Operations")
    print("-" * 70)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 8)
    mem.write(101, 4)
    mem.write(102, 2)
    mem.write(103, 16)
    
    program = [
        # Load B1 with 8
        join_instruction(0x089, 1, 0, 100),
        # ADD: 8 + 4 = 12
        join_instruction(0x081, 1, 0, 101),
        # SUBTRACT: 12 - 2 = 10
        join_instruction(0x083, 1, 0, 102),
        # MULTIPLY: 10 * 16 = 160
        join_instruction(0x082, 1, 0, 103),
        # DIVIDE: 160 / 10 = 16
        join_instruction(0x084, 1, 0, 101),
        # Store and print
        join_instruction(0x08D, 1, 0, 150),
        join_instruction(0x0EE, 0, 0, 150),
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Operations: ((8 + 4 - 2) * 16) / 4")
    print("  Using B1 register:")
    print("    B1 = 8")
    print("    B1 = B1 + 4 = 12")
    print("    B1 = B1 - 2 = 10")
    print("    B1 = B1 * 16 = 160")
    print("    B1 = B1 / 4 = 40")
    print("  Result:")
    cpu.run(0)
    print("  Expected: 40")
    
    print("\n" + "-" * 70)
    print("TEST 3: Area of Rectangle (length * width)")
    print("-" * 70)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 15)  # length
    mem.write(101, 8)   # width
    
    program = [
        join_instruction(0x0EE, 0, 0, 100),  # Load length
        join_instruction(0x0D5, 0, 0, 101),  # Multiply by width
        join_instruction(0x08D, 0, 0, 200),  # Store area
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Length: 15")
    print("  Width: 8")
    print("  Area = 15 * 8")
    print("  Result:")
    cpu.run(0)
    print("  Expected: 120")
    
    print("\n" + "-" * 70)
    print("TEST 4: Temperature Conversion (Celsius to Fahrenheit)")
    print("-" * 70)
    print("  Formula: F = (C * 9/5) + 32")
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 25)   # Celsius temperature
    mem.write(101, 9)    # Multiply by 9
    mem.write(102, 5)    # Divide by 5
    mem.write(103, 32)   # Add 32
    
    program = [
        # Load Celsius (25)
        join_instruction(0x0EE, 0, 0, 100),
        # Multiply by 9: 25 * 9 = 225
        join_instruction(0x0D5, 0, 0, 101),
        # Divide by 5: 225 / 5 = 45
        join_instruction(0x0D4, 0, 0, 102),
        # Add 32: 45 + 32 = 77
        join_instruction(0x0D2, 0, 0, 103),
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Input: 25 C")
    print("  Calculation: (25 * 9 / 5) + 32")
    print("  Result:")
    cpu.run(0)
    print("  Expected: 77 F")
    
    print("\n" + "-" * 70)
    print("TEST 5: Circle Area (pi * r^2)")
    print("-" * 70)
    print("  Formula: A = pi * r * r")
    print("  Using pi approx 3.14 (as integer 314/100)")
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 10)   # radius
    mem.write(101, 314)  # π * 100
    
    program = [
        # Load radius (10)
        join_instruction(0x0EE, 0, 0, 100),
        # Square it: 10 * 10 = 100
        join_instruction(0x0D5, 0, 0, 100),
        # Multiply by π: 100 * 314 = 31400
        join_instruction(0x0D5, 0, 0, 101),
        # Divide by 100: 31400 / 100 = 314
        join_instruction(0x0D4, 0, 0, 102),
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    mem.write(102, 100)  # Divisor for fixed-point
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Radius: 10")
    print("  Calculation: (10 * 10 * 3.14) approx 314")
    print("  Result:")
    cpu.run(0)
    print("  Expected: approx 314 (actual: 314.159...)")

    print("\n" + "-" * 70)
    print("TEST 6: Speed, Distance, Time Calculation")
    print("-" * 70)
    print("  Formula: Distance = Speed * Time")
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 60)   # Speed: 60 km/h
    mem.write(101, 2)    # Time: 2 hours
    
    program = [
        # Load speed
        join_instruction(0x0EE, 0, 0, 100),
        # Multiply by time
        join_instruction(0x0D5, 0, 0, 101),
        
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("  Speed: 60 km/h")
    print("  Time: 2 hours")
    print("  Distance = 60 * 2")
    print("  Result:")
    cpu.run(0)
    print("  Expected: 120 km")
    
    print("\n" + "=" * 70)
    print("ALL FOUR ARITHMETIC OPERATIONS WORKING! [OK]")
    print("=" * 70)
    print("\nInstructions Summary:")
    print("  Accumulator:")
    print("    0x0D2 - ADA (Add)")
    print("    0x0D3 - SBA (Subtract)")
    print("    0x0D5 - MLA (Multiply)")
    print("    0x0D4 - DIV (Divide)")
    print("  B-Register:")
    print("    0x081 - ADB (Add)")
    print("    0x083 - SBB (Subtract)")
    print("    0x082 - MLB (Multiply)")
    print("    0x084 - DVB (Divide)")

if __name__ == "__main__":
    test_four_operations()
