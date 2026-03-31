from flask_smorest import Blueprint
from flask.views import MethodView
# from flask import Blueprint, request, jsonify
# from models import db, Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields

from models import db, Task

tasks_bp = Blueprint("Tasks", "tasks", url_prefix="/tasks", description="Task APIs")
#tasks_bp = Blueprint("tasks", __name__)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str()

class TaskUpdateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()

@tasks_bp.route("/")
class TasksList(MethodView):

    @tasks_bp.response(200, TaskSchema(many=True))
    @jwt_required()
    def get(self):
        # GET all tasks
        # @tasks_bp.route("/tasks", methods=["GET"])
        # @jwt_required()
        # def get_tasks():
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        # return jsonify([{
        #     "id": t.id,
        #     "title": t.title,
        #     "description": t.description,
        #     "status": t.status
        # } for t in tasks])
        return tasks

    # POST create task
    # @tasks_bp.route("/tasks", methods=["POST"])
    # @jwt_required()
    # def create_task():
    
    @tasks_bp.arguments(TaskSchema)
    @tasks_bp.response(201, TaskSchema)
    @jwt_required()
    def post(self, new_data):
        user_id = get_jwt_identity()
        # data = request.get_json()

        # if not data.get("title"):
        #     return jsonify({"msg": "Title is required"}), 400

        # task = Task(
        #     title=data["title"],
        #     description=data.get("description"),
        #     status=data.get("status", "pending"),
        #     user_id=user_id
        # )
        task = Task(**new_data, user_id=user_id)
        db.session.add(task)
        db.session.commit()

        # return jsonify({"msg": "Task created"}), 201
        return task

# PUT update task
@tasks_bp.route("/<int:task_id>")
class TaskItem(MethodView):
    # @tasks_bp.route("/tasks/<int:id>", methods=["PUT"])
    # @jwt_required()
    # def update_task(id):
    
    @tasks_bp.response(200, TaskSchema)
    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()

        # task = Task.query.filter_by(id=id, user_id=user_id).first()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        if not task:
            return {"msg": "Task not found"}, 404

        # data = request.get_json()

        # task.title = data.get("title", task.title)
        # task.description = data.get("description", task.description)
        # task.status = data.get("status", task.status)

        # db.session.commit()

        # return jsonify({"msg": "Task updated"})

        return task

    # PUT /tasks/{id}
    @tasks_bp.arguments(TaskUpdateSchema)
    @tasks_bp.response(200, TaskSchema)
    @jwt_required()
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
    # DELETE task
    # def delete_task(id):
    # @tasks_bp.route("/tasks/<int:id>", methods=["DELETE"])
    # @jwt_required()
    # def delete_task(id):
    @tasks_bp.response(200)
    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        #task = Task.query.filter_by(id=id, user_id=user_id).first()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        if not task:
            # return jsonify({"msg": "Task not found"}), 404
            return {"msg": "Task not found"}, 404

        db.session.delete(task)
        db.session.commit()

        # return jsonify({"msg": "Task deleted"})
        return {"msg": "Task deleted"}