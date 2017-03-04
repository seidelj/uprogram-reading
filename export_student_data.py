import website.wsgi
import os, csv
from mathtutor.models import Student
from django.db.models import Q

ROOT = os.path.dirname(os.path.abspath(__file__))
csvFile = os.path.join(ROOT, 'student_data_reading.csv')


def write_headers(writer):
    headers = ['student_id', 'group', 'district', 'treatment', 'earned_wage', 'quizes_passed']
    writer.writerow(headers)

def build_row(student):
    student_id = str(student.stuid.username)
    group = student.group
    district = student.district
    treatment = student.treatment
    resultsDict = student.get_wage_info()
    earned_wage = resultsDict['earned']
    quizes_passed = student.get_quiz_progress()['passed']
    return [student_id, group, district, treatment, earned_wage, quizes_passed]

def main():
    with open(csvFile, 'w') as f:
        writer = csv.writer(f, csv.excel)
        write_headers(writer)
        for student in Student.objects.filter(Q(district='152b2') | Q(district='152cm2') | Q(district='152cp2')):
            writer.writerow(build_row(student))


if __name__ == "__main__":
    main()
