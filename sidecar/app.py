from flask import Flask, jsonify
from routes.analyzer import analyzer_bp
from routes.scraper import scraper_bp

app = Flask(__name__)

# 註冊 Blueprints
app.register_blueprint(analyzer_bp, url_prefix='/api/analyzer')
app.register_blueprint(scraper_bp, url_prefix='/api/scraper')

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

# 簡單除錯：印出路由對應表
with app.app_context():
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
