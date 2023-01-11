from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema,AssignmentGradeSchema
teacher_assignment_resources = Blueprint('teacher_assignment_resources', __name__)

@teacher_assignment_resources.route('/assignments',methods=['GET'],strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    teacherwise = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacherwisedump = AssignmentSchema().dump(teacherwise,many=True)
    return APIResponse.respond(data=teacherwisedump)

@teacher_assignment_resources.route('/assignments/grade',methods=['POST'],strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def gradeAssignment(p,incoming_payload):
    # print("calleed",file=sys.stderr)
      assignment = AssignmentGradeSchema().load(incoming_payload)

      assignment.teacher_id= p.teacher_id

    #
      gradeded_assignment = Assignment.updateGrade(p=p,id=assignment.id, grade=incoming_payload['grade'])

      db.session.commit()
      gradeded_assignment_dump = AssignmentSchema().dump(gradeded_assignment)
      return APIResponse.respond(data=gradeded_assignment_dump)

