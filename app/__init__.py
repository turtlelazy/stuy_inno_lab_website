from data.users import admin_verification
from data.schedule import admin_calendar_creation
from data.schedule import calendar_exists, create_calendar, edit_calendar
from flask import Flask, render_template, request, session, redirect, url_for

import os
import smtplib
import imghdr
from dateutil import parser

import json
import time
from data.machines import *
import sendemail

from data.users import user_exists, verify_user, create_user, get_username
from os import urandom
from data.data_functions import *
from data.schedule import compile_calendar
from datetime import datetime, timedelta, time

# reset_data()

app = Flask(__name__)
debug = True
app.secret_key = urandom(32)


machineUsage =	{
  "3D-printer1": [],
  "3D-printer2": [],
  "3D-printer3": [],
  "3D-printer4": [],
  "3D-printer_Stratasys": [],
  "laser-cutter": [],
  "CNC": []
}

waitlist = {
    "3D-printer1": "no",
    "3D-printer2": "no",
    "3D-printer3": "no",
    "3D-printer4": "no",
    "3D-printer_Stratasys": "no",
    "laser-cutter": "no",
    "CNC": "no"
}

# @app.route("/", methods=["GET","POST"])
# def home():
#     return render_template("machinelist.html")


@app.route("/", methods=["GET","POST"])
def index():
    if session.get('username') is not None:

        return render_template("calendar.html", calendarSchedule=compile_calendar(),user=session['username'] )
    else:
        return render_template("homepage.html")

@app.route("/machine_list",methods=["GET","POST"])
def machine_list():
    user = session['username']
        # return render_template("profile.html", user=user)
    e = session['email']
    return render_template("machinelist.html", user=user, email=e)

@app.route("/edit_request", methods=["GET","POST"])
def edit():

    if session.get('username') is None or not admin_verification(session["email"]):
        return redirect("/")

    payload = request.get_json()
    print(payload)
    month = payload["month"]
    year = payload["year"]
    schedule = payload["schedule"]
    print(type(schedule))
    schedule = json.dumps(schedule)
    print(schedule)
    #print(payload)
    #print(schedule)
    print(calendar_exists(year,month))

    if(calendar_exists(year,month)):
        edit_calendar(year,month,schedule)
    else:
        admin_calendar_creation(year,month,schedule)
    
    return "you should not be here!"

@app.route("/calendar")
def calendar():
    if session.get('username') is None:
        return redirect("/")
    print(compile_calendar())
    return render_template("calendar.html", calendarSchedule=compile_calendar(), user=session['username'])


@app.route("/admin_calendar")
def admin_calendar():
    if session.get('username') is None or not admin_verification(session["email"]):
        return redirect("/")
    print(compile_calendar())
    return render_template("admin_calendar.html", calendarSchedule=compile_calendar(), user=session['username'])


@app.route("/machine", methods=["GET","POST"])
def machine():
    if session.get('username') is None:
        return redirect("/")
    print(session["username"])
    # print(session["email"])
    if (request.args['machineName'] == "3D-printer1"):
        return render_template("machine.html", printer1 = "checked", user = session['username'])
    if (request.args['machineName'] == "3D-printer2"):
        return render_template("machine.html", printer2 = "checked", user = session['username'])
    if (request.args['machineName'] == "3D-printer3"):
        return render_template("machine.html", printer3 = "checked", user = session['username'])
    if (request.args['machineName'] == "3D-printer4"):
        return render_template("machine.html", printer4 = "checked", user = session['username'])
    if (request.args['machineName'] == "3D-printer_Stratasys"):
        return render_template("machine.html", printer_Stratasys = "checked", user = session['username'])
    if (request.args['machineName'] == "laser-cutter"):
        return render_template("machine.html", laserCutter = "checked", user = session['username'])
    if (request.args['machineName'] == "CNC"):
        return render_template("machine.html", CNC = "checked", user = session['username'])
    

