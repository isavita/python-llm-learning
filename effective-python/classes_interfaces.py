class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        if not grades:
            return None
        return sum(grades) / len(grades)


grade_book = SimpleGradebook()
grade_book.add_student("Ivan")
grade_book.report_grade("Ivan", 50)
grade_book.add_student("John")
grade_book.report_grade("Ivan", 84)
grade_book.add_student("Anna")
grade_book.report_grade("Anna", 75)
grade_book.report_grade("Anna", 94)
grade_book.report_grade("Anna", 86)

assert grade_book.average_grade("Anna") == 85
assert grade_book.average_grade("John") == None

grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
assert total == 89.5
total_weight = sum(weight for _, weight in grades)
assert total_weight == 1
average_grade = total / total_weight
assert average_grade == 89.5

from collections import namedtuple

Grade = namedtuple("Grade", ("score", "weight"))
grades = []
grades.append(Grade(score=95, weight=0.45))
grades.append(Grade(score=84, weight=0.55))
total = sum(g.score * g.weight for g in grades)
assert total == 88.95


class Subject:
    def __init__(self) -> None:
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        grades = self._grades
        if not grades:
            return 0

        total, total_weight = 0, 0
        for grade in grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


from collections import defaultdict


class Student:
    def __init__(self) -> None:
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        values = self._subjects.values()
        if not values:
            return 0

        total, count = 0, 0
        for subject in values:
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook:
    def __init__(self) -> None:
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


book = Gradebook()
albert = book.get_student("Albert Einstein")
math = albert.get_subject("Math")
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject("Gym")
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)

assert albert.average_grade() == 80.25
