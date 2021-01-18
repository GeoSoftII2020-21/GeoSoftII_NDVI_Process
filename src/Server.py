from flask import Flask, request, jsonify, Response
import requests
import os
import threading
import ndvi
import xarray
import uuid
docker = False
app = Flask(__name__)


job = {"status": None, "result" : None}
#Mögliche Stati running, done, idle

@app.route("/doJob/<uuid:id>", methods=["POST"])
def doJob(id):
    dataFromPost = request.get_json()
    job["status"] = "processing"
    t = threading.Thread(target=job,args=(dataFromPost, id,))
    return Response(status=200)

@app.route("/jobStatus", methods=["GET"])
def jobStatus():
    #Todo: Status der Funktion anpassen
    return jsonify(job)


def job(dataFromPost, id):
    dataset = xarray.load_dataset("data/" + str(id) + "/" + str(dataFromPost["arguments"]["data"]["from_node"]) + ".nc")
    x = ndvi.start(dataset)
    subid = uuid.uuid1()
    x.to_netcdf("data/" + str(id) + "/" + str(subid) + ".nc")
    job["id"] = str(subid)
    job["status"] = "done"


def main():
    """
    Startet den Server. Aktuell im Debug Modus und Reagiert auf alle eingehenden Anfragen auf Port 80.
    """
    global docker
    if os.environ.get("DOCKER") == "True":
        docker = True

    if docker:
        port = 80
    else:
        port = 441
    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
