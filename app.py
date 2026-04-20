from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime as dt
import json
FILE_PATH = "Flask_workout_tracker/data.json"
app = Flask(__name__)
def open_file():
    """Opens the file and returns the json contents"""
    with open(file = FILE_PATH,mode="r") as file:
        return json.load(file)

def write_file(data):
    """Writes the data to the file"""
    with open(file = FILE_PATH, mode = "w") as file:
        json.dump(data,file,indent=4)


file = open_file()
# Sort via dates
file = sorted(file, key=lambda x: dt.strptime(x["date"], "%d/%m/%Y"),reverse=True)

    
@app.route("/")
def home(): 
    return render_template(
        "index.html",
        file = file
        )

@app.route("/new_workout")
def new_workout():
    """Command to show the adding new workout html file"""
    workout = None
    return render_template("new_workout.html",workout = workout)


@app.route("/add_workout", methods=["POST"])
def add_workout():
    """Adds the workout and saves it to the file"""
    training = request.form.get("training")
    date = request.form.get("date")
    duration = request.form.get("duration")
    new_workout_entry = {"date":date,"exercise":training,"duration":duration}
    if training and date and duration:
        dt_object = dt.strptime(date,"%Y-%m-%d")
        date = dt.strftime(dt_object,"%d/%m/%Y")
        new_workout_entry["date"] = date
        file.append(new_workout_entry)
        write_file(file)
        return redirect(url_for("home"))
    else:
        return render_template("new_workout.html",workout = new_workout_entry)

@app.route("/delete_workout", methods=["POST"])
def delete_workout():
    """Command for deleting the chosen workout"""
    workout_id = int(request.form.get("workout_index"))
    file.remove(file[workout_id])
    write_file(file)
    return redirect(url_for("home"))

@app.route("/edit_workout", methods=["POST"])
def edit_workout():
    """Command for editing the chosen workout"""
    workout_id = int(request.form.get("workout_index"))
    workout = file[workout_id]
    workout["date"] = str(dt.strptime(workout["date"],"%d/%m/%Y").date())
    
    file.remove(file[workout_id])
    return render_template("new_workout.html",workout = workout)
    
if __name__ == "__main__":
    app.run(debug=True)
    