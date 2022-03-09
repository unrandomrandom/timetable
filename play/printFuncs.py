#helper
# prints a 3 * 7 * 42 | 3 * 7 * [9,9,9,9,6] thing nicely
def dumpStudentAllocation(data):

    f  = open('studentdump.txt', "w+")

    periodsPerDay = [
        9,
        9,
        9,
        9,
        6
    ]

    # data[0].classes[0].periods[0][0]

    for grade in range(3):
        foo = 0
        for row in range(5):
            myStr = ''
            for section in range(7):
                counter = 0
                smallStr = ''
                while counter < periodsPerDay[foo]:
                    smallStr += str(data[grade].classes[section].periods[row][counter]).center(15) + ", "
                    counter += 1
                smallStr = smallStr.ljust(200)    
                smallStr += " | "
                myStr += smallStr
            myStr += "\n"
            foo += 1
            f.write(myStr)
        f.write("\n ---------------------------------------------------------- \n")

    f.close()


def dumpTeacherAllocation(data: dict):
    f  = open('teacherdump.txt', "w+")

    periodsPerDay = [
        9,
        9,
        9,
        9,
        6
    ]

    for trName, schedule in data.items():
        f.write(trName)
        f.write("\n")
        for day in range(5):
            f.write(str(data[trName][day]).ljust(70))
            f.write("\n")
        f.write("\n\n")

    # for day in range(5):
    #     myStr = ''
    #     for tr in list(data):
    #         myStr += str(data[tr][day]).ljust(70)
    #         myStr += ' | '
    #     myStr += '\n'
    #     f.write(myStr)

    # for trName in data.keys():
    #     f.write(trName)

    f.close()
    