allTeachers = {}

def checkTeacherAllotment(classSubjectTeachers: dict, periodsPerWeek: dict):
    global allTeachers
    allTeachers = {}
    for c in classSubjectTeachers.values():
        for sub, tr in c.items():
            if tr not in allTeachers.keys():
                allTeachers[tr] = 0
            if sub == 'I.ED' or sub == 'G.K':
                sub = 'I.ED/GK'
            elif sub == 'W.E/Club':
                sub = 'CLUB'
            elif sub not in periodsPerWeek.keys():
                continue
            if sub != 'PED':
                allTeachers[tr] += periodsPerWeek[sub]
            else:
                allTeachers[tr] += 1
    for tr, total in allTeachers.items():
        if total > 42:
            print("teacher ", tr, " has > 42 periods alloted per week")

def checkPeriodCounts(grades, periodsPerWeek: dict, teacherTimeTable: dict):
    global allTeachers
    for g_, g in enumerate(grades):
        for c_, c in enumerate(g.classes):
            ct = 0
            subjectCount = {i: 0 for i in periodsPerWeek.keys()}
            for d in c.periods:
                for p in d:
                    if p != '':
                        if p == 'PED':
                            ct += 1
                        else:
                            subjectCount[p] += 1
                            ct += 1
            if ct != 42:
                print("number of periods for ", str([g_, c_]), " is not 42")
            for k in subjectCount.keys():
                if subjectCount[k] != periodsPerWeek[k]:
                    print("number of ", k, "periord for ", str([g_, c_]), " is",
                    subjectCount[k], " instead of ", periodsPerWeek[k])

    for tr, t in teacherTimeTable.items():
        ct = 0
        for i, d in enumerate(t):
            for j, c in enumerate(d):
                if c != '':
                    ct += 1
        if ct != allTeachers[tr]:
            print("teacher ",tr, " was alloted ", allTeachers[tr], " periods but got ", ct, " periods.")
