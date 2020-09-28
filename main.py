import openpyxl
import os
from multiprocessing import Process
import json

threadnumber= [0, 0, 0, 0, 0]
startrow= 1

def load_json_file(filename: str) -> dict:
    with open(filename) as file_stream:
        data = json.load(file_stream)
    return data

credentials= load_json_file('credentials.json')

id= credentials['id']
pw= credentials['pw']
list= credentials['list']

try:
    totprocess= int(credentials['multiprocess'])
except ValueError:
    totprocess= 1


wb= openpyxl.load_workbook(list, data_only= True)
ws= wb['Sheet1']

def run(url, id, pw):
    os.system(f'youtube-dl --username {id} --password {pw} {url}')

def job(processnum):

    while True:
        row = startrow + processnum + threadnumber[processnum]
        urlid = str(ws.cell(row, 2).value)

        if (urlid == 'None'):
            break
        url = f'https://vlive.tv/video/{urlid}'
        run(url, id, pw)
        print(f"==== Process {processnum} {url} ====")

        threadnumber[processnum] = threadnumber[processnum] + totprocess

procs= []

for i in range(totprocess):
    proc= Process(target= job, args= (i,),)
    print(f"========Process {i} is running========")
    proc.start()
    procs.append(proc)

for proc in procs:
    proc.join()