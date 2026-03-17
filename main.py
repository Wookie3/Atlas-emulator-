from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def main():
    print("--- Atlas Computer Emulator: Multiplication Loop ---")
    
    mem = Memory()
    cpu = CPU(mem)
    
    # Data Setup
    # Addr 100: Current Increment (3)
    # Addr 101: Initial Loop Count (5)
    # Addr 102: Decrement value (1)
    mem.write(100, 3) 
    mem.write(101, 5)
    mem.write(102, 1)

    # Opcodes:
    # 211 octal -> 0x89 (LDB - Load B-line)
    # 322 octal -> 0xD2 (ADA - Add to Acc)
    # 203 octal -> 0x83 (SBB - Subtract from B-line)
    # 221 octal -> 0x91 (JBN - Jump if B != 0)
    # 1000 octal -> 0x200 (Print)
    # 0 octal -> 0x0 (HALT)

    program = [
        # 0: Load B1 with count (5)
        join_instruction(0x089, 1, 0, 101),
        # 1: Start Loop - Add Increment to Acc
        join_instruction(0x0D2, 0, 0, 100),
        # 2: Subtract 1 from B1 (read from memory)
        join_instruction(0x083, 1, 0, 102),
        # 3: If B1 != 0, Jump back to instruction 1
        join_instruction(0x091, 1, 0, 1),
        # 4: Print Result
        join_instruction(0x200, 0, 0, 0),
        # 5: Halt
        join_instruction(0x000, 0, 0, 0)
    ]

    for i, inst in enumerate(program):
        mem.write(i, inst)

    print(f"Starting execution (5 * 3)...")
    cpu.run(0)
    print("Execution finished.")

if __name__ == "__main__":
    main()
