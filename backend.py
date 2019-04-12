from flask import Flask, request, jsonify, escape
from flask_restful import Resource, Api
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///menu.db')
app = Flask(__name__)
api = Api(app)

class Sections(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT sectionID, sectionName FROM Sections;")
        sections = query.fetchall()
        result = {
            'MenuSection': [{'id': row[0], 'name': row[1]} for row in sections]
        }
        return jsonify(result)

    def put(self):
        conn = db_connect.connect()
        name = escape(request.json['name'])

        # get the next id
        query = conn.execute("SELECT MAX(sectionID) FROM Sections;")
        resp = query.fetchall()
        curr_id = 0 # next id = curr_id + 1
        if resp is not None and resp[0][0] is not None: # if there were no records in Sections, then the next id would be 1
            curr_id = int(resp[0][0])

        # insert new section
        conn.execute("INSERT INTO Sections VALUES ({0}, '{1}')".format(curr_id + 1, name))

        # success, fetch all sections, return
        query = conn.execute("SELECT sectionID, sectionName FROM Sections;")
        sections = query.fetchall()
        result = {
            'success': True,
            'MenuSection': [{'id': row[0], 'name': row[1]} for row in sections]
        }
        return jsonify(result)

class Sections_ID(Resource):
    def get(self, sectionID):
        conn = db_connect.connect()
        query = conn.execute("SELECT sectionID, sectionName FROM Sections WHERE sectionID = {0};".format(sectionID))
        sections = query.fetchall()
        result = {}
        if sections == []:
            result = {'error': "sectionID not found."}
        else:
            result = {
                'MenuSection': [{'id': sections[0][0], 'name': sections[0][1]}]
            }
        return jsonify(result)

    def post(self, sectionID):
        conn = db_connect.connect()
        name = escape(request.json['name'])

        # update new name
        update = conn.execute("UPDATE Sections SET sectionName = '{0}' WHERE sectionID = {1}".format(name, sectionID))

        # success, fetch all sections, return
        query = conn.execute("SELECT sectionID, sectionName FROM Sections;")
        sections = query.fetchall()
        result = {
            'success': True,
            'MenuSection': [{'id': row[0], 'name': row[1]} for row in sections]
        }
        return jsonify(result)

    def delete(self, sectionID):
        conn = db_connect.connect()
        deletion = conn.execute("DELETE FROM Sections WHERE sectionID = {0};".format(sectionID))
        result = {
            'success': True
        }
        return jsonify(result)


        

api.add_resource(Sections, '/menusection')
api.add_resource(Sections_ID, '/menusection/<sectionID>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')