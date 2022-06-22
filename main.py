from flask import Flask, json, request, render_template
import pymysql.cursors

class Student:
    name = None
    surname = None
    id = None
    group = None
    age = None

    def __init__(self, id_,  name, surname, age, group):
        self.id = id_
        self.age = age
        self.group = group
        self.surname = surname
        self.name = name

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_age(self):
        return self.age

    def get_group(self):
        return self.group


class StudentMapper:
    connection_ = None
    cursor = None

    def __init__(self):
        self.connection_ = pymysql.connect(host='0.0.0.0',
                                           user='руру',
                                           password='руру',
                                           db='students_for_sit',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection_.cursor()

    def insert(self, student):
        id_line = f"select max(id) from students "
        self.cursor.execute(id_line)
        id_ = -1
        for row in self.cursor:
            id_ = row['max(id)']
        id_ += 1
        sql = "insert into students (id, name, surname, age, `group`) values ({}, '{}', '{}',{},'{}')". \
            format(id_, student.name, student.surname, student.age, student.group)

        self.cursor.execute(sql)
        self.connection_.commit()
        return id_

    # def update(self, student):
    #     self.cursor.execute("update students set  name = '{}', surname = '{}', age = {}, group = '{}' where id = {}". \
    #                         format(student.name, student.surname, student.age, student.group, student.id))
    #     self.connection_.commit()

    def delete(self, id):
        self.cursor.execute("delete from students where id = {}".format(id))
        self.connection_.commit()

    def get_all(self):
        self.cursor.execute("select * from students")
        res = []
        for row in self.cursor:
            student = Student(row['id'], row['name'], row['surname'], row['age'], row['group'])
            res.append(student)
        return res

    def get_by_id(self, id_):
        self.cursor.execute("select * from students where id = '{}'".format(id_))
        res = []
        for row in self.cursor:
            student = Student(row['id'], row['name'], row['surname'], row['age'], row['group'])
            res.append(student)
        return res

    def get_by_name(self, name):
        self.cursor.execute("select * from students where name = '{}'".format(name))
        res = []
        for row in self.cursor:
            student = Student(row['id'], row['name'], row['surname'], row['age'], row['group'])
            res.append(student)
        return res


class StudentRepository:
    mapper = StudentMapper
    data = []

    def __init__(self, mapper):
        self.data = []
        self.mapper = mapper
        self.update_storage()

    def update_storage(self):
        self.data = self.mapper().get_all()

    def get_all_students(self):
        return self.data

    def get_one_student(self, id_):
        return self.mapper().get_by_id(id_)

    def save(self, student):
        self.mapper().insert(student)

    def delete(self, id):
        self.mapper().delete(id)

    def get_by_name_one_student(self, name):
        return self.mapper().get_by_name(name)


app = Flask(__name__)
studentMapper = StudentMapper


@app.route('/', methods=['POST', 'GET'])
def main():
    studentMapper = StudentMapper
    students = StudentRepository(studentMapper).get_all_students()
    if request.method == 'GET':
        return render_template('index.html', students=students)
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = request.form.get('age')
        group = request.form.get('group')
        new_student = Student(1, name, surname, age, group)
        try:
            if name != '':
                StudentRepository(studentMapper).save(new_student)
            return render_template('index.html', students=students)
        except:
            return render_template('index.html', students=students)


@app.route('/get_by_id', methods=['POST'])
def get_by_id():
    id = request.form.get('id')
    studentMapper = StudentMapper
    students = StudentRepository(studentMapper).get_all_students()
    try:
        students = StudentRepository(studentMapper).get_one_student(id)
        return render_template('index.html', students=students)
    except:
        return render_template('index.html', students=students)


@app.route('/get_all', methods=['POST'])
def get_all():
    studentMapper = StudentMapper
    students = StudentRepository(studentMapper).get_all_students()
    return render_template('index.html', students=students)


@app.route('/get_by_name', methods=['POST'])
def get_by_name():
    name = request.form.get('name')
    studentMapper = StudentMapper
    students = StudentRepository(studentMapper).get_all_students()
    try:
        students = StudentRepository(studentMapper).get_by_name_one_student(name)
        return render_template('index.html', students=students)
    except:
        return render_template('index.html', students=students)


@app.route('/delete', methods=['POST'])
def delete():
    id = request.form.get('id')
    studentMapper = StudentMapper
    students = StudentRepository(studentMapper).get_all_students()
    try:
        StudentRepository(studentMapper).delete(id)
        students = StudentRepository(studentMapper).get_all_students()
        return render_template('index.html', students=students)
    except:
        return render_template('index.html', students=students)


if __name__ == '__main__':
    studentMapper = StudentMapper
    StudentRepository(studentMapper).update_storage()
    app.run()



