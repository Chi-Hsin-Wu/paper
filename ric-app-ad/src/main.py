# ==================================================================================
#  Copyright (c) 2020 HCL Technologies Limited.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ==================================================================================

import json
import scapy
import socket
import os
import time
import pandas as pd
import schedule
from ricxappframe.xapp_frame import Xapp, rmr
from ricxappframe.xapp_sdl import SDLWrapper
from mdclogpy import Logger
from ad_model import modelling, CAUSE
from ad_train import ModelTraining
from database import DATABASE, DUMMY

db = None
cp = None
threshold = None
sdl = SDLWrapper(use_fake_sdl=True)

logger = Logger(name=__name__)


def entry(self):
    """  If ML model is not present in the path, It will trigger training module to train the model.
      Calls predict function every 10 millisecond(for now as we are using simulated data).
    """
    connectdb()
    train_model()
    load_model()
    schedule.every(0.5).seconds.do(predict, self)
    while True:
        schedule.run_pending()


def load_model():
    global md
    global cp
    global threshold
    md = modelling()
    cp = CAUSE()
    threshold = 70
    logger.info("throughput threshold parameter is set as {}% (default)".format(threshold))


def train_model():
    if not os.path.isfile('src/model'):
        mt = ModelTraining(db)
        mt.train()

def send_tcp_packet(dst_ip,dst_port,message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((dst_ip,dst_port))
        print("Connect TS with TCP")
        while True:
                s.sendall(message.encode())
                time.sleep(2)
                response=s.recv(8192)
                print(f"Received and sent back: {response.decode()}")


def predict(self):
    """Read the latest ue sample from influxDB and detects if that is anomalous or normal..
      Send the UEID, DUID, Degradation type and timestamp for the anomalous samples to Traffic Steering (rmr with the message type as 30003)
      Get the acknowledgement of sent message from the traffic steering.
    """
    db.read_data()
    val = None
    if db.data is not None:
        if set(md.num).issubset(db.data.columns):
            db.data = db.data.dropna(axis=0)
            if len(db.data) > 0:
                val = predict_anomaly(self, db.data)
        else:
            logger.warning("Parameters does not match with of training data")
    else:
        logger.warning("No data in last 1 second")
        time.sleep(1)
    if (val is not None) and (len(val) > 2):
        msg_to_ts(self, val)
        print(val)

def predict_anomaly(self, df):
    """ calls ad_predict to detect if given sample is normal or anomalous
    find out the degradation type if sample is anomalous
    write given sample along with predicted label to AD measurement

    Parameter
    ........
    ue: array or dataframe

    Return
    ......
    val: anomalus sample info(UEID, DUID, TimeStamp, Degradation type)
    """
    df['Anomaly'] = md.predict(df)
    df.loc[:, 'Degradation'] = ''
    val = None
    if 1 in df.Anomaly.unique():
        df.loc[:, ['Anomaly', 'Degradation']] = cp.cause(df, db, threshold)
        df_a = df.loc[df['Anomaly'] == 1].copy()
        if len(df_a) > 0:
            df_a['time'] = df_a.index
            cols = [db.ue, 'time', 'Degradation']
            # rmr send 30003(TS_ANOMALY_UPDATE), should trigger registered callback
            result = json.loads(df_a.loc[:, cols].to_json(orient='records'))
            val = json.dumps(result).encode()
    df.loc[:, 'RRU.PrbUsedDl'] = df['RRU.PrbUsedDl'].astype('float')
    df.index = pd.date_range(start=df.index[0], periods=len(df), freq='1ms')
    db.write_anomaly(df)
    return val


def msg_to_ts(self, val):
    # send message from ad to ts
    logger.debug("Sending Anomalous UE to TS")
    success = self.rmr_send(val, 30003,1000)
    print(success)
    if success:
        logger.info(" Message to TS: message sent Successfully")
        # rmr receive to get the acknowledgement message from the traffic steering.
    else:
        send_tcp_packet("10.244.0.166",4560,val)
        logger.info("Message to TS via TCP")


    for summary, sbuf in self.rmr_get_messages():
        if sbuf.contents.mtype == 30004:
            logger.info("Received acknowldgement from TS (TS_ANOMALY_ACK): {}".format(summary))
        
        self.rmr_free(sbuf)


def connectdb(thread=False):
    # Create a connection to InfluxDB if thread=True, otherwise it will create a dummy data instance
    global db
    if thread:
        db = DUMMY()
    else:
        db = DATABASE()
    success = False
    while not success:
        success = db.connect()



def start(thread=False):
    # Initiates xapp api and runs the entry() using xapp.run()
    xapp = Xapp(entrypoint=entry, rmr_port=4560,rmr_wait_for_ready=False, use_fake_sdl=False)
    logger.debug("AD xApp starting")
    xapp.run()
