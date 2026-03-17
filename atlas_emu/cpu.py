from .utils import split_instruction, mask_48, mask_24, to_signed_24, from_signed_24
from .instructions import InstructionSet

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.instruction_set = InstructionSet(self)
        
        # Accumulator (48-bit)
        self.accumulator = 0
        
        # B-Store (128 registers, 24-bit each)
        self.b_store = [0] * 128
        
        # CPU Status
        self.running = False

    @property
    def pc(self):
        """Program Counter is B127."""
        return self.b_store[127]

    @pc.setter
    def pc(self, val):
        self.b_store[127] = mask_24(val)

    def fetch(self):
        """Read 48-bit instruction from memory at current PC."""
        instruction_word = self.memory.read(self.pc)
        self.pc += 1
        return instruction_word

    def decode(self, word):
        """Split the 48-bit word into its components."""
        return split_instruction(word)

    def step(self):
        """Execute a single instruction cycle."""
        if not self.running:
            return
            
        word = self.fetch()
        f, ba, bm, s = self.decode(word)
        
        # Address Modification (Double Modification was an Atlas feature)
        # S' = S + B[Bm]
        effective_addr = mask_24(s + self.b_store[bm])
        
        # Execute
        self.instruction_set.execute(f, ba, bm, effective_addr)
        
        # Ensure B0 is always zero
        self.b_store[0] = 0

    def run(self, start_pc):
        self.pc = start_pc
        self.running = True
        while self.running:
            self.step()
