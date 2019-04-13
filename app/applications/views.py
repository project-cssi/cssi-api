from flask_restful import Resource


class Application(Resource):
    def get(self):
        return {"message": "Get Application"}

    def post(self):
        return {"message": "Add Application"}
