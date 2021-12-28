import copy

from file_descriptor import FileDescriptor
from link import Link
from block import Block

BLOCK_SIZE = 512


class FileSystem:
    def __init__(self, amount_file_descriptors):
        self.amount_file_descriptors = amount_file_descriptors
        self.number_of_file_descriptors = 1
        self.opened_descriptors = {}
        self.dir = FileDescriptor(is_dir=True)
        self.root_dir = self.dir
        self.dir.dir_links.append(Link("..", self.dir))
        self.dir.dir_links.append(Link(".", self.dir))

    def find_file_by_number_of_fd(self, numeric_fd):
        return self.opened_descriptors[numeric_fd] if numeric_fd in list(self.opened_descriptors.keys()) else None

    def find_link_by_name(self, name):
        parent_directory = self.find_dir_by_path("/".join(name.split('/')[0:-1])) if self.is_path(name) else self.dir
        names = name.split('/') if self.is_path(name) else name
        for link in parent_directory.dir_links:
            if link.active and link.name == names[-1]:
                return link

    def find_file_descriptor_by_name(self, name):
        link = self.find_link_by_name(name)
        return link.file_descriptor if link else None

    def find_dir_by_path(self, path):
        current_directory = None
        splitted_path = path.split('/')
        splitted_path_with_symlink = self.concatenation_symlink(splitted_path)
        if splitted_path_with_symlink and len(splitted_path_with_symlink[0]) == 0:
            current_directory = self.root_dir
        index = 0
        for component in splitted_path_with_symlink:
            if not component and index == 0:
                continue
            if component == ".":
                current_directory = current_directory if current_directory else self.dir
            else:
                link_current_directory = self.find_directory_link(component, current_directory.dir_links if current_directory else self.dir.dir_links)
                current_directory = link_current_directory.file_descriptor if link_current_directory else None
        return current_directory

    def concatenation_symlink(self, splitted_path):
        result = copy.deepcopy(splitted_path)
        current_directory = self.root_dir if not splitted_path[0] else None
        index = 0
        for component in splitted_path:
            if not component and index == 0:
                continue
            if component == ".":
                current_directory = current_directory if current_directory else self.dir
            else:
                link_current_directory = self.find_directory_link(component, current_directory.dir_links if current_directory else self.dir.dir_links)
                current_directory = link_current_directory.file_descriptor if link_current_directory else None
            if current_directory and current_directory.is_symlink:
                index = result.index(component)
                res = ''
                for block in current_directory.blocks.values():
                    res += block.data
                res = res.split('/')
                result = result[:index] + res + result[index+1:]
            index += 1
        return self.concatenation_symlink(result) if self.any_symlink(result) else result

    def any_symlink(self, splitted_path):
        condition = []
        if len(splitted_path[0]) == 0:
            current_directory = self.root_dir
        else:
            current_directory = None
        index = 0
        for component in splitted_path:
            if not component and index == 0:
                continue
            if hasattr(current_directory, "dir_links"):
                for link in current_directory.dir_links:
                    if link.file_descriptor.is_symlink and link.name == component:
                        condition.append(True)
            if component == ".":
                current_directory = current_directory if current_directory else self.dir
            else:
                link_current_directory = self.find_directory_link(component, current_directory.dir_links if current_directory else self.dir.dir_links)
                current_directory = link_current_directory.file_descriptor if link_current_directory else None
            index += 1
        return any(condition)

    def create_file(self, name):
        parent_directory = self.find_dir_by_path("/".join(name.split('/')[0:-1])) if self.is_path(name) else self.dir
        name = name.split('/')[-1] if self.is_path(name) else name
        file = FileDescriptor(is_file=True)
        link = Link(name, file)
        file.number_of_links += 1
        if parent_directory:
            parent_directory.dir_links.append(link)

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
        parent_directory = self.find_dir_by_path("/".join(name.split('/')[0:-1])) if self.is_path(name) else self.dir
        name = name.split('/') if self.is_path(name) else name
        link = Link(name, fd)
        fd.number_of_links += 1
        parent_directory.dir_links.append(link)

    def remove_link(self, name, link):
        parent_directory = self.find_dir_by_path("/".join(name.split('/')[0:-1])) if self.is_path(name) else self.dir
        link.file_descriptor.number_of_links -= 1
        link.active = False
        if link.file_descriptor.number_of_links == 0 and link.file_descriptor not in list(
                self.opened_descriptors.values()):
            link.file_descriptor.blocks.clear()
        parent_directory.dir_links.remove(link)

    def create_directory(self, path):
        if path in ['.', '..']:
            return
        parent_directory = self.find_dir_by_path("/".join(path.split('/')[0:-1])) if self.is_path(path) else self.dir
        new_directory = FileDescriptor(is_dir=True)
        link_name, link_fd = path.split('/')[-1] if self.is_path(path) else path, new_directory
        directory_link = Link(link_name, link_fd)
        new_directory.dir_links.append(Link(".", new_directory))
        if not parent_directory:
            return
        new_directory.dir_links.append(Link("..", parent_directory))
        parent_directory.dir_links.append(directory_link)

    def remove_directory(self, path):
        if path in ['.', '..']:
            return
        parent_directory = self.find_dir_by_path("/".join(path.split('/')[0:-1])) if self.is_path(path) else self.dir
        # print(">>>>>>", "/".join(path.split('/')[0:-1]))
        if not parent_directory:
            return
        link_name, link_fd = path.split('/')[-1] if self.is_path(path) else path, parent_directory.dir_links
        directory = self.find_directory_link(link_name, link_fd)
        parent_directory.dir_links.remove(directory)

    def change_directory(self, path):
        name = path.split('/') if self.is_path(path) else path
        if self.is_path(path):
            directory = self.find_dir_by_path(path)
        else:
            directory = self.find_directory_link(name, self.dir.dir_links).file_descriptor \
                if self.find_directory_link(name, self.dir.dir_links) else None
        if directory:
            self.dir = directory

    def create_symlink(self, string, path):
        file_descriptor = FileDescriptor(is_symlink=True)
        self.write_file(0, len(string), string, file_descriptor)
        link_name, link_fd = path.split('/')[-1] if self.is_path(path) else path, file_descriptor
        link = Link(link_name, link_fd)
        parent_directory = self.find_dir_by_path("/".join(path.split('/')[0:-1])) if self.is_path(path) else self.dir
        parent_directory.dir_links.append(link)

    def is_path(self, path):
        splitted_path = path.split('/')
        for link in self.dir.dir_links:
            if link.file_descriptor.is_symlink and link.name == path:
                return True
        return len(splitted_path) != 1

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

    @staticmethod
    def find_directory_link(name, links):
        for link in links:
            if (link.file_descriptor.is_dir or link.file_descriptor.is_symlink) and link.name == name:
                return link
