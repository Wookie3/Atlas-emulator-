from .utils import mask_48, mask_24, to_signed_24, from_signed_24

# Simple instruction set mapping (Atlas Machine Instructions)
# These are illustrative subsets of the real Atlas opcodes

class InstructionSet:
    def __init__(self, cpu):
        self.cpu = cpu
        self.memory = cpu.memory

    def execute(self, f, ba, bm, s_prime):
        """
        f: 10-bit opcode
        ba: B-index 1
        bm: B-index 2 (already used for s_prime calculation)
        s_prime: effective address (s + B[bm])
        """
        
        # B-Store Instructions (Atlas 100-277 octal, approx)
        if f == 0x089: # 211 octal (LDB - Load B-line)
            self.cpu.b_store[ba] = mask_24(self.memory.read(s_prime))
            
        elif f == 0x08D: # 215 octal (STB - Store B-line)
            self.memory.write(s_prime, self.cpu.b_store[ba])
            
        elif f == 0x081: # 201 octal (ADB - Add to B-line)
            val = self.memory.read(s_prime)
            self.cpu.b_store[ba] = mask_24(self.cpu.b_store[ba] + val)

        elif f == 0x083: # 203 octal (SBB - Subtract from B-line)
            val = self.memory.read(s_prime)
            self.cpu.b_store[ba] = mask_24(self.cpu.b_store[ba] - val)
            
        elif f == 0x084: # 204 octal (DVB - Divide B-line)
            val = self.memory.read(s_prime)
            if val != 0:
                self.cpu.b_store[ba] = mask_24(self.cpu.b_store[ba] // val)
            else:
                print("Division by zero!")
                self.cpu.running = False
                
        elif f == 0x082: # 202 octal (MLB - Multiply B-line)
            val = self.memory.read(s_prime)
            self.cpu.b_store[ba] = mask_24(self.cpu.b_store[ba] * val)

        # Control Instructions
        elif f == 0x08F: # 217 octal (JBZ - Jump if B[ba] == 0)
            if self.cpu.b_store[ba] == 0:
                self.cpu.pc = s_prime
                
        elif f == 0x091: # 221 octal (JBN - Jump if B[ba] != 0)
            if self.cpu.b_store[ba] != 0:
                self.cpu.pc = s_prime

        # Accumulator Instructions (Atlas 300-377 octal)
        elif f == 0x0EE: # 356 octal (LDA - Load Accumulator)
            self.cpu.accumulator = self.memory.read(s_prime)
            
        elif f == 0x0F2: # 362 octal (STA - Store Accumulator)
            self.memory.write(s_prime, self.cpu.accumulator)
            
        elif f == 0x0D2: # 322 octal (ADA - Add to Accumulator)
            val = self.memory.read(s_prime)
            self.cpu.accumulator = mask_48(self.cpu.accumulator + val)

        elif f == 0x0D3: # 323 octal (SBA - Subtract from Accumulator)
            val = self.memory.read(s_prime)
            self.cpu.accumulator = mask_48(self.cpu.accumulator - val)
            
        elif f == 0x0D4: # 324 octal (DIV - Divide Accumulator)
            val = self.memory.read(s_prime)
            if val != 0:
                self.cpu.accumulator = mask_48(self.cpu.accumulator // val)
            else:
                print("Division by zero!")
                self.cpu.running = False
                
        elif f == 0x0D5: # 325 octal (MLA - Multiply Accumulator)
            val = self.memory.read(s_prime)
            self.cpu.accumulator = mask_48(self.cpu.accumulator * val)

        # System Instructions
        elif f == 0x000: # HALT (Simplified)
            self.cpu.running = False

        else:
            # Not implemented or Extracode (f >= 0x200)
            if f >= 0x200:
                self.handle_extracode(f, ba, bm, s_prime)
            else:
                print(f"Unknown Opcode: {oct(f)}")
                self.cpu.running = False

    def handle_extracode(self, f, ba, bm, s_prime):
        """Phase 4: High-Level Emulation of Atlas Extracodes."""
        # Extracode 1000 octal (Print Accumulator)
        if f == 0x200: # 1000 octal
            print(f"> OUTPUT: {self.cpu.accumulator}")
        else:
            print(f"Extracode Not Implemented: {oct(f)}")
