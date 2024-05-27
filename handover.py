from influxdb import InfluxDBClient
import pandas as pd

host="10.244.0.108"
port=8086
username="admin"
password="1234"
dbname="UEData"
measurement="liveUE"

client=InfluxDBClient(host=host,port=port,username=username,password=password,database=dbname)
query = f'SELECT * FROM "{measurement}" WHERE time > now() - 1h'
result=client.query(query)

data = []
for point in result.get_points():
    data.append(point)

print(f"Number of points retrieved: {len(data)}")
df=pd.DataFrame(data)
print(df.columns)
df['time']=pd.to_datetime(df['time'])

#Handover detector

df.sort_values(by=["ue-id","time"],inplace=True)
handover_events=[]

for i in range(1,len(df)):
    if df.iloc[i]["ue-id"]==df.iloc[i-1]["ue-id"] and df.iloc[i]["nrCellIdentity"]!=df.iloc[i-1]["nrCellIdentity"]:
        handover_events.append({

            "time":df.iloc[i]["time"],
            "ue-id":df.iloc[i]["ue-id"],
            "Source_gNB":df.iloc[i-1]["nrCellIdentity"],
            "Target_gNB":df.iloc[i]["nrCellIdentity"],
            "Serving_gNB_UE_Throughput":df.iloc[i-1]["DRB.UEThpDl"],
            "Target_gNB_UE_Throughput":df.iloc[i]["DRB.UEThpDl"]
        })

handover_measurement="handover_events"
json_body=[
{
    "measurement":handover_measurement,
    "tags":{
        "ue-id": event["ue-id"]
    },
    "time": event["time"],
    "fields": {
        "Source_gNB":event["Source_gNB"],
        "Target_gNB":event["Target_gNB"],
        "Serving_gNB_UE_Throughput":event["Serving_gNB_UE_Throughput"],
        "Target_gNB_UE_Throughput":event["Target_gNB_UE_Throughput"]
    }

}
for event in handover_events
]

client.write_points(json_body)
client.close()
#print(handover_events)
print("Handover Event Has been Detected")




