from driver import Driver

if __name__ == '__main__':
    driver = Driver()
    driver.mount()
    driver.create(name='file.txt')

    fd1 = driver.open(name='file.txt')
    driver.link(name1='file.txt', name2='document.txt')
    driver.unlink(name='file.txt')
    fd2 = driver.open(name="document.txt")
    driver.unlink(name="document.txt")
    driver.write(fd=fd1, offset=0, size=5, data="hello")

    driver.close(fd=fd2)
    driver.close(fd=fd1)

    driver.link(name1='file.txt', name2='document.txt')
    fd2 = driver.open(name="document.txt")

    driver.create(name='file.txt')

    driver.truncate(name='file.txt', size=10)

    fd = driver.open(name='file.txt')
    driver.truncate(name='file.txt', size=5)
