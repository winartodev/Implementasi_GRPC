import webbrowser
from threading import Timer

from flask import Flask, render_template, request, redirect, url_for

import grpc
from grpc_module import dataservice_pb2, dataservice_pb2_grpc

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# get response value and return from string.
def status_from_result(response):
    if response == 1:
        return "Playing Golf"
    else:
        return "Don't Play Golf"

@app.route("/weather", methods=["GET", "POST"])
def weather():
    if request.method == 'POST':
        # add 4 variables to store option from client
        outlook_value = request.form["outlook"]
        temprature_value = request.form["temprature"]
        humidity_value = request.form["humidity"]
        windy_value = request.form["windy"]

        # Connecting to GRPC Server channel in port 127.0.0.1:5001
        channel = grpc.insecure_channel("192.168.56.1:5001")
        # synchronize  data from server to clinet
        stub = dataservice_pb2_grpc.DataServiceStub(channel)
        # call PredictPlayingGolf with parameter the request from the client
        response = stub.PredictPlayingGolf(dataservice_pb2.DataServiceRequest(outlook=outlook_value, temprature=temprature_value,
                                                                            humidity=humidity_value, windy=windy_value))
        # set text-success when result of response is 1 and test-danger when responde is 0
        text_style = "text-success" if response.result == 1 else "text-danger"
        
        # redirect to check_weather.html with the response from server
        return render_template('check_weather.html', result=status_from_result(response.result), style=text_style)
    else:
        return render_template('check_weather.html')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(0, open_browser).start()
      app.run(port=5000)