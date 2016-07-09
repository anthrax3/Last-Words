
import json
import threading
#import urllib2

from multiprocessing import Pool
from urllib.request import urlopen

import ssl
import http.client

import codecs

"""
Global variables
"""

decoder = codecs.getreader("utf-8")
# To prevent SSL failure after too many calls.
context = ssl._create_unverified_context()
lock = threading.Lock()
modFile = open("modComments.txt", "w")
modData = json.load(decoder(urlopen("https://hacker-news.firebaseio.com/v0/user/dang.json", context=context)))
submitIds = modData["submitted"]

submitIds = [10551997, 7867166, 12041458, 12059888]

print(len(submitIds))

for id in submitIds:
  if type(id) != type(3):
    print(type(id))

def isBanningComment(data, id):
  print(id)
  return data is not None \
    and "type" in data \
    and data["type"] == "comment" \
    and "text" in data \
    and "banned" in data["text"] \
    and "parent" in data

def foo(id):
  modComment = ""
  try:
    modComment = json.load(decoder(urlopen("https://hacker-news.firebaseio.com/v0/item/"
      + str(id)
      + ".json",
      context=context)))
  except http.client.BadStatusLine:
    print("***********************************************")
    print("failed: " + str(id))
    print("***********************************************")
    return 0

  if isBanningComment(modComment, id):

    lock.acquire()
    #next check if user is banned
    print("id: " + str(modComment['id']))

    modCommentText = modComment["text"]
    #modCommentText = modCommentText.encode('utf-8')

    #print("banned text: " + modCommentText)
    modFile.write(modCommentText)
    modFile.write("\n\n")
    lock.release()
    return 1
  else:
    return 0

pool = Pool(8)
results = pool.map(foo, submitIds)

pool.close()
pool.join()

modFile.close()
print("Finished")
print(sum(results))

