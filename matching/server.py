from matching import app

@app.route('/')
def index():
    return "OK"
