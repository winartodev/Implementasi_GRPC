import logging
import grpc
import numpy as np
from concurrent import futures

from grpc_module import dataservice_pb2, dataservice_pb2_grpc
from ml_model.decisiontreeclassifiermodel import predict_playing_golf

# combile all the result's  of the client request
def concat_from_request(outlook, temprature, humidity, windy):
    # return result from client selected request to array
    switcher_outlook = {
        'outlook_sunny': np.array([0, 0, 1]),
        'outlook_overcast': np.array([1, 0, 0]),
        'outlook_rainy': np.array([0, 1, 0])
    }

    switcher_temprature = {
        'temprature_cool': np.array([1, 0, 0]),
        'temprature_hot': np.array([0, 1, 0]),
        'temprature_mild': np.array([0, 0, 1])
    }

    switcher_humidity = {
        'humidity_high': np.array([1, 0]),
        'humidity_normal': np.array([0, 1])
    }

    switcher_windy = {
        'windy_true': np.array([1, 0]),
        'windy_false': np.array([0, 1])
    }

    # save all selected array to 4 variable outlook, temprature, humidity, windy
    outlook_value = switcher_outlook.get(outlook, np.array([0,0,0]))
    temprature_value = switcher_temprature.get(temprature, np.array([0, 0, 0]))
    humidity_value = switcher_humidity.get(humidity, np.array([0, 0]))
    windy_value = switcher_windy.get(windy, np.array([0, 0]))

    # concate all 4 variables into 1 array
    concatenate = np.concatenate((outlook_value, temprature_value, humidity_value, windy_value))

    return concatenate

# DataService class to handle client requests
class DataService(dataservice_pb2_grpc.DataServiceServicer):
    def PredictPlayingGolf(self, request, context):
        # concat from client selected request
        concat = concat_from_request(request.outlook, request.temprature,
                                     request.humidity, request.windy)
        # call predict_paying_method to predict the result from concat variable (concat result is 1D array)
        result = predict_playing_golf(concat)

        # handle client with outcomes (the prediction)
        return dataservice_pb2.DataServiceRespond(result=result)

# serve function to initialize grpc 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dataservice_pb2_grpc.add_DataServiceServicer_to_server(DataService(), server)
    port = server.add_insecure_port('192.168.56.1:5001')
    print(f"Port {str(port)} is Ready")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()