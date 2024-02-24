from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Define Swagger UI blueprint
SWAGGER_URL = '/swagger'
API_URL = '/swagger.yml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "File Upload Service"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

def validate_file(file):
    # Perform file validation here
    # For demonstration purposes, just checking if the file name ends with .txt
    if not file.filename.endswith('.txt'):
        return False
    return True

@app.route('/v1/build', methods=['GET'])
def buildproject():
    return jsonify({'message': 'Docker build service'})

#asd

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify the request is coming from GitHub by checking the User-Agent header
    user_agent = request.headers.get('User-Agent')
    if 'GitHub-Hookshot' in user_agent:
        # Parse the JSON payload from the request
        payload = request.json
        
        # Extract relevant information from the payload
        repository_name = payload['repository']['full_name']

        print(payload)

        # action = payload['action']
        # sender = payload['sender']['login']
        
        # # Perform actions based on the event
        # if action == 'push':
        #     print(f"Repository {repository_name} was pushed to by {sender}.")
        #     # Perform actions you want to take on push event
        # elif action == 'pull_request':
        #     print(f"Pull request on repository {repository_name} was opened by {sender}.")
        #     # Perform actions you want to take on pull request event
        # else:
        #     print(f"Unhandled action: {action}")
        
        # Return a success response to GitHub
        print("returning")
        return jsonify({'message': 'Received webhook event successfully'}), 200
    else:
        # If the request doesn't come from GitHub, return a 403 Forbidden response
        return jsonify({'error': 'Forbidden'}), 403


@app.route('/v1/upload', methods=['POST'])
def upload_file():
    file_type = request.form.get('file_type')
    period = request.form.get('period')
    uploaded_file = request.files['file']
    
    if not validate_file(uploaded_file):
        return jsonify({'error': 'Invalid file format. Please upload a .txt file.'}), 400
    
    # Save the uploaded file to a directory or perform further processing
    # For now, just logging the details
    app.logger.info('File Type: %s', file_type)
    app.logger.info('Period: %s', period)
    app.logger.info('Uploaded File Name: %s', uploaded_file.filename)

    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)