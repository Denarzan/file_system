class FileDescriptor:
    def __init__(self, is_dir=False, is_file=False):
        self.is_dir = is_dir
        self.is_file = is_file
        self.number_of_links = 0
        self.blocks = {}
        self.dir_links = []

    def size(self):
        size_of_blocks = 0
        for block in self.blocks.values():
            size_of_blocks += len(block.data)
        return size_of_blocks if self.is_file else None
