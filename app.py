from flask import Flask, request
from flask_restful import Resource, Api
from models import People, Activities, User
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
# HARDCODED USERS
# USERS = {
#     "fred": "1234",
#     "roberta": "321"
# }
#
#
# @auth.verify_password
# def verification(login, password):
#     if not (login, password):
#         return False
#     return USERS.get(login) == password


@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return User.query.filter_by(login=login, password=password).first()


class PeopleAPI(Resource):
    @auth.login_required
    def get(self, name):
        people = People.query.filter_by(name=name).first()
        try:
            response = {
                "name": people.name,
                "age": people.age,
                "id": people.id
            }
        except AttributeError:
            response = {"status": "Error", "message": "People not found!"}
        return response

    def put(self, name):
        people = People.query.filter_by(name=name).first()
        people_data = request.json
        if 'name' in people_data:
            people.name = people_data['name']
        if 'age' in people_data:
            people.age = people_data['age']
        people.save()
        response = {
            "id": people.id,
            "name": people.name,
            "age": people.age
        }
        return response

    def delete(self, name):
        people = People.query.filter_by(name=name).first()
        people.delete()
        message = f"{people.name} Deleted!"
        return {"status": "Success", "Message": message}


class PeopleListAPI(Resource):
    @auth.login_required()
    def get(self):
        people = People.query.all()
        response = [{'id':i.id, 'name': i.name, 'age': i.age} for i in people]
        return response

    def post(self):
        people_data = request.json
        people = People(name=people_data['name'], age=people_data['age'])
        people.save()
        response = {
            'id': people.id,
            'name': people.name,
            'age': people.age
        }
        return response


class ActivitiesAPI(Resource):
    def get(self):
        atv = Activities.query.all()
        response = [{"id": a.id, "name": a.name, "people": a.people.name} for a in atv]
        return response

    def post(self):
        data = request.json
        people = People.query.filter_by(name=data['people']).first()
        atv = Activities(name=data['name'], people=people)
        atv.save()
        response = {
            "people": atv.people.name,
            "name": atv.name,
            "id": atv.id
        }
        return response


api.add_resource(PeopleAPI, "/people/<string:name>/")
api.add_resource(PeopleListAPI, '/people/')
api.add_resource(ActivitiesAPI, '/activities/')

if __name__ == '__main__':
    app.run(debug=True)
