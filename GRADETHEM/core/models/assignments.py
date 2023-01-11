import enum
import sys
import logging

from marshmallow import ValidationError

from core import db
from core.apis.decorators import Principal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum
log = logging.getLogger(__name__)

class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    # def __repr__(self):
    #     return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')

            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, principal: Principal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.student_id == principal.student_id, 'This assignment belongs to some other student')
        # assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
        assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                 'only a draft assignment can be submitted')

        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()

        return assignment
    @classmethod
    def updateGrade(cls,p,id,grade):
        assignment = Assignment.get_by_id(id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be graded')
        assertions.assert_valid(
            (assignment.state == AssignmentStateEnum.SUBMITTED) or (assignment.state == AssignmentStateEnum.GRADED),
            "ASSIGNMENT NOT YET SUBMITTED")

        assertions.assert_valid(assignment.teacher_id == p.teacher_id,'assigment for diffrent teacher')



        # if grade == "A":
        #     assignment.grade = GradeEnum.A
        # elif grade == "B":
        #     assignment.grade = GradeEnum.B
        # elif grade == "C":
        #     assignment.grade = GradeEnum.C
        # elif grade == "D":
        #     assignment.grade = GradeEnum.D
        g = ['A',"B","C","D"]
        if grade in g:
            assignment.grade = GradeEnum(grade)
            assignment.state=AssignmentStateEnum.GRADED


        else :
            # assertions.assert_valid(1==2,"INVALID GRADE")
            raise ValidationError('INVALID GRADE')



        db.session.flush()
        return assignment
    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()
    
    @classmethod
    def get_assignments_by_teacher(cls,teacher_id):

        return cls.filter(cls.teacher_id==teacher_id).all()
    
    
