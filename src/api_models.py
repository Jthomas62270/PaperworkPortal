from db import db
from datetime import date

class Cue(db.Model): 
    __tablename__ = "cues"

    show_name = db.Column(db.String(120), db.ForeignKey('shows.show_name'), primary_key=True)
    cue_num = db.Column(db.REAL, primary_key=True)
    cue_part = db.Column(db.REAL, primary_key=True, nullable=True)
    scene_name = db.Column(db.String(120))
    label = db.Column(db.String(120))
    duration = db.Column(db.REAL)
    up_time = db.Column(db.REAL)
    down_time = db.Column(db.REAL, nullable=True)
    up_delay = db.Column(db.REAL, nullable=True)
    down_delay = db.Column(db.REAL, nullable=True)
    follow = db.Column(db.REAL, nullable=True)

    def __repr__(self): 
        return f"<Cue {self.show_name}, {self.cue_num}"

class Show(db.Model):
    __tablename__ = "shows"

    show_name = db.Column(db.String(120), primary_key= True)
    date_added = db.Column(db.Date, nullable= True)
    company = db.Column(db.String(120), nullable= True)

    def __repr__(self): 
        return f"<Show {self.show_name}, {self.date_added}"

class Note(db.Model): 
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key= True)
    show_name = db.Column(db.String(120), db.ForeignKey('cues.show_name'), primary_key= True)
    cue_num = db.Column(db.REAL, db.ForeignKey('cues.cue_num'))
    note = db.Column(db.Text, nullable= True)

    def __repr__(self): 
        return f"<Note {self.show_name} {self.cue_num}"
