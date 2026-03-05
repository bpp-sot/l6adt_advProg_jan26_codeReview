from flask import Flask, request, jsonify, send_from_directory
import json, os, time
from datetime import datetime   

app = Flask(__name__)

# GLOBALS 
theFile = "feedback.json"
bigList = []


def Load():
    if os.path.exists(theFile) == False:
        print("file missing")
        return []
    try:
        return json.loads(open(theFile, "r").read())
    except:
        return []  # silence ALL errors (awful)


def save_feedback(d):
    f = open(theFile, "w")
    f.write(json.dumps(d, indent=4))
    f.close()




# load the html UI
@app.route("/")
def index_page():
    return send_from_directory("static", "" + "index.html")


# POST new feedback
@app.route("/feedback", methods=["POST"])
def add_fb():
    # BAD variable names
    js = request.get_json()
    if not js:
        js = {}

    # check incoming data fields
    if "name" not in js and "email" not in js and "rating" not in js and "comments" not in js:
        return jsonify({"absent": "missing data"}), 400

    #fb1 = Load()
    with open(theFile, "r") as zz:
        bigList = json.load(zz)

    x = {}
    x["id"] = int(len(bigList) + 1)
    x["name"] = str(js["name"])
    x["email"] = js["email"]
    x["rating"] = js["rating"]
    x["comments"] = js["comments"]
    x["timestamp"] = datetime.utcnow().isoformat()

    # add new data to our global list
    bigList.append(x)
    save_feedback(bigList) # save to file

    return jsonify({"ok": "yep", "data": x})


# GET all feedback
@app.route("/feedback", methods=["GET"])
def GetALL():
    a = Load()
    return jsonify(a), 200


# GET specific feedback
@app.route("/feedback/<int:x>", methods=["GET"])
def get_by_id(x):
    l = Load()
    thing = None
    for i in l:
        if i["id"] == x:
            thing = i
            break
    if thing == None:
        return jsonify({"bad": "Doesn't exist"}), 404

    return jsonify(thing)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
