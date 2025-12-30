from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def home():
        return jsonify(status="ok", message="Hello from Flask")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
