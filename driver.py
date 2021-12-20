from file_system import FileSystem


class Driver(object):
    FS = FileSystem(100)

    def __init__(self):
        self.fs = None or self.FS

    def _separator(func):
        def wrapper(self):
            print("->->->->->->->->->->->->->->->->->->->")
            func(self)
            print("<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-")
        return wrapper

    def mkfs(self, fd):
        self.fs = FileSystem(fd)

    def mount(self):
        self.fs = self.FS

    def unmount(self):
        self.fs = None

    def fstat(self, name):
        if self.exist():
            return self.fs.find_file_descriptor_by_name(name)

    @_separator
    def ls(self):
        if self.exist():
            message = "| Show content of current directory: |"
            print(message)
            for link in self.fs.dir.dir_links:
                print("|     " + link.name + " " * (len(message) - len(link.name) - 7) + "|")

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

    def read(self, fd, offset, size):
        data = ''
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            if file:
                for block in self.fs.read_file(offset, size, file):
                    data += block.data[0:size]
            else:
                return None
        print(f"Reading file descriptor #{fd}: {data}")

    def write(self, fd, offset, size, data):
        if self.exist():
            file = self.fs.find_file_by_number_of_fd(fd)
            if file:
                print(f"Writing data to file descriptor #{fd}")
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
                print(f"Size of {name} has been changed to {size}")
                return self.fs.truncate_file(file, int(size))

    def mkdir(self, name):
        if self.exist():
            print(f"Created directory {name}")
            return self.fs.create_directory(name)

    def rmdir(self, name):
        if self.exist():
            print(f"Directory {name} has been removed")
            return self.fs.remove_directory(name)

    def cd(self, path):
        if self.exist():
            print(f"Switch directory to {path}")
            return self.fs.change_directory(path)

    def symlink(self, string, path):
        if self.exist():
            print(f"Created symbolic link to {path} with {string} path")
            return self.fs.create_symlink(string, path)

    def exist(self):
        return self.fs is not None
