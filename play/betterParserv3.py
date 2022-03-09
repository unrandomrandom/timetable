
from random import choice,shuffle

from parseSpreadSheet import classWiseTeacherAllocation
from printFuncs import dumpStudentAllocation, dumpTeacherAllocation
from tests import checkPeriodCounts, checkTeacherAllotment, checkPeriodCounts

# ----------------------- START OF GLOBALS -----------------------

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
        "I.ED/GK",
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

totalPeriods_ = sum(periodsPerDay_)

teachersClasses_, classSubjectTeachers_ = classWiseTeacherAllocation()

studentTimeTable = {}
for i, grades in enumerate(range(3)):
    oneGrade = {}
    for j, divisions in enumerate(range(7)):
        oneClass = [
            [''] * 9,     # monday
            [''] * 9,     # tuesday 
            [''] * 9,     # wednesday
            [''] * 9,     # thursday
            [''] * 6,     # friday
        ]
        oneGrade[j] = oneClass
    studentTimeTable[i] = oneGrade

teacherTimeTable_ = {}
for i in teachersClasses_.keys():
    teacherTimeTable_[i] =  [ [''] * 9, [''] * 9,  [''] * 9, [''] * 9, [''] * 6 ]

subjects_ = []
for i in periodsPerWeek_:
    subjects_ += [i] * periodsPerWeek_[i]

# ----------------------- END OF GLOBALS -------------------------

'''
the periods array will be initially filled with the initial arrangement
then, for each period in the array, setSubject will be called
'''

