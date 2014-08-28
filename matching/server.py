from a import app

@app.route('/')
def index():
    return "OK"
