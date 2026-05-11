from flask import Blueprint, jsonify, request

analyzer_bp = Blueprint('analyzer', __name__)

@analyzer_bp.route('/analyze', methods=['POST'])
def analyze():
    # 增加日誌以便除錯
    print(f"Request received: {request.url}")
    print(f"Request data: {request.get_data()}")
    
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Missing text in request body"}), 400
    
    text = data['text']
    word_count = len(text.split())
    
    return jsonify({
        "status": "success",
        "word_count": word_count,
        "summary": "Text analyzed successfully"
    })
