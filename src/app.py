from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
from Paperwork import Watcher
from api_models import Cue, Show, Note
from db import db
from datetime import datetime
import pandas as pd
import os 

CUES_PATH = "./FORMATTED_CUES/"

api = Flask(__name__)
CORS(api)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.db'
api.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
api.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(api)

with api.app_context():
    db.create_all()

### SHOWS ###

@api.route('/api/post/shows/<showName>', methods=['GET'])
def postShow(showName): 
    try: 
        create_time = os.path.getctime(CUES_PATH + showName)
        creation_time_readable = datetime.fromtimestamp(create_time).date()

        new_entry = Show(show_name= showName, date_added= creation_time_readable, company= "Case High Theatre Company")
        db.session.add(new_entry)
        db.session.commit()

        return showName + ": show added to database successfully..."
    except FileNotFoundError: 
        print(f'file {showName} not found...')
    except: 
        return showName + " : Already exists..."

@api.route('/api/get/shows', methods=['GET'])
def getShows(): 
    shows = Show.query.all()
    show_list = [{'SHOW_NAME': show.show_name, 'DATE_ADDED': show.date_added, 'COMPANY': show.company} for show in shows]
    return jsonify(show_list)

@api.route('/api/delete/shows/<showName>/<date>')
def deleteShow(showName, date):
    show = Show.query.get((showName, date))

    if show: 
        db.session.delete(show)
        db.commit()
        return "Show: Delete..."
    else: 
        return f"Show: Show {showName}, {date} not found..."

### CUES ###

@api.route('/api/post/cues/<showName>', methods=['GET'])
def postCues(showName):
    try: 
        infile = CUES_PATH + showName 
        data = pd.read_csv(infile)
        print(data)
        for index, row in data.iterrows(): 
            new_entry = Cue(show_name= showName, \
                            cue_num= row["CUE_NUMBER"], \
                            cue_part= row["PART_NUMBER"], \
                            scene_name= row["SCENE_NAME"], \
                            label= row["LABEL"], \
                            duration= row["DURATION"], \
                            up_time= row["UP_TIME"], \
                            down_time= row["DOWN_TIME"], \
                            up_delay= row["UP_DELAY"], \
                            down_delay= row["DOWN_DELAY"], \
                            follow= row["FOLLOW"])
            
            db.session.add(new_entry)
            db.session.commit()

        return showName + ": cues saved to the database succesfully..."
    except FileNotFoundError: 
        print("Error: File in ", infile, " not found.")
    except: 
        return showName + " : Already exists..."
    
@api.route('/api/update/cues/<showName>', methods=['POST'])
def updateShow(showName): 
    try: 
        cues = request.get_json()

        for index, row in cues.iterrows(): 
            new_entry = Cue(show_name= showName, \
                            cue_num= row["CUE_NUMBER"], \
                            cue_part= row["PART_NUMBER"], \
                            scene_name= row["SCENE_NAME"], \
                            label= row["LABEL"], \
                            duration= row["DURATION"], \
                            up_time= row["UP_TIME"], \
                            down_time= row["DOWN_TIME"], \
                            up_delay= row["UP_DELAY"], \
                            down_delay= row["DOWN_DELAY"], \
                            follow= row["FOLLOW"])
            
            db.session.add(new_entry)
            db.session.commit()

        return showName + ": cues saved to the database succesfully..."
    except: 
        return showName + " : Cannot be updated..."
    

@api.route('/api/get/cues/<showName>', methods=['GET'])
def getCues(showName): 
    cues = Cue.query.filter_by(show_name= showName).all()
    cue_list = [{'CUE_NUMBER': cue.cue_num, 'PART_NUMBER': cue.cue_part, 'SCENE_NAME': cue.scene_name, 'LABEL': cue.label, 'DURATION': cue.duration, 'UP_TIME': cue.up_time, 'DOWN_TIME': cue.down_time, 'UP_DELAY': cue.up_delay, 'DOWN_DELAY': cue.down_delay, 'FOLLOW': cue.follow} for cue in cues]
    return jsonify(cue_list)

@api.route('/api/delete/cue/<string:showName>/<float:cueNum>/<int:cuePart>', methods=['DELETE'])
def deleteCue(showName, cueNum, cuePart): 
    #if cuePart == 0: cuePart = math.nan
    cue = db.session.get(Cue, (showName, cueNum, cuePart))

    if cue: 
        db.session.delete(cue)
        db.session.commit()
        return "Cue: Delete..."
    else: 
        return f"Cue: Cue {cueNum}, {cuePart} of {showName} not found..."

### NOTES ###

@api.route('/api/post/notes', methods=['POST'])
def postNotes(): 
    note = request.get_json()

    new_entry = Note(show_name= note['show_name'], cue_num= note['cue_num'], note= note['note'])
    db.session.add(new_entry)
    db.session.commit()
    return "Note: addded successfully..."

@api.route('/api/get/notes', methods=['GET'])
def getNotes():
    show_name = request.args.get('show_name')
    cue_num = request.args.get('cue_num')
    notes = Note.query.filter_by(show_name= show_name,cue_num= cue_num).all()
    notes_list = [{"NOTE_ID": note.id,"SHOW_NAME": note.show_name, "CUE_NUM": note.cue_num, "NOTE": note.note} for note in notes]
    return jsonify(notes_list)

@api.route('/api/delete/notes/<showName>/<noteId>', methods=['DELETE'])
def deleteNotes(noteId, showName): 

    notes = Note.query.get((noteId, showName))
    if notes: 
        db.session.delete(notes)
        db.session.commit()
        return "Note: Delete...."
    else: 
        return f"Note: Note {noteId} of {showName} not found..."

if __name__ == '__main__': 
    watcher_thread = Thread(target=Watcher().run)
    watcher_thread.start()
    api.run(debug=True)
    watcher_thread.join()
