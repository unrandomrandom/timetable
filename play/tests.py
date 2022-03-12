from sre_constants import SUCCESS


teacherSubCounts = {}
teacherSubs = {}

def checkTeacherAllotment(classSubjectTeachers: dict, periodsPerWeek: dict):
    global teacherSubCounts, teacherSubs
    totalCases = 0
    failures = 0
    teacherSubCounts = {}
    teacherSubs = {}
    for c in classSubjectTeachers.values():
        for sub, tr in c.items():
            if tr not in teacherSubCounts.keys():
                teacherSubCounts[tr] = 0
                teacherSubs[tr] = []
            if sub == 'PED':
                teacherSubCounts[tr] += 1
                teacherSubs[tr] += ['PED'] * 1
            else:
                if sub == 'W.E/Club': # the teacher alloted for this teaches both WELL BEING and CLUB?
                    teacherSubCounts[tr] += periodsPerWeek['WELL BEING']    
                    teacherSubCounts[tr] += periodsPerWeek['CLUB']
                    teacherSubs[tr] += ['W.E/Club'] * periodsPerWeek['WELL BEING']    
                    teacherSubs[tr] += ['W.E/Club'] * periodsPerWeek['CLUB']    
                elif sub in ['ROBOTICS', 'STEAM']: #these subjects arent in periodsPerWeek
                    teacherSubCounts[tr] += periodsPerWeek['CLUB']
                    teacherSubs[tr] += [sub] * periodsPerWeek['CLUB']
                elif sub in ['I.ED', 'G.K']:
                    teacherSubCounts[tr] += periodsPerWeek['I.ED/GK']
                    teacherSubs[tr] += [sub] * periodsPerWeek['I.ED/GK']
                else:
                    if sub not in periodsPerWeek.keys():
                        continue
                    teacherSubCounts[tr] += periodsPerWeek[sub]
                    teacherSubs[tr] += [sub] * periodsPerWeek[sub]
    for tr, total in teacherSubCounts.items():
        totalCases += 1
        if total > 42:
            failures += 1
            print("teacher ", tr, " has > 42 periods alloted per week")
    print(totalCases - failures, " out of ", totalCases,
    " teachers were allocated more than 42 peiods per week")

def checkPeriodCounts(grades, periodsPerWeek: dict, classSubjectTeachers: dict, getSubject):
    global teacherSubCounts, teacherSubs
    for g_, g in enumerate(grades):
        for c_, c in enumerate(g.classes):
            ct = 0
            subjectCount = {i: 0 for i in periodsPerWeek.keys()}
            for d in c.periods:
                for p in d:
                    if getSubject(p) != '':
                        if getSubject(p) == 'PED':
                            ct += 1
                        else:
                            subjectCount[getSubject(p)] += 1
                            ct += 1
            if ct != 42:
                print("number of periods for ", str([g_, c_]), " is not 42")
            for k in subjectCount.keys():
                if subjectCount[k] != periodsPerWeek[k]:
                    print("number of ", k, "periord for ", str([g_, c_]), " is",
                    subjectCount[k], " instead of ", periodsPerWeek[k])

    counts2 = {i:0 for i in teacherSubCounts.keys()}

    secondSubjectCounts = {i: [] for i in teacherSubCounts.keys()}
    for g_, g in enumerate(grades):
        for c_, c in enumerate(g.classes):
            for d in c.periods:
                for p in d:
                    for tr in p.teachers:
                        counts2[tr] += 1
                        if p.subject != 'CLUB':
                            secondSubjectCounts[tr].append(p.subject)
                        else:
                            #a CLUB in student time table corresponds to these keys in the classSubject dict
                            subs = ['W.E/Club', 'STEAM', 'ROBOTICS'] 
                            gradeString = str(g_ + 6) + chr(c_ + ord('A'))
                            for sub in subs:
                                secondSubjectCounts[classSubjectTeachers[gradeString][sub]].append(sub)


    totalCases = 0
    succcesses = 0
    for tr, ct in counts2.items():
        totalCases += 1
        if ct == teacherSubCounts[tr]:
            succcesses += 1
            continue
        if len(teacherSubs[tr]) > len(secondSubjectCounts[tr]):
            diff = teacherSubs[tr][:]
            list(map(lambda x: diff.remove(x), secondSubjectCounts[tr]))
        else:
            diff = secondSubjectCounts[tr][:]
            list(map(lambda x: diff.remove(x), teacherSubs[tr]))
        print("\n teacher ",tr, " was alloted ", teacherSubCounts[tr], " periods but got ", ct, " periods.")
        print("difference: ", diff)

    print(succcesses, " out of ", totalCases,
     " teachers were allocated correct number of periods by subject ")


# for tr, t in teacherTimeTable.items():
#     ct = 0
#     for i, d in enumerate(t):
#         for j, c in enumerate(d):
#             if c != '':
#                 ct += len(c)
#     if ct != teacherSubCounts[tr]:
#         print("teacher ",tr, " was alloted ", teacherSubCounts[tr], " periods but got ", ct, " periods.")
