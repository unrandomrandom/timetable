from openpyxl import Workbook, load_workbook
from os import getcwd, chdir
from pprint import pprint
from json import dumps
from random import choice
import numpy as np


###########################################
# the spreadsheet parser
###########################################
chdir(getcwd() + "/data")

# helper
def nextIndex(currentIndex):
    if type(currentIndex) is not str:
        raise TypeError("expected str but got " + type(currentIndex))
    if currentIndex.isalpha():
        # split the string into its chars, all uppercase 
        foo = list(map(lambda x: x.upper(), list(currentIndex)))
        i = -1
        increment = True
        while i >= -1 * len(currentIndex) and increment is True:
            if foo[i] == 'Z':
                if i == -1 * len(currentIndex):
                    foo[i] = 'AA'
                    increment = False
                else:
                    # the character behind this needs to be incremented as well
                    foo[i] = 'A'
            else:
                foo[i] = chr(ord(foo[i]) + 1)
                increment = False
            i -= 1
        return ''.join(foo)
    elif currentIndex.isnumeric():
        return str(int(currentIndex) + 1)
    else:
        return ValueError("Invalid index passed")

def classWiseTeacherAllocation():
    teacherColumn = "B"
    classColumn = "C"
    subjectRow = "9"
    subjectColumnRanges = ["D", "U"]  #both inclusive
    classRowRanges = ["10", "30"] #both inclusive
    workbook = load_workbook(filename="6.  CLASS ALLOCATION 2020-2021  (MIDDLE BOYS- (1).xlsx")
    s = workbook.active
    teacherSubject = {}
    classSubjectTeacher = {}
    classClassTeacher = {}
    '''
    {
        teacher: {
            class: {
                subject1,
                subject2,
                subject3
            }
        }
    }
    '''
    i = classRowRanges[0]

    while i != nextIndex(classRowRanges[1]):
        className = s[classColumn + i].value
        classTeacherName = s[teacherColumn+i].value
        classClassTeacher[className] = classTeacherName    
        classSubjectTeacher[className] = {}

        j = subjectColumnRanges[0]
        while j != nextIndex(subjectColumnRanges[1]):    
            teacherName = s[j+i].value
            # split by space and see if each substring is alphabetic
            truefalse = list(map(lambda x: x.isalpha(), teacherName.split(' ')))
            if set(truefalse) == set([True]):
                #getting the cell value
                subjectName = s[j+subjectRow].value
                #carefully filling in teacherSubject
                if teacherName not in teacherSubject:
                    teacherSubject[teacherName] = {}
                if subjectName not in teacherSubject[teacherName]:
                    teacherSubject[teacherName][subjectName] = [className]
                else:
                    teacherSubject[teacherName][subjectName].append(className)
                #filling in classSubjectTeacher
                classSubjectTeacher[className][subjectName] = teacherName
            else:
                print("in location " + j + " " + i + " no teacher name was found")
            j = nextIndex(j)
        i = nextIndex(i)
    
    # to test
    # print(dumps(classSubjectTeacher, indent=4))

    with open("class_subject_and_teacher.json", "w+") as f:
        f.write(dumps(classSubjectTeacher, indent=4))

    with open("teacher_class_and_subject.json", "w+") as f:
        f.write(dumps(teacherSubject, indent=4))

    return teacherSubject, classSubjectTeacher



###########################################
# the time table generation
###########################################


# constants
# "I.ED/GK" is 2 separate periods in the spreadsheet
periodsPerWeek = {
    "ENGLISH": 5,
    "HINDI": 5,
    "MATHEMATICS": 5,
    "SCIENCE": 5,
    "SOCIAL SCIENCE": 5,
    "ARABIC": 4,
    "USST": 2,
    "I.ED/GK": 2,
    "COMP SC": 3,
    "LIBRARY": 1,
    "CLUB": 1,
    "MUSIC": 1,
    "ART": 1,
    "WELL BEING": 1
}

subjectsByWeight = {
    1: [
        "ARABIC",
        "USST",
        "I.ED/GK",
        "COMP SC",
        "LIBRARY" ,
        "CLUB" ,
        "MUSIC" ,
        "ART" ,
        "WELL BEING"
    ],
    2: [
        "ENGLISH",
        "HINDI",
        "MATHEMATICS",
        "SCIENCE",
        "SOCIAL SCIENCE",
    ]
}

print("sum(periodsPerWeek.values()): ", sum(periodsPerWeek.values()))

