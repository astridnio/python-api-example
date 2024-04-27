from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

import question_review

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

        return jsonify({"text": text.upper()})
    
class Questions(Resource):
    def get(self):
        """
        This method responds to the GET request for returning a number of questions.
        ---
        tags:
        - Questions
        parameters:
            - name: count
              in: query
              type: integer
              required: false
              description: The number of Questions to return
            - name: sort
              in: query
              type: string
              enum: ['ASC', 'DESC']
              required: false
              description: Sort order for the Questions
        responses:
            200:
                description: A successful GET request
                schema:
                    type: object
                    properties:
                        questions:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                        description: The ID of the question
                                    createdTime:
                                        type: string
                                        description: The creation time of the question
                                    fields:
                                        type: object
                                        description: The fields of the question
                                        properties:
                                            name:
                                                type: string
                                                description: The name of the question
                                            exam:
                                                type: string
                                                description: The exam of the question
                                            options:
                                                type: array
                                                items:
                                                    type: string
                                                description: The options of the question
                                            correct:
                                                type: number
                                                description: The correct response of the question
        """

        count = request.args.get('count')  # Default to returning 10 questions if count is not provided
        sort = request.args.get('sort')

        # Get all the questions
        questions = question_review.get_all_records(count=count, sort=sort)

        # Adjust the format of options and move them into the 'fields' object
        for question in questions:
            fields = question.pop('fields', {})  # Extract the 'fields' object
            options = fields.get('options', '')  # Get the options from the 'fields' object
            fields['options'] = eval(options) if options else []  # Convert options string to list
            question['fields'] = fields  # Place the modified 'fields' object back into the question

        return {"questions": questions}, 200
    
class AddQuestion(Resource):
    def post(self):
        """
        This method responds to the POST request for adding a new record to the DB table.
        ---
        tags:
        - Records
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: ResidencyQuestions
                required:
                  - name
                  - options
                  - correct
                properties:
                  name:
                    type: string
                    description: the name of the question
                  options:
                    type: string
                    description: the options of the question
                  correct:
                    type: integer
                    description: the correct option of the question
                  exam:
                    type: string
                    description: the exam of the question
                    
        responses:
            200:
                description: A successful POST request
            400: 
                description: Bad request, missing 'name' or 'options' or 'correct' in the request body
        """

        data = request.json
        print(data)

        # Check if 'name' and 'options' and 'correct' are present in the request body
        if 'name' not in data or 'options' not in data or 'correct' not in data:
            return {"message": "Bad request, missing 'name' or 'options' or 'correct' in the request body"}, 400
        # Call the add_record function to add the record to the DB table
        success = question_review.add_record(data)

        if success:
            return {"message": "Record added successfully"}, 200
        else:
            return {"message": "Failed to add record"}, 500
        


api.add_resource(AddQuestion, "/add-question")
api.add_resource(Questions, "/questions")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)