import time 
import os 
import json
from mdclogpy import Logger
from ricxappframe.xapp_frame import Xapp, rmr
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
import random
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import RequestException, ConnectionError



logger = Logger(name=__name__)

def start(thread=False):
    xapp = Xapp(entrypoint=entry, rmr_port=4560,rmr_wait_for_ready=False, use_fake_sdl=False)
    logger.debug("Fake QP xApp starting")
    xapp.run()

def __init__(self, dbname='UEData', user='admin', password='1234', host="10.244.0.172", port='8086', path='', ssl=False):
        self.data = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.path = path
        self.ssl = ssl
        self.dbname = dbname
        self.client = None

def read_data(self):
    self.data = None
    query = 'select "ue-id","nrCellIdentity","nbCellIdentity_0","nbCellIdentity_1","nbCellIdentity_2","nbCellIdentity_3","nbCellIdentity_4" from "liveUE" limit 10'
    result = self.query(query)
    if result is not None:
        self.data=result
        print(result)
    
def connect(self):
    if self.client is not None:
        self.client.close()

    try:
        self.client = DataFrameClient(self.host, port=self.port, username=self.user, password=self.password, path=self.path, ssl=self.ssl, database=self.dbname, verify_ssl=self.ssl)
        version = self.client.request('ping', expected_response_code=204).headers['X-Influxdb-Version']
        logger.info("Connected to Influx Database, InfluxDB version : {}".format(version))
        return True

    except (RequestException, InfluxDBClientError, InfluxDBServerError, ConnectionError):
        logger.error("Failed to establish a new connection with InflulxDB, Please check your url/hostname")
        time.sleep(10)

def set_ue_prediction_set():   
    print("Attack Cell:"+str(5))
    pre_msg={
        "3":{
            "5": [random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
        },
        "7":{
           "5": [random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
        },
        "8":{
            "5": [random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "10":{
            "5": [random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "9":{
            "5":[random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "4":{
            "5":[random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "6":{
            "5":[random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "1":{
            "5":[random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            },
        "5":{
            "5":[random.randint(1000000, 2500000),random.randint(1000000, 2500000)]
            }
    }
    print(json.dumps(pre_msg, indent=4))
    return pre_msg

def send_prediction(self):
    while True:
        message=set_ue_prediction_set()
        print(json.dumps(message,indent=4))
        success=self.rmr_send(message,30002,10000)
        print(success)
        if success:
            logger.info("Sending Prediction to TS Successfully")
            time.sleep(10)
            self.rmr_free(self.rmr_get_messages.sbuf)



def entry(self):
    __init__(self)
    connect(self)
    read_data(self)



if __name__ == '__main__':
    start()



          