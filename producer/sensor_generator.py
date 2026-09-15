import json, os, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer

servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092")
topic=os.getenv("KAFKA_TOPIC","sensors")
eps=float(os.getenv("EVENTS_PER_SECOND","2"))
p=KafkaProducer(bootstrap_servers=servers,
				value_serializer=lambda v: json.dumps(v).encode("utf-8"))
sensors=[("sensor-001","Buda","temperature"),("sensor-002","Pest","temperature"),
		 ("sensor-003","Buda","traffic"),("sensor-004","Pest","air_quality")]
while True:
	sid,loc,typ=random.choice(sensors)
	if typ=="temperature": value=round(random.gauss(24,5),2)
	elif typ=="traffic": value=random.randint(10,120)
	else: value=round(max(1,random.gauss(30,12)),2)
	event={"timestamp":datetime.now(timezone.utc).isoformat(),
		   "sensor_id":sid,"location":loc,"sensor_type":typ,"value":value}
	p.send(topic,event)
	# print(f"Topic: {topic}, event:{event}")
	p.flush()
	time.sleep(1/eps)
