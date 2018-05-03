from flask_marshmallow import Marshmallow
from models import Student, Group, User


ma = Marshmallow()


class StudentSchema(ma.Schema):
    class Meta:
        model = Student
        # include_fk = True
        # Fields to expose
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', '_links', 'traing', 'telegram_id', 'phone')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('urls.student_detail', pk='<id>'),
        'collection': ma.URLFor('urls.get_students')
    })


class GroupSchema(ma.Schema):
    class Meta:
        model = Group
        # Fields to expose
        fields = ('id', 'name_group', '_links')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('urls.group_detail', pk='<id>'),
        'collection': ma.URLFor('urls.get_groups'),
        'students': ma.URLFor('urls.group_students', pk='<id>')
    })


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'username')
