from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "¡Funciona tu nuevo proyecto Flask en Render!"

if __name__ == "__main__":
    app.run()
