from random import choice

# prints a 3 * 7 * 42 thing nicely
def printNicely(data):

    f  = open('playdump.txt', "w+")

    periodsPerDay = [
        9,
        9,
        9,
        9,
        6
    ]

    if type(data[0][0][0]) is not list:
        for grade in range(3):
            foo = 0
            for row in range(5):
                myStr = ''
                for section in range(7):
                    counter = 0
                    while counter < periodsPerDay[foo]:
                        myStr += str(data[grade][section][sum(periodsPerDay[:foo]) + counter]).center(5) + ", "
                        counter += 1
                    myStr = myStr.ljust(70)    
                    myStr += " | "
                myStr += "\n"
                foo += 1
                f.write(myStr)
            f.write("\n ---------------------------------------------------------- \n")

    else:
        for grade in range(3):
            foo = 0
            for row in range(5):
                myStr = ''
                for section in range(7):
                    counter = 0
                    while counter < periodsPerDay[foo]:
                        myStr += str(data[grade][section][row][counter]).center(5) + ", "
                        counter += 1
                    myStr = myStr.ljust(70)    
                    myStr += " | "
                myStr += "\n"
                foo += 1
                f.write(myStr)
            f.write("\n ---------------------------------------------------------- \n")

    f.close()





def test():

    studentTimeTable = []
    for grades in range(3):
        oneGrade = []
        for divisions in range(7):
            oneClass = [
                [''] * 9,     # monday
                [''] * 9,     # tuesday 
                [''] * 9,     # wednesday
                [''] * 9,     # thursday
                [''] * 6,     # friday
            ]
            oneGrade.append(oneClass)
        studentTimeTable.append(oneGrade)

    studentTimeTable[0][0][0][0] = 'xvcb'

    printNicely(studentTimeTable)

test()