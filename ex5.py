import json
import os


def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    with open(input_json_path, 'r') as f:
        student_db = json.load(f)
    return [s['student_name'] for _, s in student_db.items() if course_name in s.get('registered_courses', [])]


def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """
    with open(input_json_path, mode='r') as f:
        student_db = json.load(f)
    course_db = {}
    # Group by courses count:
    for _, s in student_db.items():
        for course in s.get('registered_courses', []):
            if course not in course_db:
                course_db[course] = 1
            else:
                course_db[course] += 1

    course_names = list(course_db.keys())
    course_names.sort()
    # write to file:
    with open(output_file_path, mode='w') as f:
        for course in course_names:
            f.write('"{course}" {value}\n'.format(course=course, value=course_db[course]))


def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    db_names = [path for path in os.listdir(json_directory_path) if path[-5:] == '.json']

    lecturers_db = {}
    for name in db_names:
        db_path = os.path.join(json_directory_path, name)
        with open(db_path, 'r') as f:
            semester_db = json.load(f)
        for _, course in semester_db.items():
            for lecturer in course.get('lecturers', []):
                if lecturer not in lecturers_db:
                    lecturers_db[lecturer] = [course['course_name'], ]
                else:
                    if course['course_name'] not in lecturers_db[lecturer]:
                        lecturers_db[lecturer].append(course['course_name'])

    with open(output_json_path, mode='w') as f:
        json.dump(lecturers_db, f, indent=4)
