
from random import choice

from numpy import empty
from parseSpreadSheet import classWiseTeacherAllocation
from printFuncs import dumpStudentAllocation, dumpTeacherAllocation

# --------------GLOBAL VARIABLES----------------------

periodsPerWeek_ = {
    "ENG": 5,
    "HIND": 5,
    "MATHS": 5,
    "SCIENCE": 5,
    "S.ST": 5,
    "ARAB": 4,
    "USST": 2,
    "I.ED/GK": 2,
    "CSC": 3,
    "LIB": 1,
    "CLUB": 1,
    "MUSIC": 1,
    "ART": 1,
    "WELL BEING": 1
}

subjectsByWeight_ = {
    1: [
        # "I.ED/GK",
        "ARAB",
        "USST",
        "CSC",
        "LIB" ,
        "CLUB" ,
        "MUSIC" ,
        "ART" ,
        "WELL BEING"
    ],
    2: [
        "ENG",
        "HIND",
        "MATHS",
        "SCIENCE",
        "S.ST",
    ]
}

periodsPerDay_ = [
    9,
    9,
    9,
    9,
    6
]

# will be filled with 3 Grade objects
grades = []

# --------------END OF GLOBAL VARIABLES-----------------


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

teachersClasses, classSubjectTeachers = classWiseTeacherAllocation()

teacherTimeTable = {}
for i in teachersClasses.keys():
    teacherTimeTable[i] =  [ [''] * 9, [''] * 9,  [''] * 9, [''] * 9, [''] * 6 ]

subjects_ = []
for i in periodsPerWeek_:
    subjects_ += [i] * periodsPerWeek_[i]

# ----------------------END OF GLOBALS --------------------------------


'''
check for existing occupancy in teacher timetable,
if there is a clash:
    return false
else:
    return true
'''
def subjectTeacherSlotIsEmpty(grade, section, dayNo, periodNo, subjectName):
    global classSubjectTeachers, teacherTimeTable
    gradeNo = int(grade)
    sectionNo = int(section) - ord("A")
    className = grade + section

    if subjectName == 'I.ED/GK':
        tr1 = classSubjectTeachers[className]['I.ED']
        tr2 = classSubjectTeachers[className]['G.K']
        if teacherTimeTable[tr1][dayNo][periodNo] != '':
            return False
        if teacherTimeTable[tr2][dayNo][periodNo] !='':
            return False
        return True
    elif subjectName == 'CLUB' or subjectName == 'WELL BEING':
        teacherName = classSubjectTeachers[className]["W.E/Club"]
        if teacherTimeTable[teacherName][dayNo][periodNo] != '':
            return False
        return True
    else:
        teacherName = classSubjectTeachers[className][oneClass[i]]
        if teacherTimeTable[teacherName][dayNo][periodNo] != '':
            return False
        return True

'''
assigns a teacher to a given period; assumes that the slot is empty 
at that period
'''
def setSubjectTeacherSlot(grade, section, dayNo, periodNo, subjectName):
    global classSubjectTeachers, teacherTimeTable
    gradeNo = int(grade)
    sectionNo = ord(section) - ord("A")
    className = grade + section
    
    if subjectName == 'I.ED/GK':
        tr1 = classSubjectTeachers[className]['I.ED']
        tr2 = classSubjectTeachers[className]['G.K']
        teacherTimeTable[tr1][dayNo][periodNo] = className
        teacherTimeTable[tr2][dayNo][periodNo] = className
    elif subjectName == 'CLUB' or subjectName == 'WELL BEING':
        teacherName = classSubjectTeachers[className]["W.E/Club"]
        teacherTimeTable[teacherName][dayNo][periodNo] = className
    else:
        teacherName = classSubjectTeachers[className][subjectName]
        teacherTimeTable[teacherName][dayNo][periodNo] = className

    studentTimeTable[gradeNo - 6][sectionNo][dayNo][periodNo] = subjectName

# returns the empty slots of a given class if the period[i][j] is empty
def getSwapSlots(grade, section, i, j):
    global grades, classSubjectTeachers, teacherTimeTable
    gNo= ord(grade) - ord('6')
    sNo = ord(section) - ord('A')
    emptySlots = []
    if grades[gNo].classes[sNo].periods[i][j] == '':
        subjectToSwap = grades[gNo].classes[sNo].periods[i][j]
        emptySlots = grades[gNo].classes[sNo].overlappingFreeSlots(subjectToSwap)
        emptySlots.remove([i, j])
    return emptySlots

