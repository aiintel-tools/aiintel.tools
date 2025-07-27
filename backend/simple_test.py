from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'AI Directory API is running'
    }), 200

if __name__ == '__main__':
    print("Starting simple Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)

