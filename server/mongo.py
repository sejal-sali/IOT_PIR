import sys, threading, time, datetime, random, json, os
from flask import Flask, render_template
import RPi.GPIO as GPIO
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient

app = Flask(__name__)
alive = 0
data = {}

PIR_pin = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)

load_dotenv()

seat_channel = os.environ.get('SEAT_CHANNEL')
motion_channel = os.environ.get('MOTION_CHANNEL')

def setup_pubnub():
	pnconfig = PNConfiguration()
	pnconfig.publish_key = os.environ.get('PUBNUB_PUBLISH_KEY')
	pnconfig.subscribe_key = os.environ.get('PUBNUB_SUBSCRIBE_KEY')
	pnconfig.user_id = os.environ.get('PUBNUB_USER_ID')

	pubnub = PubNub(pnconfig)
	return pubnub

pubnub = setup_pubnub()

@app.route("/")
def index():
   return render_template("index.html")


@app.route("/keep_alive")
def keep_alive():
   global alive, data
   alive += 1
   keep_alive_count = str(alive)
   data['keep_alive'] = keep_alive_count
   parsed_json = json.dumps(data)
   return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
   global data
   if name == "buzzer":
       if action == "on":
           data["alarm"] = True
       elif action == "off":
           data["alarm"] = False
   return str("Ok")

class MySubscribeCallback(SubscribeCallback):
    def presense(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

def message(self, pubnub, message):
	print(message.message)

		
        
			
pubnub.add_listener(MySubscribeCallback())

def motion_detection():
    print("Starting motion detection loop")
    data["alarm"] = False
    trigger = False
    while True:
        if GPIO.input(PIR_pin):
            data['motion'] = 1
            # beep(4)
            publish(motion_channel, {"motion": "Motion Detected"})
            trigger = True
        elif trigger:
            data['motion'] = 0
            publish(motion_channel, {"motion": "No Motion Detected"})
            trigger = False
        # if data["alarm"]:
        #     beep(2)
        time.sleep(2)

def publish(channel, message):
    pubnub.publish().channel(channel).message(message).pn_async(my_publish_callback)		



'''
Description - Main server loop

Data will be stored in the following JSON format

	{
		"seat_num" 	 : 1  ,
		"type"   : "pressure"  ,
		"value"  : 0 ,
		"time"   : 1040241123
	}

'''
def startSeat():

	mongoconn = MongoClient(os.environ.get('MONGODB_URI'))
	db        = mongoconn.seatdb
	coll      = db.seatcollection
	
	coll.create_index([('time',DESCENDING)])

	seatsDataInit(coll)

	updateTime = 5 
	random.seed()

	while True:

		time.sleep(updateTime)
		
		newSeatData = getUpdatedSeat(coll)
		print ("New Seat Update " + str(newSeatData))
		coll.insert_one(newSeatData)
		MongoClient(os.environ.get('MONGODB_URI')).seatdb.motioncollection.insert_one({
			"type": "motion",
			"value": data['motion'],
			"time": int(time.time())
		})
		

		seatData = { 'seat_num' : newSeatData['seat_num'],
						  'type'   : newSeatData['type'],
						  'value'  : newSeatData['value'],
						  'time' : newSeatData['time'],
						}

		pubnub.publish().channel(seat_channel).message(json.dumps(seatData)).sync()


def seatsDataInit(coll):
	global seatdataDescr

	numOfSeats = 40
	seatdataDescr = [i for i in range(1, numOfSeats + 1)]
	for seat_num in seatdataDescr:
		count = coll.count_documents({'seat_num': seat_num})
		if count == 0:
			seat = {'seat_num': int(seat_num), 'type': "pressure", 'value': 0, 'time': 1705252950}
			coll.insert_one(seat)
	print("Seats initialization complete")




def getUpdatedSeat(coll):
	# seat_num = random.choice(seatdataDescr)
	seat_num = 2

	currentSeat = getCurrentSeat(coll,seat_num)
	if(currentSeat == 0):
		newSeatStatus = 1
	else:
		newSeatStatus = 0
	
	updateTime = int(time.time())
	return {
		"seat_num" 	 : seat_num  ,
		"type"   	 : "pressure"  ,
		"value"  	 : newSeatStatus ,
		"time"   	 : updateTime
	}

def getCurrentSeat(coll,seat_num):
	
	query = [{'$group': {'_id': '$seat_num', 'maxValue': {'$max': '$time'}}}]
	result = coll.aggregate(query)

	for entry in result:
		if (entry['_id'] == seat_num):
			it = coll.find({'seat_num' : seat_num, 'time' : entry['maxValue'] }).limit(1)
			val =  it.next()['value']
			return val
	return None

def getCurrentTimeInSecs():
	
	dtime = datetime.datetime.now()

	ans_time = time.mktime(dtime.timetuple())	

	return int(ans_time)

'''
PubNub Callback for incoming requests on global listening channel
'''
def my_publish_callback(envelope, status):
    if not status.is_error():
        # print(envelope)
        pass
    else:
        print(status)
        

if __name__ == '__main__':
    sensorsThread = threading.Thread(target=motion_detection)
    seatsThread = threading.Thread(target=startSeat)
    
    seatsThread.start()
    sensorsThread.start()
	
    pubnub.subscribe().channels(seat_channel).execute()
    pubnub.subscribe().channels(motion_channel).execute()
    
    app.run(host="0.0.0.0", port="5000")
    

	