def reBalance(grade, section, subjectName, i, j, flexible = False):
    global grades, classSubjectTeachers, teacherTimeTable
    print("rebalance called on " + str([grade, section, subjectName, i, j, flexible]))
    className = grade + section
    if subjectName == 'I.ED/GK':
        tr1 = classSubjectTeachers[className]['I.ED']
        tr2 = classSubjectTeachers[className]['G.K']
        classes1 = teachersClasses[tr1][subjectName]
        classes2 = teachersClasses[tr2][subjectName]
        for c1 in classes1:
            for c2 in classes2:
                g1 = c[0]    # grade
                s1 = c[1]    # section
                gNo1 = ord(g1) - ord('6')
                sNo1 = ord(s1) - ord('A')
                g2 = c[0]    # grade
                s2 = c[1]    # section
                gNo2 = ord(g2) - ord('6')
                sNo2 = ord(s2) - ord('A')
                swapSlots1 = getSwapSlots(g1, s1, i, j)
                swapSlots2 = getSwapSlots(g2, s2, i, j)
                if len(swapSlots1) == 0 and len(swapSlots2) == 0:
                    commonSlots = [i for i in swapSlots1 if i in swapSlots2]
                    if len(commonSlots) != 0:
                        i_, j_ = commonSlots[0]
                        subjectToSwap = grades[gNo].classes[sNo].periods[i][j]
                        grades[gNo].classes[sNo].periods[i_][j_] = subjectToSwap
                        grades[gNo].classes[sNo].periods[i][j] = ''
                        teacherTimeTable[teacherName][i_][j_] = c
                        teacherTimeTable[teacherName][i][j] = subjectName
                        grades[gNo].classes[sNo].periods[i][j] = subjectName
                        print("swapped successfully")
                        return


    else:
        teacherName = ''
        if subjectName == 'CLUB' or subjectName == 'WELL BEING':
            teacherName = classSubjectTeachers[className]["W.E/Club"]
        else:
            teacherName = classSubjectTeachers[className][subjectName]
        classes= teachersClasses[teacherName][subjectName]
        classes.remove(grade + section)
        for c in classes:
            g = c[0]    # grade
            s = c[1]    # section
            gNo= ord(g) - ord('6')
            sNo = ord(s) - ord('A')
            swapSlots = getSwapSlots(g, s, i, j)
            if len(swapSlots) != 0:
                i_, j_ = swapSlots[0]
                subjectToSwap = grades[gNo].classes[sNo].periods[i][j]
                grades[gNo].classes[sNo].periods[i_][j_] = subjectToSwap
                grades[gNo].classes[sNo].periods[i][j] = ''
                teacherTimeTable[teacherName][i_][j_] = c
                teacherTimeTable[teacherName][i][j] = subjectName
                grades[gNo].classes[sNo].periods[i][j] = subjectName
                print("swapped successfully")
                return
        print("swap was not successful")
        return


