import sys, threading, time, datetime, random, json, os, pymongo
# import RPi.GPIO as GPIO
from queue import Queue
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient


'''
Global Data - Queue
'''

load_dotenv()


data_channel = os.environ.get('DATA_CHANNEL')
history_channel = os.environ.get('PUBNUB_PUBLISH_KEY')

def setup_pubnub():
	pnconfig = PNConfiguration()
	pnconfig.publish_key = os.environ.get('PUBNUB_PUBLISH_KEY')
	pnconfig.subscribe_key = os.environ.get('PUBNUB_SUBSCRIBE_KEY')
	pnconfig.user_id = os.environ.get('PUBNUB_USER_ID')

	pubnub = PubNub(pnconfig)
	return pubnub

pubnub = setup_pubnub()
'''
Client Listener Thread
'''
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
        print("Received Historical Data Request: " + message.message)
		
        
			
pubnub.add_listener(MySubscribeCallback())

def publish(channel, message):
    pubnub.publish().channel(channel).message(message).pn_async(my_publish_callback)		


class ClientListenerThread(threading.Thread):

	def __init__(self,pnb):
		threading.Thread.__init__(self)
		self.mongoconn = MongoClient(os.environ.get('MONGODB_URI'))
		self.db = self.mongoconn.stockdb
		self.coll = self.db.stockcollection

		self.pnb = pnb

	def getLastUpdateTime(self,idxname):
		
		query = [{'$group': {'_id': '$name', 'maxValue': {'$max': '$time'}}}]

		result = self.coll.aggregate(query)

		for entry in result:
			if (entry['_id'] == idxname):
				return entry['maxValue'] 
			
		return None

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

	#Step 1 - Initialize MongoDB & PubNub Connection
	mongoconn = MongoClient(os.environ.get('MONGODB_URI'))
	db        = mongoconn.seatdb
	coll      = db.seatcollection
	
	#Setup index on time to fetch the latest update
	coll.create_index([('time',DESCENDING)])

	
	
	#Step 2 - Check and define the metadata ( index names )
	metaDataInit(coll)

	#Step 3 - Set the parameters , max periodicity , random range
	updateTime = 10 
	numOfSeats = 40

	random.seed()

	#Step 4 - Setup the Queue and ClientListener Thread
	# clientListener = ClientListenerThread(pubnub)
	# clientListener.start()


	#Step 5 - Setup PubNub Subscription for client requests

	#Step 6 - Start the stock picking loop
	while True:


		time.sleep(updateTime)
		
		newSeatData = getUpdatedSeat(coll)

		#Step 6.3 - Update the new price in DB
		print ("New Seat Update " + str(newSeatData))
		coll.insert_one(newSeatData)

		#Step 6.4 - Publish over Pubnub , stockdata channel
		broadcastData = { 'seat_num' : newSeatData['seat_num'],
						  'type'   : newSeatData['type'],
						  'value'  : newSeatData['value'],
						  'time' : newSeatData['time'],
						}


		# pubnub.publish('stockdata',json.dumps(broadcastData))
		pubnub.publish().channel(data_channel).message(json.dumps(broadcastData)).sync()


'''
Description - Populate the index names to track and initial database
'''
def metaDataInit(coll):
	global metadataDescr

	numOfSeats = 40
	metadataDescr = [f'Seat{i}' for i in range(1, numOfSeats + 1)]
	
	for seat_num in metadataDescr:
		if coll.count_documents({'seat_num': seat_num}) == 0:
			seat = {'seat_num': seat_num, 'type': "pressure", 'value': 0, 'time': 1}
			coll.insert_one(seat)



'''
Description - This function simulates the stock index price update
			  Gets the new price details for indices based on random
			  selection

Return      - Returns the JSON formatted index name, price , delta and time
'''
def getUpdatedSeat(coll):
	#Random select the index whose seat is to be updated
	seat_num = random.choice(metadataDescr)

	currentSeat = getCurrentSeat(coll,seat_num)
	if(currentSeat == 0):
		newSeatStatus = 1
	else:
		newSeatStatus = 0
	
	print ("New Seat for " + str(seat_num) + " : " + str(newSeatStatus))

	#Get the current time of update
	updateTime = getCurrentTimeInSecs()
	#Return the new index price
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

'''
Description - This function fetches the most recent price update of 
              an index idxname 

Returns -  Last updated seat
'''


'''
Description - Get the current system time in unix timestamp format
'''
def getCurrentTimeInSecs():
	
	dtime = datetime.datetime.now()

	ans_time = time.mktime(dtime.timetuple())	

	return int(ans_time)

'''
PubNub Callback for incoming requests on global listening channel
'''
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    print("my_publish_callback")
    if not status.is_error():
        print("Queue request successfully completed : " + envelope)
    else:
        print("Error in receiving Historical Data Request : " + status)

if __name__ == '__main__':
	startSeat()
	pubnub.subscribe().channels(data_channel).execute()
	pubnub.subscribe.channels(history_channel).execute()

	
