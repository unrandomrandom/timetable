from random import choice,shuffle,randint

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
    teacherTimeTable_[i] =  [ [[]] * 9, [[]] * 9,  [[]] * 9, [[]] * 9, [[]] * 6 ]

class teacherPeriod:
    def __init__ (self, subject, grade, section):
        self.subject = subject
        self.grade = grade
        self.section = section

class studentPeriod:
    def __init__ (self, subject, grade, section, day, period):
        global classSubjectTeachers_, teacherTimeTable_
        self.subject = subject
        self.grade = grade
        self.section = section
        self.day = day
        self.period = period
        self.teachers = {}
        gradeString = str(self.grade) + chr(self.section + ord('A'))
        if subject == 'I.ED/GK':
            self.teachers['I.ED'] = classSubjectTeachers_[gradeString]['I.ED']
            self.teachers['G.K'] = classSubjectTeachers_[gradeString]['G.K']
        elif subject == 'WELL BEING':
            self.teachers['WELL BEING'] = classSubjectTeachers_[gradeString]['W.E/Club']
        elif subject == 'CLUB':
            self.teachers['CLUB'] = classSubjectTeachers_[gradeString]['W.E/Club']
            self.teachers['ROBOTICS'] = classSubjectTeachers_[gradeString]['ROBOTICS']
            self.teachers['STEAM'] = classSubjectTeachers_[gradeString]['STEAM']
        else:
            self.teachers[subject] = classSubjectTeachers_[gradeString][subject]

        for tr in self.teachers:
            teacherTimeTable_[tr][self.day][self.period].append([self.grade, self.section, self.subject])

    def getClashes(self):
        for tr in self.teachers:
            if len(teacherTimeTable_[tr][self.day][self.period]) > 1:
                return True
        return False


'''
how the schdeule gets made

allocate ped for all grades
for each class, call initialArrange, 
    this sets each element of self.periods to a string representing the subject for that period
for each class, call setSchedule, 
    this converts each string in self.periods to a Class object
    NOTE: this does NOT set the teacher time table for each class though
for each class, call resolveConflicts
'''

class Class:
    def __init__(self, grade, section):
        global periodsPerDay_
        self.grade = grade
        self.section = section
        self.periods = [[''] * i for i in periodsPerDay_]

    '''
    To be called on each class after PED has been assigned
    assumes that PED is already assigned
    fills up self.periods to a string representing the subject
    '''
    def initialArrange(self):
        global totalPeriods_, periodsPerWeek_, subjectsByWeight_

        #allocate the light subjects
        v1 = []
        for i in subjectsByWeight_[1]:
            v1 += [i] * periodsPerWeek_[i]
        shuffle(v1)
        while len(v1) > 0: 
            p = randint(0, totalPeriods_ - 1)
            while (self.periods[p//9][p%9] != ''): #dont want two 1's in the same period
                p = (p+1) % totalPeriods_
            self.periods[p//9][p%9] = v1.pop()

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
                    self.periods[i][j] = v1.pop()

    '''
    To be called on each class after initialArrange
    for each subject string in self.periods: stirng -> studentPeriod object
    '''
    def setSchedule(self):
        for i, day in enumerate(self.periods):
            for j, period in enumerate(day):
                self.periods[i][j] = studentPeriod(
                    period,
                    self.grade,
                    self.section,
                    i,
                    j
                )

    '''
    HELPER

    the time table of a class wants to swaps periods @[i][j] and @[i_][j_]
    assumes the subjects  @[i][j] and @[i_][j_] are single teacher
    and that teacher@[i][j] is free @[i_][j_] and vice versa

    algorithm:
        find teacher@[i][j]
            remove the [grade,section, subject] from [i][j] 
            append [grade,section, subject] to [i_][j_] 
        find teacher@[i_][j_]
            remove the [grade,section, subject] from [i_][j_] 
            append [grade, section, subject] to [i][j] 
        swap the studentPeriod objects @[i][j] and @[i_][j_]
    '''
    def swap(self, i, j, i_, j_):
        global teacherTimeTable_
        p = self.periods[i][j]
        p_ = self.periods[i_][j_]
        # swap time table of the teacher @[i][j] (will teach the class [i_][j_] instead of [i][j])
        teacherTimeTable_[p.teachers[0]][i][j].remove([self.grade, self.section, p.subject])
        teacherTimeTable_[p.teachers[0]][i_][j_].append([self.grade, self.section, p.subject])
        # swap time table of the teacher @[i_][j_] (will teach the class [i][j] instead of [i_][j_])
        teacherTimeTable_[p_.teachers[0]][i_][j_].remove([self.grade, self.section, p_.subject])
        teacherTimeTable_[p_.teachers[0]][i][j].append([self.grade, self.section, p_.subject])
        # swap the actual class time table
        foo = self.periods[i][j]
        self.periods[i][j] = self.periods[i_][j_]
        self.periods[i_][j_] = foo


    '''
    HELPER

    assumes that the teacher for this subject is just one
    tries to move the subject @[day][period] to another period in the week
    
    algorithm:
        find all the free periods of the teacher teaching @[day][period]
        for each free period, say [i][j], 
            if the subject has multiple teachers, continue
            if the teacher teaching at [i][j] is free at [day][period], 
                swap [i][j] and [day][period]
                return True
        return False
    '''
    def moveToAnotherPeriod(self, day, period):
        p = self.periods[day][period]
        teacher = p.teachers[0]
        # all the periods at which teacher[day][period] is free
        freePeriods = []
        for i, d in enumerate(teacherTimeTable_[teacher]):
            for j, p in enumerate(d):
                if len(p) == 0:
                    freePeriods.append([i, j])
        for i, j in freePeriods:
            p2 = self.periods[i][j]
            teacher2 = p2.teachers[0]
            if len(p2.teachers) > 1:
                continue
            # teacher @[i][j] is free @[day][period]
            # remember, teacher@[day][period] is free @[i][j]
            if len(teacherTimeTable_[teacher2][day][period]) == 0:
                self.swap(i, j, day, period)
                return True
        return False

    '''
    to be called on each class after setSchedule
    '''
    def resolveConflicts(self):
        global teacherTimeTable_
        for i, day in enumerate(self.periods):
            for j, p in enumerate(day):
                # if the subject has > 1 teacher, dont bother with conflict resolution; too messy
                if len(p.teachers) > 1:
                    continue 
                teacher = p.teachers[0]
                # if the teacher is only teaching one class at [day][period], it has to be this one so we are good
                if len(teacherTimeTable_[teacher][p.day][p.period]) == 1:
                    continue
                # if flow reaches here, that means the teacher @[][] is teaching > 1 class,
                # so we try to move the subject taught @[][] for 'this' class to another class
                if self.moveToAnotherPeriod(p.day, p.period) is False:
                    print("error on ", [self.grade, self.section, i, j, p.subject])

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
    
    def resolveConflicts(self):
        for i, c in enumerate(self.classes):
            c.resolveConflicts()
                
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

    for g in grades:
        g.resolveConflicts()

    print("checking the final allotment of grades of each class ")
    checkPeriodCounts(grades, periodsPerWeek_, teacherTimeTable_)

    # TODO restructure the dump functions for new structure of grades 
    dumpStudentAllocation(grades)
    dumpTeacherAllocation(teacherTimeTable_)

runner()