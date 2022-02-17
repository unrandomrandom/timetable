from openpyxl import Workbook, load_workbook
from os import getcwd, chdir
from pprint import pprint
from json import dumps
from random import choice



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
    "PED": 1,
    "MUSIC": 1,
    "ART": 1,
    "LIBRARY": 1,
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
        "PED" ,
        "MUSIC" ,
        "ART" ,
        "LIBRARY" ,
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
    oneClass = [
        [
            [
                [2]*42
            ] * 7
        ] * 3
    ] 

    #allocate the PT period
    '''
    PT is not in the first 3 periods or the last one
    which gives us 5*4 + 2 = 22 options and 21 classrooms 
    '''

    v1 = list(range(21))
    for i in range(21):
        p = choice(v1)
        day = p // 5
        period = p % 5
        studentTimeTable[i//3][i%7][day][period] = 'PED'
        oneClass[i//3][i%7][p] = 'PED'
        v1.remove(p)

    #allocate the rest of the periods as weights
    '''
    we have 25 heavies & 16 lights
    '''

    for grade in range(3):
        for section in range(7):

            for i in range(16): #since we have 16 lights
                p = choice(42)
                while (oneClass[grade][section][p] != 1): #dont want two 1's in the same period
                    p = (p+1) % 42
                oneClass[grade][section][p] = 1

            #now we will rewrite oneClass with the subject names

            # allocate the heavy subjects
            v1 = subjectsByWeight[2]*5 #each of the numbers 0 to 4 represents a heavy subject
            for i in range(25):
                p = choice(v1)
                oneClass[grade][section][oneClass.index(2)] = p
                v1.remove(p)

            #TODO figure out a way to push for about 1 of each heavy per day
            
            #allocate the lightweights away
            v1 = []
            for i in subjectsByWeight[2]:
                v1 += [i] * periodsPerWeek[i]
            for i in range(25):
                p = choice(v1)
                oneClass[grade][section][oneClass.index(1)] = p
                v1.remove(p)

        for i in range(42):
            studentTimeTable[grade][section][i // 9][i % 9] = v1[i]

    #TODO fill out the teacher's time table as well

# helper
def resolveConflicts(studentTimeTable, teacherTimeTable):
    pass

def createClassTimeTable():
        
    global periodsPerWeek, subjectsByWeight

    # access: teacherSubject[teacherName][subjectName] = [className]
    teachersClasses, classsTeachers = classWiseTeacherAllocation()

    #access: timeTable[classIndex][dayIndex][periodIndex]
    studentTimeTable = [
        [
            [
                [[''] * 9],     # monday
                [[''] * 9],     # tuesday 
                [[''] * 9],     # wednesday
                [[''] * 9],     # thursday
                [[''] * 6],     # friday
            ] * 7               # 7 sections in a grade
        ] * 3                   #grades 6, 7, 8
    ]

    teacherTimeTable = {
        i: [ [[''] * 9], [[''] * 9],  [[''] * 9], [[''] * 9], [[''] * 6] ] for i in teachersClasses.keys() 
    }

    createInitial(studentTimeTable, teacherTimeTable)

    resolveConflicts(studentTimeTable, teacherTimeTable)


# classWiseTeacherAllocation()
createClassTimeTable()


