"""
making functions and classes efficient
python 3 implementation
vatsamail @ github
vatsamail@gmail.com
"""


'''
functions
'''


priority = {2, 3, 4}
numbers = [6,5,3,2,8,4]

def helper(x):
  if x in priority:
    return (0, x)
  return (1, x) # tuple comparison as 0 is less than 1

numbers.sort(key=helper)
print(numbers)



def write():
  a = 20
  b = 30
  def new_write():
    a = 10
    nonlocal b
    b = 33
    print(a)
    print(b)
  new_write()
  print(a)
  print(b)
write()

# amazing class
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(priority)
numbers.sort(key=sorter)
print("Class found", sorter.found)
print(numbers)


# accepting the functions over classes
names = ['abcd', 'abcde', 'abc']
names.sort(key=lambda x: len(x))
print(names)


from collections import defaultdict

d = defaultdict(int)
print(d['foo'])
d = defaultdict(lambda: 100)
print(d['foo'])
d = defaultdict(lambda: 100)
d['foo'] = 55
print(d['foo'])
def default_missing():
    print("Key added")
    return 0

d = defaultdict(default_missing)
d['foo'] = 55
print(d['bar'])
for a in d.items():
    print(a)


def increment_with_report(current, increments):
    added_count = 0
    def missing():
        nonlocal added_count
        added_count +=1
        return 0
    result = defaultdict(missing, current)
    for key, offset in increments:
        result[key] += offset

    return result, added_count

current = {'green': 12, 'blue': 3}
increments = [('red', 5), ('blue', 8)]
print(increment_with_report(current, increments))


def write(str, *opt):
    print("Writing what you said", str, opt)
write("first write", 9)
write("second write")
list = [6, 77, 88]
write("third write", list)
write("fourth write", 6, 77, 88)
write("sixth write", *list)


def sub(a, b):
    return a-b
print(sub(b=3, a=5))


from datetime import datetime
from time import sleep
def log(msg, when=datetime.now()):
    print('%s %s' %(when, msg))
def log_better(msg, when=None):
    if when is None:
        when = datetime.now()
    print('%s %s' %(when, msg))
log('hello')
sleep(1)
log('hello')

log_better('hello2')
sleep(1)
log_better('hello2')

'''
classes
'''
print("\n\nLearning classes\n\n")
class SimpleGrades(object):
    def __init__(self):
        self._grades = {}
    def add_student(self, name):
        self._grades[name] = []
    def add_grade(self, name, score):
        self._grades[name].append(score)
    def avg_grade(self, name):
        grades = self._grades[name]
        return sum(grades)/len(grades)

book = SimpleGrades()
book.add_student('Newton')
book.add_grade('Newton', 90)
book.add_grade('Newton', 93)
book.add_grade('Newton', 94)
print(book.avg_grade('Newton'))


class SubjectGrades(object):
    def __init__(self):
        self._grades = {}
    def add_student(self, name):
        self._grades[name] = {}
    def add_grade(self, name, subject, score):
        sub = self._grades[name]
        grade_list = sub.setdefault(subject, [])
        grade_list.append(score)

    def avg_grade(self, name):
        by_subs = self._grades[name]
        total, count = 0,0
        for grades in by_subs.values():
            total+= sum(grades)
            count += len(grades)
        return total / count

book = SubjectGrades()
book.add_student('Isaac')
book.add_grade('Isaac', 'Math', 90)
book.add_grade('Isaac', 'Science', 93)
book.add_grade('Isaac', 'Art', 94)
print(book.avg_grade('Isaac'))


import collections
Grade = collections.namedtuple('Grade', ('score', 'weight'))
grade = Grade(95, 0.42)
print(grade)

class Subject(object):
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def avg_grade(self):
        total, total_weight = 0,0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def avg_grade(self):
        total, count = 0,0
        for sub in self._subjects.values():
            total += sub.avg_grade()
            count += 1
        return total/count

class GradeBook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]

book = GradeBook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.8)
math.report_grade(79, 0.8)
math.report_grade(61, 0.8)

art = albert.subject('Art')
art.report_grade(98, 0.5)
art.report_grade(97, 0.5)
art.report_grade(98, 0.5)

print(albert.avg_grade())

# avoiding getters and setters dealing with attributes
from pprint import pprint
from abc import ABC, abstractmethod

class Celsius:
    def __init__(self, temperature = 0):
        self._temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property
    def temperature(self):
        print("Getting value")
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        print("Setting value")
        self._temperature = value

a = Celsius(20)
print(a.temperature)
print(a.to_fahrenheit())

a.temperature = 30
print(a.temperature)
print(a.to_fahrenheit())




class Mark(object):
    def __init__(self, val):
        self.grade   = None
        self._marks   = val

        if self._marks > 90:
            self.grade = 'A'
        elif self._marks > 70:
            self.grade = 'B'
        else:
            self.grade = 'C'

    @property
    def marks(self): #getter
        print("I am a getter")
        return self._marks

    @marks.setter
    def marks(self, marks):
        print("I am a setter", marks)
        self._marks = marks

        if self._marks > 90:
            self.grade = 'A'
        elif self._marks > 70:
            self.grade = 'B'
        else:
            self.grade = 'C'



class Resistor(object):
    #@abstractmethod
    def __init__(self, resistance):
        self.resistance = resistance
        # assert not hasattr(super(), '__init__') # the delegation stops here

    # class Meta():
    #     abstract = True
    # the class meta abstract method does not work


class BoundedResistor(Resistor):
    def __init__(self, resistance):
        super().__init__(resistance)

    @property
    def resistance(self):
        return self._ohms

    @resistance.setter
    def resistance(self, ohms):
        if ohms < 0:
            raise ValueError("%f ohms must be > 0" % ohms)
        self._ohms = ohms


class VoltageResistance(Resistor):
    def __init__(self, resistance):
        super().__init__(resistance)
        self._voltage = 0
        self.current  = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage/self.resistance

r0 = Resistor(1e3)
pprint(vars(r0))
r1 = VoltageResistance(1e3)
pprint(vars(r1))
print(r1.current)
r1.voltage = 10
print(r1.current)
r3 = BoundedResistor(5e3)
r3 = BoundedResistor(0)
pprint(vars(r3))


class General(object):
    def __init__(self):
        self.pub = 2
        self.__pri = 3
    @classmethod
    def get_private(cls, instance):
        return instance.__pri

a = General()
print(a.pub)
# print(a.__pri) # private variable
print(General.get_private(a))
