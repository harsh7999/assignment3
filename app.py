from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_detail.db'
db = SQLAlchemy(app)

class Task(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    #dob = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.first_name

taskFields = {
    'student_id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    #'dob':fields.DateTime,
    'amount_due':fields.Integer
 }

class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks = Task.query.all()
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data = request.json
        #dob_str = data.get('dob')
        #dob = datetime.strptime(dob_str, "%Y-%m-%dT%H:%M:%SZ")
        task = Task(first_name=data['first_name'], last_name=data['last_name'], amount_due=data['amount_due'])
        #task = Task(first_name=data['first_name'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks
    
class Item(Resource):
    @marshal_with(taskFields)
    def get(self, pk):
        task = Task.query.filter_by(student_id=pk).first()
        return task
    
    @marshal_with(taskFields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(student_id=pk).first()
        #task = Task(first_name=data['first_name'], last_name=data['last_name'], amount_due=data['amount_due'])
        task.first_name = data['first_name']
        task.last_name = data['last_name']
        task.amount_due = data['amount_due']
        db.session.commit()
        return task
    
    @marshal_with(taskFields)
    def delete(self, pk):
         task = Task.query.filter_by(student_id=pk).first()
         db.session.delete(task)
         db.session.commit()
         tasks = Task.query.all()
         return tasks
    
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

if __name__ == '__main__':
    app.run(debug=True)