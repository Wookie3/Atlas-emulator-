from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_jbz_debug():
    print("=" * 50)
    print("Atlas: Debugging JBZ Test")
    print("=" * 50)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    print("\nSetup:")
    mem.write(100, 100)  # For accumulator
    mem.write(103, 1)    # Decrement value
    mem.write(107, 5)    # Initial B3 value
    
    program = [
        # 0: Load B3 with 5
        join_instruction(0x089, 3, 0, 107),
        # 1: Load accumulator with 100
        join_instruction(0x0EE, 0, 0, 100),
        # 2: Decrement B3 by 1 (B3 = 5 - 1 = 4)
        join_instruction(0x083, 3, 0, 103),
        # 3: If B3 == 0, jump to 6 (should NOT jump since B3=4)
        join_instruction(0x08F, 3, 0, 6),
        # 4: Add 1000 to accumulator
        join_instruction(0x081, 0, 0, 108),
        # 5: Load accumulator with B0 value (just to print)
        join_instruction(0x0D2, 0, 0, 108),
        # 6: Print accumulator (should be 1100)
        join_instruction(0x200, 0, 0, 0),
        # 7: Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    mem.write(108, 1000)
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("\nProgram loaded, running...")
    print("Expected: 1100 (JBZ should NOT jump, add should execute)")
    cpu.run(0)
    
    print(f"\nFinal accumulator: {cpu.accumulator}")
    print(f"Final B3: {cpu.b_store[3]}")
    print(f"Final PC: {cpu.pc}")

if __name__ == "__main__":
    test_jbz_debug()