class Class():
    def __init__(self, grade: str, section: str):
        self.grade = grade
        self.section = section
        self.oneClass = []
        self.allocateClasses()

    def allocateClasses(self):
        global subjects_

        # empty slots
        self.periods = [[]] * 5
        for i, p in enumerate(periodsPerDay_):
            self.periods[i] = [''] * p

    def assignInitial(self):
        global subjectsByWeight_, periodsPerWeek_
        self.oneClass = ['']*42
        oneClassByWeight = [0] * 42
        v1 = []
        for i in subjectsByWeight_[1]:
            v1 += [i] * periodsPerWeek_[i]
        for i in range(14): #since we have 16 lights - 2 lights(IED/GK; assigned in runner)
            p = choice(list(range(42)))
            while (self.oneClass[p] != ''): #dont want two 1's in the same period
                p = (p+1) % 42
            self.oneClass[p] = v1[i]
            oneClassByWeight[p] = 1

        # allocate the heavy subjects
        v1 = subjectsByWeight_[2]*5 #each of the numbers 0 to 4 represents a heavy subject
        for i in range(25):
            p = choice(v1)
            ind = self.oneClass.index('')
            self.oneClass[ind] = p
            oneClassByWeight[ind] = 2
            v1.remove(p)

    def assignTheRest(self):
        initialSubjects = ['I.ED/GK', ]
        initialIndices = [[subject, i] for i, subject in enumerate(self.oneClass) if subject in initialSubjects]

            
        for i, subject in enumerate(self.oneClass):
            if subject == '':
                continue
            self.setPeriod(
                i//9,
                i%9,
                subject
            ) 

    '''
    returns the indices of the overlap of the free slots of 
    a given subject teachers time table and the class' time table
    '''
    def overlappingFreeSlots(self, subjectName):
        slots = [  ]
        global classSubjectTeachers, teacherTimeTable
        className = self.grade + self.section
        if subjectName == 'I.ED/GK':
            tr1 = classSubjectTeachers[className]['I.ED']
            tr2 = classSubjectTeachers[className]['G.K']
            tr1Schedule = teacherTimeTable[tr1]
            tr2Schedule = teacherTimeTable[tr2]
            for i, dayLength in enumerate(periodsPerDay_):
                for j in range(dayLength):
                    if tr1Schedule[i][j] == '':
                        slots.append([i, j])
            slots = [[i, j] for i, j in slots if tr2Schedule[i][j] == '']
        else:
            teacherName = ''
            if subjectName == 'CLUB' or subjectName == 'WELL BEING':
                teacherName = classSubjectTeachers[className]["W.E/Club"]
            else:
                teacherName = classSubjectTeachers[className][subjectName]
            trSchedule = teacherTimeTable[teacherName]
            for i, dayLength in enumerate(periodsPerDay_):
                for j in range(dayLength):
                    if trSchedule[i][j] == '':
                        slots.append([i, j])
        slots = [[i, j] for i, j in slots if self.periods[i][j] == '']
        return slots

    def setPeriod(self, i, j, subjectName, flexible = True):
        emptySlots = self.overlappingFreeSlots(subjectName)
        if len(emptySlots) == 0:
            # print(
                # "the teacher: ", classSubjectTeachers[self.grade+self.section][subjectName] ,
                # "cannot teach class: ", subjectName
            # )
            print("subject: ", subjectName, " cannot be printed for class: ", self.grade + self.section)
            # reBalance(self.grade, self.section, subjectName, i, j, flexible)
            return
            # exit(0)
        if not flexible:
            if [i, j] in emptySlots:
                setSubjectTeacherSlot(
                    self.grade, 
                    self.section, 
                    i, 
                    j, 
                    subjectName
                )
                self.periods[i][j] = subjectName
            else:
                print("cannot fix ",[i, j], " for subject ", subjectName,
                "for class ", [self.grade, self.section])
                # reBalance(self.grade, self.section, subjectName, i, j, False)
                return
        else:
            setSubjectTeacherSlot(
                self.grade, 
                self.section, 
                emptySlots[0][0], 
                emptySlots[0][1], 
                subjectName
            )
            self.periods[emptySlots[0][0]][emptySlots[0][1]] = subjectName

    
class Grade():
    def __init__(self, grade: str):
        self.grade = grade
        self.classes = []
        for i in range(7):
            self.classes.append(Class(self.grade, chr(ord('A')+i)))

    def assignSchedule(self):
        for c in self.classes:
            c.assignInitial()



def runner():
    global grades
    grades = [
        Grade('6'),
        Grade('7'),
        Grade('8')
    ]

    # since we need to ensure 0 overlaps over the grades for PT, we assign them first
    v1 = list(range(21))
    for i in range(21):
        p = choice(v1)
        grades[p//7].classes[p%7].oneClass = 'PED'
        v1.remove(p)

    

    v1 = list(range(42))
    for i in range(42):
        p = choice(v1)
        day = p // 10
        period = p % 8 + 1
        neww = p
        while (grades[i//14].classes[i%7].periods[day][period] != ''):
            neww = (neww + 1) % 42
            day = neww // 10
            period = neww % 8 + 1
            i = neww
        grades[i//14].classes[i%7].setPeriod(
            day,
            period,
            "I.ED/GK",
            False
        )
        v1.remove(p)


    # assigning the rest of the grades
    for g in grades:
        g.assignSchedule()

    dumpStudentAllocation(grades)
    dumpTeacherAllocation(teacherTimeTable)

    for i in range(5):
        print(str(grades[0].classes[0].periods[i]))
    
runner()


