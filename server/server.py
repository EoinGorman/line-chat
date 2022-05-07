from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/send_message',  methods = ['POST'])
def send_message():
    message = request.get_data().decode("utf-8") 
    return 'Sent message: ' + message

if __name__ == '__main__':
    app.run(port=4567)