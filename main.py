from driver import Driver

if __name__ == '__main__':
    driver = Driver()
    driver.mount()
    driver.create(name='file.txt')
    print("File 'file.txt' has been created.")

    fd1 = driver.open(name='file.txt')
    print("File descriptor #{} for 'file.txt' has opened.".format(fd1))
    driver.link(name1='file.txt', name2='document.txt')
    print("Link between 'file.txt' and 'document.txt' has been created")

    driver.unlink(name='file.txt')
    print("Link for 'file.txt' has been removed from file system.")

    fd2 = driver.open(name="document.txt")
    print("File descriptor #{} for 'file.txt' has opened.".format(fd2))

    driver.unlink(name="document.txt")
    print("Link for 'document.txt' has been removed from file system.")

    driver.write(fd=fd1, offset=0, size=5, data="hello")
    print("Reading data of 'file.txt': {}".format(driver.read(fd=fd2, offset=0, size=5)))
    driver.close(fd=fd2)
    print("File descriptor #{} has been closed.".format(fd2))
    driver.close(fd=fd1)
    print("File descriptor #{} has been closed.".format(fd1))

    print("Returning of read command return None value: {}.".format(driver.read(fd=fd2, offset=0, size=5)))
    print("Returning of read command return None value: {}.".format(driver.read(fd=fd1, offset=0, size=5)))
    driver.link(name1='file.txt', name2='document.txt')
    print("Link between 'file.txt' and 'document.txt' has been created")
    fd2 = driver.open(name="document.txt")
    print("File descriptor #{} for 'document.txt' has opened.".format(fd2))

    driver.create(name='file.txt')
    print("File 'file.txt' has been created.")

    driver.truncate(name='file.txt', size=10)
    print("Size of 'file.txt' has been changed to 10")
    fd = driver.open(name='file.txt')
    print("File descriptor #{} for 'file.txt' has opened.".format(fd))
    print("Reading data of 'file.txt': {}".format(driver.read(fd=fd, offset=0, size=10)))
    driver.truncate(name='file.txt', size=5)
    print("Size of 'file.txt' has been changed to 5")
    print("Reading data of 'file.txt': {}".format(driver.read(fd=fd, offset=0, size=10)))
