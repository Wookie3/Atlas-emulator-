from .utils import mask_48

# Atlas standard: 512 words per page
PAGE_SIZE = 512
PAGE_BITS = 9 # log2(512)
ADDRESS_BITS = 24
PAGE_MASK = 0x1FF

class Memory:
    """
    Simulates the Atlas 'One-Level Store' (Virtual Memory).
    """
    def __init__(self, core_blocks=32, drum_pages=1024):
        # Physical Core Store (RAM)
        self.core_store = [0] * (core_blocks * PAGE_SIZE)
        
        # Backing Drum Store (Simulated Disk)
        # Using a dictionary to save memory for unused pages
        self.drum_store = {} 
        
        # Page Address Registers (PAR)
        # Maps virtual_page_number -> core_block_index
        self.par = {}
        
        # Simple list of free core blocks for allocation
        self.free_core_blocks = list(range(core_blocks))
        
        # Reverse mapping: core_block -> virtual_page_number
        self.core_to_virtual = {}

    def _get_page_indices(self, virtual_addr):
        virtual_page = virtual_addr >> PAGE_BITS
        offset = virtual_addr & PAGE_MASK
        return virtual_page, offset

    def _page_fault(self, virtual_page):
        """
        Triggered when a virtual page is not in Core Store.
        In a real Atlas, this would trigger a supervisor interrupt.
        Here we handle it synchronously for simplicity.
        """
        if not self.free_core_blocks:
            # Simple 'victim' selection (Atlas used a Learning Program)
            # We'll just pick the first core block to swap out
            victim_block = 0 
            old_vp = self.core_to_virtual[victim_block]
            
            # Write victim back to Drum
            page_data = self.core_store[victim_block * PAGE_SIZE : (victim_block + 1) * PAGE_SIZE]
            self.drum_store[old_vp] = list(page_data)
            
            # Clean up mappings
            del self.par[old_vp]
            self.free_core_blocks.append(victim_block)

        # Assign new core block
        new_block = self.free_core_blocks.pop(0)
        
        # Load data from Drum if it exists, otherwise initialize to zero
        if virtual_page in self.drum_store:
            data = self.drum_store[virtual_page]
            self.core_store[new_block * PAGE_SIZE : (new_block + 1) * PAGE_SIZE] = data
        else:
            # Page never written before, initialize with zeros
            for i in range(PAGE_SIZE):
                self.core_store[new_block * PAGE_SIZE + i] = 0
        
        # Update PAR
        self.par[virtual_page] = new_block
        self.core_to_virtual[new_block] = virtual_page

    def read(self, virtual_addr):
        vp, offset = self._get_page_indices(virtual_addr)
        
        if vp not in self.par:
            self._page_fault(vp)
            
        block = self.par[vp]
        return self.core_store[block * PAGE_SIZE + offset]

    def write(self, virtual_addr, val):
        vp, offset = self._get_page_indices(virtual_addr)
        
        if vp not in self.par:
            self._page_fault(vp)
            
        block = self.par[vp]
        self.core_store[block * PAGE_SIZE + offset] = mask_48(val)
