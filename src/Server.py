from flask import Flask, request, jsonify, Response
import requests
import os

docker = False
app = Flask(__name__)


job = {"status": None, "result" : None}
#Mögliche Stati running, done, idle

@app.route("/doJob", methods=["POST"])
def doJob():
    dataFromPost = request.get_json()
    #Todo: Funktions aufruf
    return Response(status=200)

@app.route("/jobStatus", methods=["GET"])
def jobStatus():
    #Todo: Status der Funktion anpassen
    return jsonify(job)



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