class Class():
    def __init__(self, grade, section) -> None:
        self.grade = grade
        self.section = section
        self.periods = [[''] * i for i in periodsPerDay_]
        self.teacherBySubject = classSubjectTeachers_[str(self.grade) + chr(self.section + ord('A'))]
        self.alreadySet = []

    def setSubject(self, day, period, subject):
        global teacherTimeTable_
        teachers = self.getSubjectTeachers(subject)
        og = self.periods[day][period]
        attemptCalled = False
        if subject == 'I.ED/GK':
            tr1 = teachers[0]
            tr2 = teachers[1]
            if teacherTimeTable_[tr1][day][period] != '' or teacherTimeTable_[tr2][day][period] != '':
                # print("calling changeToFree on ", subject, " for ", str([self.grade, self.section]))
                attempt = self.changeToFree(day, period, subject)
                attemptCalled = True
                if attempt is False:
                    print("could not set ", subject, " for ", str([self.grade, self.section]))
            else:
                teacherTimeTable_[tr1][day][period] = 'I.ED'
                teacherTimeTable_[tr2][day][period] = 'GK'
        else:
            teacher = teachers[0]
            # see if the teacher is busy, if busy, change period to a free period
            if teacherTimeTable_[teacher][day][period] != '':
                attempt = self.changeToFree(day, period, subject)
                attemptCalled = True
                if attempt is False:
                    print("could not set ", subject, " for ", str([self.grade, self.section]))
            else:
                teacherTimeTable_[teacher][day][period] = subject
        if og != self.periods[day][period] and attemptCalled is False:
            print(str([self.grade, self.section]), " changed while running setsubject @", str([day, period, subject]))

    # get a list of teachers teaching a subject
    def getSubjectTeachers(self, subject):
        teachers = []
        if subject == 'I.ED/GK':
            teachers.append(self.teacherBySubject['I.ED'])
            teachers.append(self.teacherBySubject['G.K'])
        else:
            if subject == 'CLUB' or subject == 'WELL BEING':
                teachers.append(self.teacherBySubject["W.E/Club"])
            else:
                teachers.append(self.teacherBySubject[subject])
        return teachers

    def changeToFree(self, day, period, subject):
        global teacherTimeTable_
        '''
        get the empty slots of the subject teacher
        for each empty slot
            see who is teaching (other teacher) that slot for this grade
            if other teacher is also free at [day,period]
                update the timetable of other teacher (empty out @empty slot and fill up @day,period)
                swap the periods in self.periods (@empty slot and @[day, period]) so now the subject teacher is supposed to teach@(empty slot)
                fill up the time table of the subject teacher @(empty slot)
                return true
        return false
        '''
        teachers = self.getSubjectTeachers(subject)

        if subject == 'I.ED/GK':
            teacher1 = teachers[0]
            teacher2 = teachers[1]
            freePeriods1 = []
            for i, d in enumerate(teacherTimeTable_[teacher1]):
                for j, p in enumerate(d):
                    if p == '':
                        freePeriods1.append([i, j])
            freePeriods2 = []
            for i, d in enumerate(teacherTimeTable_[teacher2]):
                for j, p in enumerate(d):
                    if p == '':
                        freePeriods2.append([i, j])
            # the common free periods
            freePeriods = [i for i in freePeriods1 if i in freePeriods2]
            for i, j in freePeriods:
                if self.periods[i][j] == 'I.ED/GK':
                    continue
                tr = self.getSubjectTeachers(self.periods[i][j])[0]
                if teacherTimeTable_[tr][day][period] == '':
                    # update the time table of the teacher that is free @day, period (empty @i,j) & fill @(day, period)
                    teacherTimeTable_[tr][day][period] = teacherTimeTable_[tr][i][j]
                    teacherTimeTable_[tr][i][j] = ''
                    # the original teacher now teaches @(free slot ie. i,j)
                    # we dont disturb [tr1][day][period] since the tr is teaching some other class then 
                    teacherTimeTable_[teacher1][i][j] = 'I.ED'
                    teacherTimeTable_[teacher2][i][j] = 'G.K'
                    # update the time table
                    sub = self.periods[i][j]
                    self.periods[day][period] = sub
                    self.periods[i][j] = subject
                    self.alreadySet.append([day, period])
                    self.alreadySet.append([i, j])
                    return True
            return False

        else:
            teacher = teachers[0]
            # get the free periods of the teacher teaching "subject"
            freePeriods = []
            for i, d in enumerate(teacherTimeTable_[teacher]):
                for j, p in enumerate(d):
                    if p == '':
                        freePeriods.append([i, j])
            
            for i, j in freePeriods:
                if self.periods[i][j] == 'I.ED/GK':
                    continue
                tr = self.getSubjectTeachers(self.periods[i][j])[0]
                if teacherTimeTable_[tr][day][period] == '':
                    # update the time table of the teacher that is free @day, period (empty @i,j) & fill @(day, period)
                    teacherTimeTable_[tr][day][period] = teacherTimeTable_[tr][i][j]
                    teacherTimeTable_[tr][i][j] = ''
                    # the original teacher now teaches @(free slot ie. i,j)
                    teacherTimeTable_[teacher][i][j] = subject
                    # update the time table
                    sub = self.periods[i][j]
                    self.periods[day][period] = sub
                    self.periods[i][j] = subject
                    return True
            return False

    # assumes that PED(PT) is already assigned
    def initialArrange(self):
        global totalPeriods_, periodsPerWeek_, subjectsByWeight_
        lightPeriods = sum([periodsPerWeek_[i] for i in subjectsByWeight_[1]])
        heavyPeriods = sum([periodsPerWeek_[i] for i in subjectsByWeight_[2]])
        v1 = []
        for i in subjectsByWeight_[1]:
            v1 += [i] * periodsPerWeek_[i]
        shuffle(v1)
        pds = list(range(totalPeriods_))
        for i in range(lightPeriods): 
            p = choice(pds)
            pds.remove(p)
            while (self.periods[p//9][p%9] != ''): #dont want two 1's in the same period
                p = (p+1) % totalPeriods_
            self.periods[p//9][p%9] = v1[i]

        # allocate the heavy subjects
        v1 = []
        for i in subjectsByWeight_[2]:
            v1 += [i] * periodsPerWeek_[i]
        shuffle(v1)
        # since the rest of the subjects by weight have taken their place, 
        # the empty ones have to be where these subjects (the heavy ones) go
        for i, day in enumerate(self.periods):
            for j, period in enumerate(day):
                if period == '':    #is guaranteed to be found for every heavy subject
                    p = choice(v1)
                    self.periods[i][j] = p
                    v1.remove(p)
    
    def setSchedule(self):
        # ct = 0
        # for day in self.periods:
        #     for period in day:
        #         if period != '':
        #             ct += 1
        # print(str([self.grade, self.section]), ": ", ct)
        # self.copy = self.periods[:]

        for i, day in enumerate(self.periods):
            for j, period in enumerate(day):
                if [i, j] in self.alreadySet:
                    continue
                self.setSubject(i, j, period)



class Grade():
    def __init__(self, grade: str):
        self.grade = grade
        self.classes = []
        for i in range(7):
            self.classes.append(Class(self.grade, i))

    def initialArrange(self):
        for c in self.classes:
            c.initialArrange()

    def setSchedule(self):
        for i, c in enumerate(self.classes):
            c.setSchedule()

def runner():
    global teacherTimeTable_, classSubjectTeachers_, periodsPerWeek_
    grades = [
        Grade(6),
        Grade(7),
        Grade(8),
    ]

    v1 = list(range(21))
    for i in range(21):
        p = choice(v1)
        day = p // 5
        period = p % 5 + 3
        grades[i//7].classes[i%7].periods[day][period] = 'PED'
        v1.remove(p)

    print("checking the initial allotment counts of the teachers")
    checkTeacherAllotment(classSubjectTeachers_, periodsPerWeek_)
    
    for g in grades:
        g.initialArrange()

    dumpStudentAllocation(grades)

    for g in grades:
        g.setSchedule()

    print("checking the final allotment of grades of each class ")
    checkPeriodCounts(grades, periodsPerWeek_, teacherTimeTable_)

    dumpStudentAllocation(grades)
    dumpTeacherAllocation(teacherTimeTable_)

runner()


'''
past problems while designing
having to manually rearrage the teacher time table while the swap happened in the student time table
cant fucking rebalance easily
'''

'''
steps to rebalance:
description: we are given an i, j (initial arrangement), and a teacherName A, subjectName X who would like to teach at that given period
solution:
find an empty slot (p,q) for that teacher's time table and say teacher B, subjectName Y who teaches that subject
if B is free @i,j then,
stTimeTable[i][j] = Y
stTimeTable[p][q] = X
trTimeTable[i][j] = B
trTimeTable[p][q] = A
'''

'''
how to assign classes? and possibly minimize conflict

1. allocate grade wise (pt), then classwise constraint(pt teacher first), 
    then assign subjects by decreasing business of the teacher
2. 
'''