from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from models import db, Task

tasks_bp = Blueprint("Tasks", "tasks", url_prefix="/tasks", description="Task APIs")


# --- Schemas ---
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str()


class TaskUpdateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()


# --- Task list (GET / POST) ---
@tasks_bp.route("/")
class TasksList(MethodView):
    @jwt_required()
    @tasks_bp.response(200, TaskSchema(many=True))
    @tasks_bp.doc(security=[{"BearerAuth": []}])
    def get(self):
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return tasks

    @jwt_required()
    @tasks_bp.arguments(TaskSchema)
    @tasks_bp.response(201, TaskSchema)
    @tasks_bp.doc(security=[{"BearerAuth": []}])
    def post(self, new_data):
        user_id = get_jwt_identity()
        task = Task(**new_data, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return task

    # Handle OPTIONS for CORS preflight
    def options(self):
        return {}, 200


# --- Task item (GET / PUT / DELETE) ---
@tasks_bp.route("/<int:task_id>")
class TaskItem(MethodView):
    @jwt_required()
    @tasks_bp.response(200, TaskSchema)
    @tasks_bp.doc(security=[{"BearerAuth": []}])
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        return task

    @jwt_required()
    @tasks_bp.arguments(TaskUpdateSchema)
    @tasks_bp.response(200, TaskSchema)
    @tasks_bp.doc(security=[{"BearerAuth": []}])
    def put(self, update_data, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        if "title" in update_data:
            task.title = update_data["title"]
        if "description" in update_data:
            task.description = update_data["description"]
        if "status" in update_data:
            task.status = update_data["status"]

        db.session.commit()
        return task

    @jwt_required()
    @tasks_bp.doc(security=[{"BearerAuth": []}])
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return {"msg": "Task deleted"}

    # Handle OPTIONS for CORS preflight
    def options(self, task_id=None):
        return {}, 200