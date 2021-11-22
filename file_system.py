from file_descriptor import FileDescriptor
from link import Link
from block import Block

BLOCK_SIZE = 512


class FileSystem:
    def __init__(self, amount_file_descriptors):
        self.amount_file_descriptors = amount_file_descriptors
        self.dir = FileDescriptor(is_dir=True)
        self.number_of_file_descriptors = 1
        self.opened_descriptors = {}

    def find_file_by_number_of_fd(self, numeric_fd):
        return self.opened_descriptors[numeric_fd] if numeric_fd in list(self.opened_descriptors.keys()) else None

    def find_link_by_name(self, name):
        for link in self.dir.dir_links:
            if link.active and link.name == name:
                return link
        return None

    def find_file_descriptor_by_name(self, name):
        link = self.find_link_by_name(name)
        return link.file_descriptor if link else None

    def create_file(self, name):
        if self.number_of_file_descriptors + 1 < self.amount_file_descriptors:
            file = FileDescriptor(is_file=True)
            link = Link(name, file)
            file.number_of_links += 1
            self.dir.dir_links.append(link)

    def open(self, fd):
        if self.opened_descriptors:
            number_of_fd = list(self.opened_descriptors.keys())[-1] + 1

        else:
            number_of_fd = self.number_of_file_descriptors
        self.opened_descriptors[number_of_fd] = fd
        return number_of_fd

    def close(self, number_of_fd):
        file = self.find_file_by_number_of_fd(number_of_fd)
        self.opened_descriptors.pop(int(number_of_fd))
        if file.number_of_links == 0 and file not in self.opened_descriptors.values():
            file.blocks.clear()

    def create_link(self, name, fd):
        link = Link(name, fd)
        fd.number_of_links += 1
        self.dir.dir_links.append(link)

    def remove_link(self, link):
        link.file_descriptor.number_of_links -= 1
        link.active = False
        if link.file_descriptor.number_of_links == 0 and link.file_descriptor not in list(self.opened_descriptors.values()):
            link.file_descriptor.blocks.clear()
        self.dir.dir_links.remove(link)

    @staticmethod
    def read_file(offset, size, file):
        result = []

        for block_offset, block in file.blocks.items():
            if len(result) == 0:
                if offset < block_offset:
                    continue
                else:
                    result.append(block)
            elif (offset + size) > block_offset:
                result.append(block)
            else:
                break
        return result

    @staticmethod
    def write_file(offset, size, data, file):
        current_block = None if len(file.blocks) == 0 else list(file.blocks.values())[0]

        for block_offset, block in file.blocks.items():
            if offset <= block_offset:
                current_block = block
                break

        if current_block is None:
            current_block = Block()
            file.blocks[0] = current_block

        if BLOCK_SIZE - current_block.size() > size:
            current_block.data += data[0:BLOCK_SIZE - current_block.size()]
            data = data[0:BLOCK_SIZE - current_block.size()]

        if len(data) != 0:
            blocks_size = 1 if size / BLOCK_SIZE <= 1 else size / BLOCK_SIZE + 1
            for block_id in range(blocks_size):
                if len(data) <= BLOCK_SIZE:
                    file.blocks[BLOCK_SIZE * (block_id + file.size() / BLOCK_SIZE)] = Block(data)
                else:
                    file.blocks[BLOCK_SIZE * (block_id + file.size() / BLOCK_SIZE)] = Block(data[0, BLOCK_SIZE])

    @staticmethod
    def truncate_file(file, size):
        if file.size() < size:
            current_block = None
            data = '0' * size
            if len(file.blocks) != 0:
                current_block = list(file.blocks.values())[-1]

            if current_block is None:
                current_block = Block()
                file.blocks[0] = current_block

            if BLOCK_SIZE - current_block.size() >= size - file.size():
                current_block.data += data[0:BLOCK_SIZE - current_block.size()]
                data = data[0:BLOCK_SIZE - current_block.size()]

            if len(data) != 0:
                blocks_size = 1 if len(data) / BLOCK_SIZE <= 1 else len(data) / BLOCK_SIZE + 1
                for block_id in range(blocks_size):
                    if len(data) <= BLOCK_SIZE:
                        file.blocks[BLOCK_SIZE * (block_id + 1 + file.size() / BLOCK_SIZE)] = Block(data)
                    else:
                        file.blocks[BLOCK_SIZE * (block_id + 1 + file.size() / BLOCK_SIZE)] = Block(data[0:BLOCK_SIZE])
        else:
            offset, current_block = list(file.blocks.items())[0]
            for block_offset, block in file.blocks.items():
                if (block_offset + block.size()) >= size:
                    offset, current_block = block_offset, block
                    break
            current_block.data = current_block.data[0:size - int(offset)]
            if len(file.blocks) == 1:
                return
            for out_offset in list(file.blocks.keys())[int(offset) + 1:]:
                file.blocks.pop(out_offset)
