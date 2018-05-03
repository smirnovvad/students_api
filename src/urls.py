from flask import Blueprint, request, jsonify
from models import db, Student, Group, User
from schema import ma, StudentSchema, GroupSchema, UserSchema
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


jwt = JWTManager()


student_schema = StudentSchema()
group_schema = GroupSchema()
user_schema = UserSchema()
students_schema = StudentSchema(many=True)
groups_schema = GroupSchema(many=True)
users_schema = UserSchema(many=True)


urls_blueprint = Blueprint('urls', __name__,)


### STUDENTS ###s
@urls_blueprint.route("/student", methods=["GET"])
@jwt_required
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)


# ADD STUDENT
@urls_blueprint.route("/student", methods=["POST"])
@jwt_required
def add_student():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    middle_name = request.json['middle_name']
    email = request.json['email']
    group_id = request.json['group_id']
    traing = request.json['traing']

    new_student = Student(email, first_name, last_name, middle_name, group_id, traing)

    db.session.add(new_student)
    db.session.commit()

    return jsonify(student_schema.dump(new_student))


# GET STUDENT
@urls_blueprint.route("/student/<int:pk>", methods=["GET"])
@jwt_required
def student_detail(pk):
    try:
        student = Student.query.get(pk)
        student_result = student_schema.dump(student)
    except AttributeError:
        return jsonify({"message": "Student could not be found."}), 400
    group_result = group_schema.dump(student.group)
    return jsonify({"student": student_result, "group": group_result})


# STUDENT UPDATE
@urls_blueprint.route("/student/<int:pk>", methods=["PUT"])
@jwt_required
def student_update(pk):
    student = Student.query.get(pk)
    phone = request.json['phone']

    student.phone = phone

    db.session.commit()
    return jsonify(student_schema.dump(student))


# DEL STUDENT
@urls_blueprint.route("/student/<int:pk>", methods=["DELETE"])
@jwt_required
def student_delete(pk):
    try:
        student = Student.query.get(pk)
        db.session.delete(student)
        db.session.commit()
    except AttributeError:
        return jsonify({"message": "Student could not be found."}), 400

    return student_schema.dump(student)


# GROUPS
@urls_blueprint.route("/group", methods=["GET"])
@jwt_required
def get_groups():
    all_group = Group.query.all()
    result = groups_schema.dump(all_group)
    return jsonify(result)


# GET GROUP
@urls_blueprint.route("/group/<int:pk>", methods=["GET"])
@jwt_required
def group_detail(pk):
    try:
        group = Group.query.get(pk)
        group_result = group_schema.dump(group)
    except AttributeError:
        return jsonify({"message": "Group could not be found."}), 400
    return jsonify(group_result)


# GROUP STUDENTS
@urls_blueprint.route("/group/<int:pk>/students", methods=["GET"])
@jwt_required
def group_students(pk):
    group = Group.query.get(pk)
    group_result = group_schema.dump(group)
    students_result = students_schema.dump(Student.query.filter(Student.group_id == group.id))
    return jsonify({"students": students_result, "group": group_result})


# GET AUTH
@urls_blueprint.route("/auth", methods=["POST"])
def auth():
    print(request.get_data())
    if not request.is_json:
        # print(request.get_data())
        return jsonify({"message": "Missing JSON in request"}), 400
    telegram_id = request.json.get('telegram_id', None)
    user = User.query.filter(User.telegram_id == telegram_id).scalar()
    if user is not None:
        result = user_schema.dump(user)
        access_token = create_access_token(identity=result['telegram_id'])
        result['access_token'] = access_token
        return jsonify(result), 200
    else:
        user = Student.query.filter(Student.telegram_id == telegram_id).scalar()
        if user is not None:
            result = student_schema.dump(user)
            access_token = create_access_token(identity=result['telegram_id'])
            result['access_token'] = access_token
            return jsonify(result), 200
        else:
            return jsonify({'message': 'User with this telegram_id not found'}), 400


# GET USER
@urls_blueprint.route("/user/<int:pk>", methods=["GET"])
@jwt_required
def user_detail(pk):
    try:
        user = User.query.get(pk)
        user_result = user_schema.dump(user)
    except AttributeError:
        return jsonify({"message": "Student could not be found."}), 400
    # group_result = group_schema.dump(student.group)
    return jsonify({"student": user_result})