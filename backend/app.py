from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({
        "message": "Welcome to AI Directory API",
        "name": "AI Directory API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "message": "AI Directory API is running",
        "status": "healthy",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

