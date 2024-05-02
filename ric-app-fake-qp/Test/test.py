import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime
import time
import json
import random
import dateutil.parser

client = InfluxDBClient(host='10.244.0.172', port=8086, username='admin', password='1234', database='UEData')
print("Connected to Influx Database")
query='select "ue-id","nrCellIdentity","nbCellIdentity_0","nbCellIdentity_1","nbCellIdentity_2","nbCellIdentity_3","nbCellIdentity_4" from "liveUE" limit 20'
result=client.query(query)
if result:
    points = list(result.get_points(measurement='liveUE'))
    if points:  
        data = pd.DataFrame(points)
        for index, row in data.iterrows():
            print(f"ue-id: {row['ue-id']}, nrCellIdentity: {row['nrCellIdentity']}, nbCellIdentity_0: {row['nbCellIdentity_0']}, nbCellIdentity_1: {row['nbCellIdentity_1']}, nbCellIdentity_2: {row['nbCellIdentity_2']}, nbCellIdentity_3: {row['nbCellIdentity_3']}, nbCellIdentity_4: {row['nbCellIdentity_4']}")
    
else:
    print("No data found for 'liveUE'")


#{"3":{"2": [12650, 12721],"6": [12663, 12739],"7": [12576, 12655],"2": [12649, 12697],"3": [12592, 12688]}}
#choose one neighbor cell and let it has highest UL and DL throughput
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

set_ue_prediction_set()