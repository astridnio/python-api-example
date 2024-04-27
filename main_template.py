from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return {"text": text.upper()}, 200

api.add_resource(UppercaseText, "/uppercase")


class modifiedText(Resource):

    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
            - name: duplication
              in: query
              type: integer
              required: false
              description: Number of times to duplicate the text
            - name: modifytext
              in: query
              type: string
              required: false
              description: Specify '1', '2', or '0' to modify the text accordingly
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase, lowercase, or unchanged
        """
        text = request.args.get('text')
        duplication = int(request.args.get('duplication', 1))  # Default to 1 if not provided
        modify_text = request.args.get('modifytext', 'none')

        duplicated_text = text * duplication

        if modify_text == '1':
            modified_text = duplicated_text.upper()
        elif modify_text == '2':
            modified_text = duplicated_text.lower()
        else:
            modified_text = duplicated_text

        return {"text": modified_text}, 200

api.add_resource(modifiedText, '/modifiedText')

if __name__ == "__main__":
    app.run(debug=True)