# app.py

import config
import io
import sqlite3
from flask import abort, Flask, g, request
from os import path
from pydub import AudioSegment

app = config.connexion_app
#Path to database
DATABASE = app.app.root_path+'/database.db'

#Default route
@app.route("/")
def home():
  return "home"

#Route for getting audio file
@app.route('/audio/user/<userid>/phrase/<phraseid>/<audioformat>')
def get_file(userid, phraseid, audioformat, methods=['GET']):
  #If audio format is something else than mp3, return error
  if audioformat != 'mp3':
    return abort (400, f"Only supported audio format is mp3")
  #Check if a phrase with given userID and phraseID exists in the DB
  phrase_exists = run_query("SELECT pathToFile FROM pathsToFiles WHERE userID=? AND phraseID=?", [userid, phraseid])
  if phrase_exists:
    #If a phrase is found, convert the saved wav file into mp3 and export to memory. 
    #Return the converted file from memory.
    memoryBuffer = io.BytesIO()
    wavSegment = AudioSegment.from_wav(phrase_exists[0][0])
    wavSegment.export(memoryBuffer, format="mp3")
    return memoryBuffer
  else:
    return abort (400, f"No phrase found with given userID and phraseID")

@app.route('/audio/user/<userid>/phrase/<phraseid>', methods=['POST'])
def save_file(userid, phraseid):
  #Run queries to check if the phraseID and userID already exist.
  #PhraseID needs to be unique
  phraseid_exists = run_query('SELECT * FROM phrases WHERE phraseID=?', [phraseid])
  user_exists = run_query('SELECT * FROM users WHERE userID=?', [userid])
  if phraseid_exists:
    return abort (400, f"PhraseID already exists, please use another ID")
  #Get the file from the request, and add the userID and phraseID to the filename to make it unique
  #Use pydub to export the mp3 file onto disk as wav
  originFile = request.files['audio_file']
  newName = userid+'_'+phraseid+'_'+originFile.filename.replace("mp3", "wav")
  mp3Segment = AudioSegment.from_mp3(originFile)
  mp3Segment.export(newName, format="wav")
  #If userID didn't exist in the DB, add a new entry
  if not user_exists:
    run_query('INSERT INTO users(userID) VALUES(?)', [userid])
  #Add phraseID into phrases table, and add the path with userid and phraseid into pathsToFiles table
  run_query('INSERT INTO phrases(phraseID) VALUES(?)', [phraseid])
  run_query('INSERT INTO pathsToFiles(userID, phraseID, pathToFile) VALUES(?,?,?)', [userid, phraseid, newName] )
  return 'File saved'

#Helper function to open a connection to the database
def get_database():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  return db

#Helper function to run a query with arguments
def run_query(query, args):
  db = get_database()
  cur = db.cursor()
  cur.execute(query, args)
  returnValue = cur.fetchall()
  db.commit()
  cur.close()
  return returnValue

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)

