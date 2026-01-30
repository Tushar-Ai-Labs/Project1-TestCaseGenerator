from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.generator import generate_test_cases

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    feature = data.get('feature_description')
    test_type = data.get('test_type', 'all')  # Default to 'all'
    
    if not feature:
        return jsonify({"error": "feature_description is required"}), 400
        
    try:
        result = generate_test_cases(feature, test_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
