def create_app():
    @app.route("/register", methods=["GET","POST"])
    def register(app):
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if username == username and password == password:
                session['username'] = username