@app.route("/confirmation", methods=["GET","POST"])
def confirmation():
    if session.get('username') is None:
        return redirect("/")
    print(session["email"])
    try:
        int(request.args["time"])
    except:
        return render_template("machine.html", machineName=request.args["machineName"], user=session["username"], error="Please enter an integer number of minutes")

    try:
        if (len(machineUsage[request.args["machineName"]]) == 0):
            machineUsage[request.args["machineName"]].append(datetime.now() + timedelta(minutes = int(request.args["time"])))
            machineUsage[request.args["machineName"]].append(session['email'])

        else:
            if(machineUsage[request.args["machineName"]][1] == session["email"]):
                return render_template("machine.html", machineName = request.args["machineName"], user = session["username"], error = "You have already signed on to use this machine")
            else:
                return render_template("waitlist.html", machineName = request.args["machineName"], user = session["username"])

        # print("HELLO" + str(machineUsage[request.args["machineName"]][0]))
        # try:
        #     int(request.args["time"])
        #     if (len(machineUsage[request.args["machineName"]]) == 0):
        #         machineUsage[request.args["machineName"]].append(int(request.args["time"]))
        #         machineUsage[request.args["machineName"]].append(session['email'])
        #         print(datetime.now().time())
        #         print(datetime.now().time() + timedelta(minutes=10))
        #     else:
        #         if(machineUsage[request.args["machineName"]][1] == session["email"]):
        #             return render_template("machine.html", machineName = request.args["machineName"], user = session["username"], error = "You have already signed on to use this machine")
        #         else:
        #             return render_template("waitlist.html", machineName = request.args["machineName"], user = session["username"])
        #
        #
        # except:
        #     if (request.args['machineName'] == "3D-printer1"):
        #         return render_template("machine.html", printer1 = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "3D-printer2"):
        #         return render_template("machine.html", printer2 = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "3D-printer3"):
        #         return render_template("machine.html", printer3 = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "3D-printer4"):
        #         return render_template("machine.html", printer4 = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "3D-printer_Stratasys"):
        #         return render_template("machine.html", printer_Stratasys = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "laser-cutter"):
        #         return render_template("machine.html", laserCutter = "checked", user = session["username"], error = "The input is not a valid integer")
        #     if (request.args['machineName'] == "CNC"):
        #         return render_template("machine.html", CNC = "checked", user = session["username"], error = "The input is not a valid integer")
        #     return render_template("machine.html")
        print(session["username"])
        print(request.args['machineName'])
        print(machineUsage[request.args["machineName"]][0])
        # print(request.args['time'])
        new_reservations(session["username"], request.args['machineName'], machineUsage[request.args["machineName"]][0])
        return render_template("confirmation.html")
    except(Exception):
            return render_template("error.html", message="confrimation error")

@app.route("/register", methods=["GET", "POST"])
def register():
    # if "username" in session:
    #     return redirect(url_for("machineli"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # POST request: handle the form response and redirect
        email = request.form.get("email", default="")
        username = request.form.get("name", default="")
        password = request.form.get("password", default="")
        password2 = request.form.get("password2", default="")

        error = None

        if password != password2:
            print("bad")
            error = "Error: Passwords Must Match"

        if error:
            print("bad")
            return render_template("register.html", error=error)

        if user_exists(email):
            error = "Email already in use"

        if error:
            print("bad")
            return render_template("register.html", error=error)
        else:
            create_user(email, username, password, "not admin")
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
        email = request.form.get("email", default = "")
        password = request.form.get("password", default="")
        # username = get_username(email)

        if not user_exists(email):
            error = "Email does not exist"
            return render_template('login.html', error=error)

        else:
            if not verify_user(email, password):
                error = "Incorrect Password"
                return render_template('login.html', error=error)
            else:
                username = get_username(email)
                session['username'] = username
                session['email'] = email
                return redirect(url_for("index"))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if "username" in session:
        session["username"] = None
    return redirect(url_for("index"))



# @app.route("/waitlistConfirmation", methods=["GET","POST"])
# def waitlistConfirmation():

@app.route("/waitlistConfirmation", methods=["GET","POST"])
def waitlistConfirmation():
    if session.get('username') is None:
        return redirect("/")
    try:
        if(request.args["submit"]=="yes"):
            if (waitlist[request.args["machineName"]] == "no"):
                if (machineUsage[request.args["machineName"]][0]-datetime.now()> timedelta(seconds = 1)):
                    sendemail.send(session["email"], "The " + request.args["machineName"] + " will be available in "+ str(round((machineUsage[request.args["machineName"]][0] - datetime.now()).total_seconds() / 60))+ " minutes"
                    )
                    waitlist[request.args["machineName"]] = session["email"]
                else:
                    sendemail.send(session["email"], "The " + request.args["machineName"] + " will be available soon")
                    waitlist[request.args["machineName"]] = session["email"]
            else:
                return render_template("fail.html",error="There is already someone on the waitlist. Please try again later.")
        else:
            return render_template("machinelist.html")
        return render_template("waitlistConfirmation.html")
    except(Exception):
            return render_template("error.html", message="waitlist confirmation error")
    # # try:
    #     msg = Message(subject='Test Email', sender='ftc789project@gmail.com', recipients=['22shriya.a@gmail.com'])
    #     msg.body = 'This is a test email.'
    #     mail.send(msg)
    #     # sendemail.send(request.args["waitlist"])
    #     return render_template("waitlistConfirmation.html")
    # # except:
    # #     return render_template("fail.html")

