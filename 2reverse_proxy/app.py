from flask import Flask
app = Flask(__name__)

@app.route('/api/message')
def message():
    return 'Hello from Flask backend!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
