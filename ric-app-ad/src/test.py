import pandas as pd
from influxdb import InfluxDBClient
import datetime
import time
import dateutil.parser


df = pd.read_csv('ue.csv')


client = InfluxDBClient(host='10.244.0.178', port=8086, username='admin', password='1234',ssl=True, database='RIC_Test',verify_ssl=True)
result = client.query('show measurements;')
print("Result: {0}".format(result))
#current_time = datetime.datetime.utcnow().isoformat("T")


json_body = []
for _, row in df.iterrows():
    json_body.append(  {
        "measurement": "UEReports",
        "tags": {"du-id": row['du-id']},
        "time": row['measTimeStampRf'],
        #"time": current_time,
        "fields": {
            "nrCellIdentity": row['nrCellIdentity'],
            "RRU.PrbUsedDl": row['RRU.PrbUsedDl'],
            "targetTput": row['targetTput'],
            "DRB.UEThpDl": row['DRB.UEThpDl'],
            "x": row['x'],
            "y": row['y'],
            "RF.serving.RSRP": row['RF.serving.RSRP'],
            "RF.serving.RSRQ": row['RF.serving.RSRQ'],
            "RF.serving.RSSINR": row['RF.serving.RSSINR'],
            "nbCellIdentity_0": row['nbCellIdentity_0'],
            "nbCellIdentity_1": row['nbCellIdentity_1'],
            "nbCellIdentity_2": row['nbCellIdentity_2'],
            "nbCellIdentity_3": row['nbCellIdentity_3'],
            "nbCellIdentity_4": row['nbCellIdentity_4'],
            "rsrp_nb0": row['rsrp_nb0'],
            "rsrq_nb0": row['rsrq_nb0'],
            "rssinr_nb0": row['rssinr_nb0'],
            "rsrp_nb1": row['rsrp_nb1'],
            "rsrq_nb1": row['rsrq_nb1'],
            "rssinr_nb1": row['rssinr_nb1'],
            "rsrp_nb2": row['rsrp_nb2'],
            "rsrq_nb2": row['rsrq_nb2'],
            "rssinr_nb2": row['rssinr_nb2'],
            "rsrp_nb3": row['rsrp_nb3'],
            "rsrq_nb3": row['rsrq_nb3'],
            "rssinr_nb3": row['rssinr_nb3'],
            "rsrp_nb4": row['rsrp_nb4'],
            "rsrq_nb4": row['rsrq_nb4'],
            "rssinr_nb4": row['rssinr_nb4'],
            "Viavi.UE.anomalies": row['Viavi.UE.anomalies'],
            "ue-id":row['ue-id']
        }
    })
    

client.write_points(json_body)
res=client.write_points(json_body)
print(res)
print(client.write_points(json_body))
print("success")
client.close()
