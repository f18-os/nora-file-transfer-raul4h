# How to run 
In order to run this lab you need either two command lines or to run the server in the background, if there is two command lines the following commands will run the program
* python3 framedThreadServer.py
* python3 framedThreadClient.py

If there is only one command line the following will run the program
* python3 framedThreadServer &
* python3 framedThreadClient.py

# Explanation

The way Mutex is used in this lab is that the client will not send more information until one thread has done sending all of its data, this way, the files will not get jumbled because they will send information one at a time by using Locks and begin sending more once one thread has finished.