# helper
# get dimenstions of multi dimensional containers (types: list, tuple, set, dict)
# assumes that the container[i] and container[j] are of the same size
def dimensions(obj):
    d = []
    j = obj
    while True:
        if type(j) in [list, tuple]:
            d.append(len(j))
            j = j[0]
        elif type(j) is set:
            d.append(len(j))
            j = next(iter(j))
        elif type(j) is dict:
            d.append(len(j))
            j = j[next(iter(j))]
        else:
            break
    return d 

#helper
# prints a 3 * 7 * 42 thing nicely
def printNicely(data):

    f  = open('dump.txt', "w+")

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
                    smallStr = ''
                    while counter < periodsPerDay[foo]:
                        smallStr += str(data[grade][section][row][counter]).center(15) + ", "
                        counter += 1
                    smallStr = smallStr.ljust(200)    
                    smallStr += " | "
                    myStr += smallStr
                myStr += "\n"
                foo += 1
                f.write(myStr)
            f.write("\n ---------------------------------------------------------- \n")

    f.close()


        
# helper
def createInitial(studentTimeTable, teacherTimeTable):
    global periodsPerWeek, subjectsByWeight

    #technically every 42 in this method should be replaced by sum(periodsPerDay)
    periodsPerDay = [
        9,
        9,
        9,
        9,
        6
    ]

    #assume every class is heavy; we will replace 15 of them with lights
    oneClass = []

    # for _ in range(3):
    #     oneGrade = []
    #     for _ in range(7):
    #         oneGrade.append([''] * 42)
    #     oneClass.append(oneGrade)

    # print("dimensions of the oneClass: ", dimensions(oneClass))



    #allocate the PT period
    '''
    PT is not in the first 3 periods or the last one
    which gives us 5*4 + 2 = 22 options and 21 classrooms 
    '''

    v1 = list(range(21))
    ptPeriods = []
    for i in range(21):
        p = choice(v1)
        day = p // 5
        period = p % 5 + 3
        print("grade: ", i//7+6, " | section: ", i%7, " | slot: ", [day, period])
        studentTimeTable[i//7][i%7][day][period] = 'PED'
        ptPeriods.append(p)
        v1.remove(p)

    # print("\n")
    # usedUpSlots.sort()
    # list(map(print, usedUpSlots))

    # printNicely(studentTimeTable)

    #allocate the rest of the periods as weights
    '''
    we have 25 heavies & 16 lights
    '''

    for grade in range(3):
        for section in range(7):
            
            oneClass = ['']*42
            oneClass[ptPeriods[grade*3 + section]] = 'PED'

            v1 = []
            for i in subjectsByWeight[1]:
                v1 += [i] * periodsPerWeek[i]
            for i in range(16): #since we have 16 lights
                p = choice(list(range(42)))
                while (oneClass[p] != ''): #dont want two 1's in the same period
                    p = (p+1) % 42
                oneClass[p] = v1[i]

            #now we will rewrite oneClass with the subject names

            # allocate the heavy subjects
            v1 = subjectsByWeight[2]*5 #each of the numbers 0 to 4 represents a heavy subject
            for i in range(25):
                p = choice(v1)
                oneClass[oneClass.index('')] = p
                v1.remove(p)

            #TODO figure out a way to push for about 1 of each heavy per day

            for i in range(42):
                studentTimeTable[grade][section][i // 9][i % 9] = oneClass[i]

    #TODO fill out the teacher's time table as well

    printNicely(studentTimeTable)


# helper
def resolveConflicts(studentTimeTable, teacherTimeTable):
    pass

def createClassTimeTable():
        
    global periodsPerWeek, subjectsByWeight

    # access: teacherSubject[teacherName][subjectName] = [className]
    teachersClasses, classsTeachers = classWiseTeacherAllocation()

    #access: timeTable[classIndex][dayIndex][periodIndex]
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

    teacherTimeTable = {
        i: [ [''] * 9, [''] * 9,  [''] * 9, [''] * 9, [''] * 6 ] for i in teachersClasses.keys() 
    }

    print("dimensions of the student time table: ", dimensions(studentTimeTable))
    print("dimensions of the teacher time table: ", dimensions(teacherTimeTable))

    # list(map(lambda x: print(x, ": ", teacherTimeTable[x]), teacherTimeTable.keys()))

    # return

    createInitial(studentTimeTable, teacherTimeTable)

    print("createInitial done")

    resolveConflicts(studentTimeTable, teacherTimeTable)


# classWiseTeacherAllocation()
createClassTimeTable()


