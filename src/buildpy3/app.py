from flask import Flask, request, jsonify
#from flask_swagger_ui import get_swaggerui_blueprint
from flask_restx import Api, Resource
import logging
import hmac
import hashlib


# Setup logging
logging.basicConfig(level=logging.INFO)

# Log to console by default
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

app = Flask(__name__)

api = Api(app, version='1.0', title='Echo API',
          description='A simple echo API')

ns = api.namespace('build', description='build operations')

app.logger.addHandler(console_handler)


# # Define Swagger UI blueprint
# SWAGGER_URL = '/swagger'
# API_URL = '/swagger.yml'
# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "File Upload Service"
#     }
# )
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

def validate_file(file):
    # Perform file validation here
    # For demonstration purposes, just checking if the file name ends with .txt
    if not file.filename.endswith('.txt'):
        return False
    return True


@ns.route('/ping',methods=['GET'])
class PingerBuilder(Resource):
    def get(self):
        logging.warn("ping called")
        return jsonify({'message': 'Docker build service ping'}), 200


@ns.route('/<string:param>')
@api.doc(params={'param': 'A parameter to build'})
class Builder(Resource):
    def post(self, param):
        logging.warn(f"build called with param: {param}")
        return jsonify({'message': 'Docker build service'}), 200


global WEBHOOK_SECRET
WEBHOOK_SECRET = 'github'


def verify_signature(payload, signature):
    """Verify the request signature."""
    sha_name, signature = signature.split('=')
    if sha_name != 'sha1':
        return False
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)

#@app.route('/webhook', methods=['POST'])
@ns.route('/github/<string:param>',methods=['POST'])
@api.doc(params={'param': 'A repo to build'})
class Webhook(Resource):
    def post(self, param):
        logging.warn(f"webhook called: {param}")
        # GitHub sends the signature in the header 'X-Hub-Signature'
        signature = request.headers.get('X-Hub-Signature')

        # GitHub sends the event type in the header 'X-GitHub-Event'
        event_type = request.headers.get('X-GitHub-Event')

        payload = request.data

        # Verify the signature
        if not verify_signature(payload, signature):
            return jsonify({'message': 'Invalid signature'}), 403

        # Process the GitHub event here (e.g., push, pull request)
        logging.warn(f'Event: {event_type}')
        logging.warn(f'Payload: {payload}')

        # Respond to GitHub that the webhook was successfully received
        return jsonify({'message': 'Webhook received!'}), 200




# @app.routeold('/webhook', methods=['POST'])
# def webhook():
#     logging.warn("webhook called")
#     # Verify the request is coming from GitHub by checking the User-Agent header
#     user_agent = request.headers.get('User-Agent')
#     if 'GitHub-Hookshot' in user_agent:
#         # Parse the JSON payload from the request
#         payload = request.json
        
#         # Extract relevant information from the payload
#         repository_name = payload['repository']['full_name']

#         logging.warn(payload)

#         # action = payload['action']
#         # sender = payload['sender']['login']
        
#         # # Perform actions based on the event
#         # if action == 'push':
#         #     print(f"Repository {repository_name} was pushed to by {sender}.")
#         #     # Perform actions you want to take on push event
#         # elif action == 'pull_request':
#         #     print(f"Pull request on repository {repository_name} was opened by {sender}.")
#         #     # Perform actions you want to take on pull request event
#         # else:
#         #     print(f"Unhandled action: {action}")
        
#         # Return a success response to GitHub
#         print("returning")
#         return jsonify({'message': 'Received webhook event successfully'}), 200
#     else:
#         # If the request doesn't come from GitHub, return a 403 Forbidden response
#         return jsonify({'error': 'Forbidden'}), 403


# @app.route('/v1/upload', methods=['POST'])
# def upload_file():
#     file_type = request.form.get('file_type')
#     period = request.form.get('period')
#     uploaded_file = request.files['file']
    
#     if not validate_file(uploaded_file):
#         return jsonify({'error': 'Invalid file format. Please upload a .txt file.'}), 400
    
#     # Save the uploaded file to a directory or perform further processing
#     # For now, just logging the details
#     app.logger.info('File Type: %s', file_type)
#     app.logger.info('Period: %s', period)
#     app.logger.info('Uploaded File Name: %s', uploaded_file.filename)

#     return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
