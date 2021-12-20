from driver import Driver

if __name__ == '__main__':
    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "First part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="test")
    d.ls()
    d.cd(path="test")
    d.ls()
    d.cd(path="..")
    d.ls()

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Second part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="test")
    d.mkdir(name="test1")
    d.ls()
    d.cd(path="test")
    d.rmdir(name="../test1")
    d.cd(path="..")
    d.ls()

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Third part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="test")
    d.mkdir(name="test1")
    d.mkdir(name="test/test12")
    d.mkdir(name="test/test12/test123")
    d.ls()
    d.cd(path="test")
    d.ls()
    d.cd(path="test12")
    d.ls()

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Fourth part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="test1")
    d.mkdir(name="test1/../test2")
    d.mkdir(name="test1/test11")
    d.mkdir(name="./test1/test11/test111")
    d.ls()
    d.cd(path="test1")
    d.ls()
    d.cd(path="../test1/test11")
    d.ls()

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Fifth part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="test")
    d.mkdir(name="test/test1")
    d.mkdir(name="test/test1/test11")
    d.symlink(string="test/test1/test11", path="sym_test11")
    d.create(name="sym_test11/text.txt")
    d.ls()
    d.cd(path="test/test1/test11")
    d.ls()
    d.cd(path="../../..")
    fd1 = d.open(name="sym_test11/text.txt")
    d.write(fd=fd1, offset=0, size=5, data="hello")
    d.read(fd=fd1, offset=0, size=5)

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Sixth part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="a")
    d.mkdir(name="a/b")
    d.mkdir(name="a/b/c")
    d.mkdir(name="a/b/c/d")
    d.mkdir(name="a/b/c/d/e")
    d.mkdir(name="a/b/c/d/e/f")
    d.mkdir(name="a/b/c/d/e/f/g")
    d.mkdir(name="a/b/c/d/e/f/g/h")
    d.cd(path="a/b/c")
    d.symlink(string="d/e/f", path="1")
    d.cd(path="..")
    d.symlink(string="c/1/g", path="2")
    d.ls()
    d.cd(path="2")
    d.ls()

    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|" +
        " " * 16 + "Seventh part" + " " * 16 +
        "|\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

    d = Driver()
    d.mkdir(name="a")
    d.mkdir(name="a/b")
    d.mkdir(name="a/b/c")
    d.cd(path="a/b/c")
    d.symlink(string="/a/b", path="1")
    d.create(name="1/text.txt")
    d.cd(path="..")
    d.ls()
    d.cd(path="/.")
    d.ls()
