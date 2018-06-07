import os
from uuid import uuid4

from pymongo import MongoClient
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic import response as res
from sanic_cors import CORS

app = Sanic('some_name')

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.my_database

class View(HTTPMethodView):

    def get(self, request):
        return res.json({'data': list(db.records.find())})

    def post(self, request):
        record = request.json
        record['_id'] = str(uuid4())
        result = db.records.insert_one(record)
        return res.json({'result': str(result)})

    def put(self, request):
        return json({'hello': 'PUT'})

    def delete(self, request):
        return json({'hello': 'DELETE'})

    def options(self, request):
        return res.json({ })


app.add_route(View.as_view(), '/backend/data')

if __name__ == "__main__":
    CORS(app)
    app.run(host="0.0.0.0", port=80, debug=True)
