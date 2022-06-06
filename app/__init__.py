from flask import Flask, render_template, request, session, redirect, url_for

from data.users import user_exists, verify_user, create_user
from os import urandom
from data.data_functions import *
reset_data()
app = Flask(__name__)
debug = True
app.secret_key = urandom(32)

dict =	{
  "3D printer": 0,
  "Laser cutter": 0,
  "another machine": 0
}


# @app.route("/", methods=["GET","POST"])
# def home():
#     return render_template("machinelist.html")


@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
    if session.get('username') is not None:
        user = session['username']
        # return render_template("profile.html", user=user)
        return render_template("machinelist.html")

    else:
        return render_template("machinelist.html")



@app.route("/machine", methods=["GET","POST"])
def machine():
    if (request.args['machine'] == "3D printer"):
        return render_template("machine.html", printer = "checked")
    if (request.args['machine'] == "Laser cutter"):
        return render_template("machine.html", laserCutter = "checked")
    if (request.args['machine'] == "another machine"):
        return render_template("machine.html", anotherMachine = "checked")

@app.route("/confirmation", methods=["GET","POST"])
def confirmation():
    print(request.args["machineName"]== "3D printer")
    print("HELLO" + str(dict[request.args["machineName"]]))
    try:
        int(request.args["time"])
        if (dict[request.args["machineName"]] == 0):
            dict[request.args["machineName"]] = int(request.args["time"])
        else:
            return render_template("waitlist.html", machineName = request.args["machineName"])
        print(dict[request.args["machineName"]])

    except:
        if (request.args['machineName'] == "3D printer"):
            return render_template("machine.html", printer = "checked")
        if (request.args['machineName'] == "Laser cutter"):
            return render_template("machine.html", laserCutter = "checked")
        if (request.args['machineName'] == "another machine"):
            return render_template("machine.html", anotherMachine = "checked")
        return render_template("machine.html")
    return render_template("confirmation.html")
    print(type(request.args["time"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("index"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # POST request: handle the form response and redirect
        username = request.form.get("name", default="")
        password = request.form.get("password", default="")
        password2 = request.form.get("password2", default="")

        error = None

        if password != password2:
            print("bad")
            error = "Error: Passwords Must Match"
        
        if error:
            return render_template("register.html", error=error)
        
        if user_exists(username):
            error = "Username already in use"
    
        if error:
            return render_template("register.html", error=error)
        else:
            create_user(username, password, "not admin")
            print(username)
            print(password)
            return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    # if "username" in session:
    #     return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("name", default = "")
        password = request.form.get("password", default="")

        if not user_exists(username):
            error = "Username does not exist"
            return render_template('login.html', error=error)
        
        else:
            if not verify_user(username, password):
                error = "Incorrect Password"
                return render_template('login.html', error=error)
            else:
                session['username'] = username
                return redirect(url_for("index"))






# @app.route("/waitlistConfirmation", methods=["GET","POST"])
# def waitlistConfirmation():
    

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
