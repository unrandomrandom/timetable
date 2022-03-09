from os import chdir, getcwd

def changePathDecorator(func):
    def runner():
        ogDir = getcwd()
        chdir('..')
        chdir(getcwd() + "\\data")
        func()
        chdir(ogDir)
    return runner()

def decorator_list(fnc):
    print("called 1")
    def inner(list_of_tuples):
        print("called 2")
        return [fnc(val[0], val[1]) for val in list_of_tuples]
    return inner


@decorator_list
def add_together(a, b):
    print("called 3")
    return a + b


print(add_together([(1, 3), (3, 17), (5, 5), (6, 7)]))