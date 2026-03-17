from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_basic():
    print("=" * 50)
    print("Atlas Computer Emulator: Basic Operations Test")
    print("=" * 50)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    print("\n1. Setting up test data...")
    mem.write(100, 5)
    mem.write(101, 10)
    mem.write(102, 3)
    print(f"   - Addr 100: {mem.read(100)}")
    print(f"   - Addr 101: {mem.read(101)}")
    print(f"   - Addr 102: {mem.read(102)}")
    
    print("\n2. Test: Addition via accumulator...")
    
    program = [
        # Load accumulator with 5
        join_instruction(0x0EE, 0, 0, 100),
        # Add 10 to accumulator
        join_instruction(0x0D2, 0, 0, 101),
        # Add 3 to accumulator
        join_instruction(0x0D2, 0, 0, 102),
        # Print result (should be 18)
        join_instruction(0x200, 0, 0, 0),
        # Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Running: 5 + 10 + 3")
    print("   - Output:")
    cpu.run(0)
    
    print(f"\n   - Final accumulator: {cpu.accumulator} (Expected: 18)")
    
    print("\n3. Test: B-register operations...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 7)
    mem.write(101, 5)
    mem.write(102, 3)
    
    program = [
        # Load B1 with 7
        join_instruction(0x089, 1, 0, 100),
        # Add 5 to B1 (from memory)
        join_instruction(0x081, 1, 0, 101),
        # Subtract 3 from B1 (from memory)
        join_instruction(0x083, 1, 0, 102),
        # Store B1 to memory
        join_instruction(0x08D, 1, 0, 150),
        # Load accumulator from B1 value in memory
        join_instruction(0x0EE, 0, 0, 150),
        # Print result (should be 9)
        join_instruction(0x200, 0, 0, 0),
        # Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Running: B1 = 7 + 5 - 3")
    print("   - Output:")
    cpu.run(0)
    
    print(f"\n   - Final B1: {cpu.b_store[1]} (Expected: 9)")
    print(f"   - Memory addr 150: {mem.read(150)} (Expected: 9)")
    
    print("\n4. Test: Conditional jump (JBZ - Jump if B == 0)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 0)  # Zero value
    
    program = [
        # Load B2 with 0
        join_instruction(0x089, 2, 0, 100),
        # Load accumulator with 100
        join_instruction(0x0EE, 0, 0, 101),
        # Jump if B2 == 0 to skip next instruction
        join_instruction(0x08F, 2, 0, 6),  # Jump to print
        # This instruction should be SKIPPED
        join_instruction(0x081, 0, 0, 1000),
        # Print accumulator (should be 100, not 1100)
        join_instruction(0x200, 0, 0, 0),
        # Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    mem.write(101, 100)
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Running: Load 100, test JBZ with B2=0")
    print("   - Output:")
    cpu.run(0)
    
    print(f"\n   - Final accumulator: {cpu.accumulator} (Expected: 100)")
    
    print("\n5. Test: Conditional jump (JBN - Jump if B != 0)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 1)  # Non-zero value
    
    program = [
        # Load B3 with 1
        join_instruction(0x089, 3, 0, 100),
        # Load accumulator with 100
        join_instruction(0x0EE, 0, 0, 101),
        # Jump if B3 != 0 to skip next instruction
        join_instruction(0x091, 3, 0, 6),  # Jump to print
        # This instruction should be SKIPPED
        join_instruction(0x081, 0, 0, 1000),
        # Print accumulator (should be 100, not 1100)
        join_instruction(0x200, 0, 0, 0),
        # Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    mem.write(101, 100)
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Running: Load 100, test JBN with B3=1")
    print("   - Output:")
    cpu.run(0)
    
    print(f"\n   - Final accumulator: {cpu.accumulator} (Expected: 100)")
    
    print("\n6. Test: Simple multiplication loop (5 * 3)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 3)   # Multiplicand
    mem.write(101, 5)   # Loop counter
    mem.write(102, 0)   # Initial accumulator
    mem.write(103, 1)   # Decrement value
    
    program = [
        # Load B1 with loop counter (5)
        join_instruction(0x089, 1, 0, 101),
        # Load accumulator with 0
        join_instruction(0x0EE, 0, 0, 102),
        # Start loop: Add multiplicand (3) to accumulator
        join_instruction(0x0D2, 0, 0, 100),
        # Decrement B1 by 1
        join_instruction(0x083, 1, 0, 103),
        # Jump if B1 != 0 back to add instruction
        join_instruction(0x091, 1, 0, 2),
        # Print result (should be 15)
        join_instruction(0x200, 0, 0, 0),
        # Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Running: 5 * 3 via loop")
    print("   - Output:")
    cpu.run(0)
    
    print(f"\n   - Final accumulator: {cpu.accumulator} (Expected: 15)")
    print(f"   - Final B1: {cpu.b_store[1]} (Expected: 0)")
    
    print("\n7. Test: Memory paging...")
    mem = Memory(core_blocks=2)
    cpu = CPU(mem)
    
    print(f"   - Writing to different pages...")
    mem.write(0, 111)      # Page 0
    mem.write(512, 222)    # Page 1
    mem.write(1024, 333)   # Page 2 (should trigger swap)
    mem.write(1536, 444)   # Page 3 (should trigger swap)
    
    print(f"   - Reading back...")
    v0 = mem.read(0)
    v512 = mem.read(512)
    v1024 = mem.read(1024)
    v1536 = mem.read(1536)
    
    print(f"     Page 0 (addr 0): {v0} (Expected: 111)")
    print(f"     Page 1 (addr 512): {v512} (Expected: 222)")
    print(f"     Page 2 (addr 1024): {v1024} (Expected: 333)")
    print(f"     Page 3 (addr 1536): {v1536} (Expected: 444)")
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_basic()
