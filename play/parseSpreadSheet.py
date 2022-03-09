from os import getcwd, chdir, name
from openpyxl import Workbook, load_workbook
from json import dumps

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


def changePathDecorator(func):
    def runner():
        ogDir = getcwd()
        chdir('..')
        if name == 'nt':        # windows
            chdir(getcwd() + "\\data")
        else:
            chdir(getcwd() + "/data")
        teacherSubject, classSubjectTeacher = func()
        chdir(ogDir)
        return teacherSubject, classSubjectTeacher
    return runner

@changePathDecorator
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

def runner():
    print("cwd: ", getcwd())
    a, b = classWiseTeacherAllocation()
    print("cwd: ", getcwd())
    print(a)
    print(b)

if __name__ == "__main__":
    runner()