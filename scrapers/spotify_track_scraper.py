import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import time
import json
from tqdm import tqdm

# We had split the data scraping task among the four members of our team
numPartitions=4
index=0 #index values: 0, 1, 2, 3
apiBatchSize=50
partialRestart=True
trackList = json.load(open("tracks_list_10k_1k_26_90","r"))

partitionSize=int(len(trackList)/numPartitions)
start=index*partitionSize
if partialRestart:
	start = index*partitionSize+1 #replace this with the value you want to start from
end=(index+1)*partitionSize
if index==numPartitions-1:
	end=len(trackList)

listTracks=trackList[start:end]

print(start,end,len(listTracks))
#put your own SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_CLIENT_ID']='<SPOTIPY_CLIENT_ID>'
os.environ['SPOTIPY_CLIENT_SECRET']='<SPOTIPY_CLIENT_SECRET>'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

trackDetails={}
if partialRestart:
	trackDetails = pickle.load(open("trackDetails"+str(index)+".pkl","rb"))
	print("Previous dict has "+str(len(trackDetails))+" entries")

progress_bar = tqdm(total = len(listTracks), desc = "Progress", ncols = 100)
for i in range(0, len(listTracks), apiBatchSize):
	ids=listTracks[i:i+apiBatchSize]
	temp=sp.tracks(ids)["tracks"]
	for j in range(apiBatchSize):
		trackDetails[ids[j]]=temp[j]
	time.sleep(10)
	albumFile=open("trackDetails"+str(index)+".pkl","wb")
	pickle.dump(trackDetails, albumFile)
	progress_bar.update(apiBatchSize)
progress_bar.close()
print("Complete!")