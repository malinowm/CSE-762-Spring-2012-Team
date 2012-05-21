#!/usr/local/bin/python

from pymongo import Connection
import os
import logging
from datetime import datetime
import smtplib
import string
from ftplib import FTP

#connect to mine database
HOST = '127.0.0.1'
PORT = 27017
connection = Connection(HOST, PORT)
db = connection.MINE


def postRequest(studyid, email, processed = False, queued = False):
        if not alreadyRequested(studyid):
                request = {"gse": studyid, "email": email, "datetime": datetime.now(), "processed": False, "queued": False}
                db.request.insert(request)

def alreadyRequested(studyid):
        if db.request.find({"gse":studyid}).count() > 0:
                return True
        else:
                return False

def requestProcessed(studyid):
        if db.request.find({"gse":studyid, "processed":True}).count() > 0:
                return True
        else:
                return False

def requestQueued(studyid):
        if db.request.find({"gse":studyid, "queued":True}).count() > 0:
                return True
        else:
                return False

def markRequestProcessed(studyid):
        db.request.update({"gse":studyid,}, {"$set": {"processed":True}})
        email = db.request.find({"gse":studyid}).distinct("email")
        sendEmail(email, studyid)

def markRequestQueued(studyid):
        db.request.update({"gse":studyid,}, {"$set": {"queued":True}})

def getStudyList():
        return db.request.find().distinct("gse")

def isValidNumber(studyid):
    ftp = FTP('ftp.ncbi.nih.gov')
    ftp.login()
    ftp.cwd('/pub/geo/DATA/SeriesMatrix/')
    try:
        ftp.cwd(studyid)
    except:
        ftp.quit()
        return False

    ftp.quit()
    return True

def sendEmail(address, studyid):
    MESSAGE = 'Your request for study ' + studyid + ' has been processed \n\n to view go to http://yates.webfactional.com/studies/'+studyid
    SENDER = 'noreply@yates.webfactional.com'
    SUBJECT = 'Mine has processed your study!'

    Body = string.join(( "From: %s" % SENDER,
                         "To: %s" % address,
                         "Subject: %s" % SUBJECT,
                         "",
                         MESSAGE
                         ), "\r\n")
    
    server = smtplib.SMTP('smtp.webfaction.com')
    server.login('minebox','b0d79559')
    server.sendmail(SENDER, [address], Body)
    server.quit()

def remove(studyid, email):
        db.request.remove({"gse":studyid, "email":email})

def removeByNumber(studyid):
        db.request.remove({"gse":studyid})

def removeByEmail(email):
        db.request.remove({"email":email})

def uploadLine(studyid, varname, floats, no): 
        line = {"id": varname, "data": floats, "no": no}
        db[studyid].insert(line)

def NumberExists(studyid, no):
        if db[studyid].find({"no":no}).count() > 0:
                return True
        else:
                return False

def RetrieveData(studyid, no):
        return map(float, db[studyid].find({"no":no}).distinct("data"))

def RetrieveVariable(studyid, no):
        return db[studyid].find({"no":no}).distinct("id")       

def uploadStudy(studyid):

        #logging setup
        logging.basicConfig(filename='DEBUG.log',level=logging.INFO)

        #path for study files
        path = 'OUT/'
        listing = os.listdir(path)

        #for all studies (exclude the file log.txt)
        for file in listing:
                if not file == 'log.txt':
                        try:
                                #open the file
                                logging.info("trying to open " + file)
                                f = open(path + file)
                                count = 0

                                #for each line after the header
				logging.info("trying to read lines")
                                for line in f:
                                        count = count + 1
                                        if count > 3:
                                                try:
                                                        #insert lines
                                                        cells = line.split("\t")
                                                        no = count -3
                                                        uploadLine(studyid, cells[0], cells[1:], no)

                                                except:
                                                        logging.error("line " + count + " could not be read")

                                #close file
                                logging.info("closing " + file)
                                f.close()

                                #delete file from system
                                logging.info("removing " + file)
                                os.remove(path + file)
                        except:
                                logging.error("Could not open " + file)

                                


                                                              



