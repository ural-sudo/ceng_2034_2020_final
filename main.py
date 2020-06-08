#*
#* Ahmet Erçin URAL
#* 160709046
#* 

import os # importing os library
import requests # importing request
import uuid # importing uuid for create a unique ıd
import hashlib 
import multiprocessing #it is necessery for multiprocessing
from itertools import product # In multiprocess you need to send 2 arguments to the pool function.

def generateHash(image):
    t = open(image, "rb")
    return (image, hashlib.md5(t.read()).hexdigest())
    


 

#* h[0], fileHashes[0] => hash number
#* h[1], fileHashes[1] => file name

def findDuplicate(h, fileHashes):
    if h[0] != fileHashes[0]:
        if h[1] == fileHashes[1]:
            return (h[0], fileHashes[0])
#*
#* If the user gave a 'file_name' as a parameter, use it, otherwise we 
#* 
#* create a unique 'file_name' using uuid.uuid4
#*
def fileDownload(url, file_name=None):
    if (file_name != None):
        file_name = file_name
    else:
        file_name = str(uuid.uuid4())

    res = requests.get(url, allow_redirects=True)

    file = open(file_name, "wb")
    file.write(res.content)

def multiprocessChildProcess():
    # we create childProcess
    childProcess = os.fork() 

    # If the child process is greater than 0,
    # the parent is continuing and we wait.
    if childProcess > 0:
        os.wait()

# If the child process is equal to 0, the child process is now in progress.
    elif childProcess == 0:

        multiprocess = multiprocessing.Pool()

        request_urls = [
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

        for i in request_urls:
            fileDownload(i)

        currentDirectory = os.listdir()

        fileHashes = []
        for h in currentDirectory:
            fileHashed = generateHash(h)
            fileHashes.append(fileHashed)

        # We can assign two parameters to the multiprocess pool we created using Starmap.       
        duplicateWithDuplicates = multiprocess.starmap(findDuplicate, product(fileHashes, fileHashes))

        # There are duplicate structures among duplicate checked files, we check and eliminate them.
        onlyDuplicate = []
        for i in duplicateWithDuplicates:
            if i != None:
                if i[0] != i[1] and i[1]:
                    if i[0] not in onlyDuplicate:
                        onlyDuplicate.append(i[0])
                    elif i[1] not in onlyDuplicate:
                        onlyDuplicate.append(i[1])

        # Printing duplicate images...
        for i in onlyDuplicate:
            print(i)

if __name__ == '__main__':
    multiprocessChildProcess()



