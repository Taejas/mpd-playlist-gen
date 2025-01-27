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
apiBatchSize=20
albumList = json.load(open("albums_list_10k_1k_26_90","r"))

partitionSize=int(len(albumList)/numPartitions)
start=index*partitionSize
end=(index+1)*partitionSize
if index==numPartitions-1:
	end=len(albumList)

listAlbums=albumList[start:end]
print(start,end,len(listAlbums))

#put your own SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_CLIENT_ID']='<SPOTIPY_CLIENT_ID>'
os.environ['SPOTIPY_CLIENT_SECRET']='<SPOTIPY_CLIENT_SECRET>'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

albumDetails={}
progress_bar = tqdm(total = len(listAlbums), desc = "Progress", ncols = 100)
for i in range(0, len(listAlbums), apiBatchSize):
	ids=listAlbums[i:i+apiBatchSize]
	temp=sp.albums(ids)["albums"]
	for j in range(apiBatchSize):
		if temp[j]==None:
			print("None encountered for ", ids[j])
			continue
		albumDetails[ids[j]]=temp[j]
	time.sleep(10)
	albumFile=open("albumDetails"+str(index)+".pkl","wb")
	pickle.dump(albumDetails, albumFile)
	progress_bar.update(apiBatchSize)
progress_bar.close()
print("Complete!")
