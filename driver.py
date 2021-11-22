from file_system import FileSystem


class Driver:
    FS = FileSystem(100)

    def __init__(self):
        self.fs = None or self.FS

    def mkfs(self, fd):
        self.fs = FileSystem(fd)

    def mount(self):
        self.fs = self.FS

    def unmount(self):
        self.fs = None

    def fstat(self, name):
        if self.exist():
            self.fs.find_file_descriptor_by_name(name)

    def ls(self):
        if self.exist():
            self.fs.dir.dir_links()

    def create(self, name):
        if self.exist():
            self.fs.create_file(name)

    def open(self, name):
        if self.exist():
            file = self.fs.find_file_descriptor_by_name(name)
            return self.fs.open(file)

    def close(self, fd):
        if self.exist():
            self.fs.close(fd)

    def read(self, fd, offset, size):
        data = ''
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            if file:
                for block in self.fs.read_file(offset, size, file):
                    data += block.data[0:size]
            else:
                return None

        return data

    def write(self, fd, offset, size, data):
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            self.fs.write_file(offset, size, data, file)

    def link(self, name1, name2):
        if self.exist():
            fd = self.fs.find_file_descriptor_by_name(name1)
            if fd:
                self.fs.create_link(name2, fd)

    def unlink(self, name):
        if self.exist():
            link = self.fs.find_link_by_name(name)
            self.fs.remove_link(link)

    def truncate(self, name, size):
        if self.exist():
            file = self.fs.find_file_descriptor_by_name(name)
            self.fs.truncate_file(file, size)

    def exist(self):
        return self.fs is not None
