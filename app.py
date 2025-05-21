from flask import Flask

app = Flask(__name__)  # 实例化并命名为app实例


@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
