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
            return self.fs.find_file_descriptor_by_name(name)

    def ls(self):
        if self.exist():
            for link in self.fs.dir.dir_links:
                print(link.name)

    def create(self, name):
        if self.exist():
            print(f"File {name} has been created.")
            return self.fs.create_file(name)

    def open(self, name):
        if self.exist():
            file = self.fs.find_file_descriptor_by_name(name)
            if file:
                print(f"File descriptor #{file.number_of_links} for {name} has opened.")
                return self.fs.open(file)

    def close(self, fd):
        if self.exist():
            print(f"File descriptor #{fd} has been closed.")
            return self.fs.close(fd)

    def read(self, fd, offset, size, data):
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            if file:
                return self.fs.write_file(int(offset), int(size), data, file)
            else:
                return None

    def write(self, fd, offset, size, data):
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            if file:
                print(f"Writing data to {file}")
                return self.fs.write_file(int(offset), int(size), data, file)

    def link(self, name1, name2):
        if self.exist():
            fd = self.fs.find_file_descriptor_by_name(name1)
            if fd:
                print(f"Link between {name1} and {name2} has been created")
                return self.fs.create_link(name2, fd)

    def unlink(self, name):
        if self.exist():
            link = self.fs.find_link_by_name(name)
            if link:
                print(f"Link for {name} has been removed from file system.")
                return self.fs.remove_link(name, link)

    def truncate(self, name, size):
        if self.exist():
            file = self.fs.find_file_descriptor_by_name(name)
            if file:
                print(f"Size of {file} has been changed to {size}")
                return self.fs.truncate_file(file, int(size))

    def mkdir(self, name):
        if self.exist():
            return self.fs.create_directory(name)

    def rmdir(self, name):
        if self.exist():
            return self.fs.remove_directory(name)

    def cd(self, path):
        if self.exist():
            return self.fs.change_directory(path)

    def symlink(self, string, path):
        if self.exist():
            return self.fs.create_symlink(string, path)

    def exist(self):
        return self.fs is not None