@app.route("/signOutList", methods=["GET","POST"])
def signOutList():
    if session.get('username') is None:
        return redirect("/")

    if (request.args['machineName'] == "3D-printer1"):
        return render_template("signOut.html", printer1="checked", user=session['username'])
    if (request.args['machineName'] == "3D-printer2"):
        return render_template("signOut.html", printer2="checked", user=session['username'])
    if (request.args['machineName'] == "3D-printer3"):
        return render_template("signOut.html", printer3="checked", user=session['username'])
    if (request.args['machineName'] == "3D-printer4"):
        return render_template("signOut.html", printer4="checked", user=session['username'])
    if (request.args['machineName'] == "3D-printer_Stratasys"):
        return render_template("signOut.html", printer_Stratasys="checked", user=session['username'])
    if (request.args['machineName'] == "laser-cutter"):
        return render_template("signOut.html", laserCutter="checked", user=session['username'])
    if (request.args['machineName'] == "CNC"):
        return render_template("signOut.html", CNC="checked", user=session['username'])
    return render_template("signOut.html")

@app.route("/signOut", methods=["GET","POST"])
def signOut():
    if session.get('username') is None:
        return redirect("/")

    try:
        if (len(machineUsage[request.args["machineName"]]) == 0):
            id = get_latest(request.args['machineName'])
            usage = get_use(id)
            if usage == 1:
                end_reservations(request.args['machineName'])
                return redirect(url_for("reservations"))
            return render_template("fail.html",error="This machine is not in use. You can't sign out from a machine not in use.")

        if (machineUsage[request.args["machineName"]][1] != session["email"]):
            return render_template(
                "fail.html", error="You can't sign out from a machine you are not using.")

        machineUsage[request.args["machineName"]] = []
        if(waitlist[request.args["machineName"]] != "no"):
            sendemail.send(waitlist[request.args["machineName"]], "You may use the " + request.args["machineName"] + " now")
            waitlist[request.args["machineName"]] = "no"
        print("ending")
        print(session["username"])
        print(request.args['machineName'])
        end_reservations(request.args['machineName'])
        return redirect("/machine")
    except:
        return render_template("fail.html",error="Please try signing in and signing out of your account")

@app.route("/reservation", methods=["GET","POST"])
def reservation():
    try:
        if session.get('username') is None:
            return redirect("/")

        # end_reservations("3D-printer1")
        # end_reservations("laser-cutter")
        laser = machine_column("laser-cutter")
        print(laser[1])
        if laser[1] != '':
            lt = str(round((datetime.fromisoformat(laser[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            laser[1] = lt

        p1 = machine_column("3D-printer1")
        if p1[1] != '':
            p1t = str(round((datetime.fromisoformat(p1[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            p1[1] = p1t
        
        p2 = machine_column("3D-printer2")
        if p2[1] != '':
            p2t = str(round((datetime.fromisoformat(p2[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            p2[1] = p2t
        
        p3 = machine_column("3D-printer3")
        if p3[1] != '':
            p3t = str(round((datetime.fromisoformat(p3[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            p3[1] = p3t

        strat = machine_column("3D-printer_Stratasys")
        if strat[1] != '':
            st = str(round((datetime.fromisoformat(strat[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            strat[1] = st
        
        cnc = machine_column("CNC")
        if cnc[1] != '':
            cnct = str(round((datetime.fromisoformat(cnc[1]) - datetime.now()).total_seconds() / 60)) + "minutes"
            cnc[1] = cnct
        return render_template("reservation.html", laser = laser, p1 = p1, p2 = p2, p3 = p3, strat = strat, cnc = cnc)
    except(Exception):
        return render_template("error.html", message="reservation error")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    
