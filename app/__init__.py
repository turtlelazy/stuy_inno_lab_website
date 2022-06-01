from flask import Flask, render_template, request
app = Flask(__name__)

dict =	{
  "3D printer": 0,
  "Laser cutter": 0,
  "another machine": 0
}


@app.route("/", methods=["GET","POST"])
def home():
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
            return render_template("waitlist.html")
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


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
