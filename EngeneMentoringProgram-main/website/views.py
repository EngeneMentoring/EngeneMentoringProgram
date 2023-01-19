from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
import codecs

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    all_notes = Note.query.order_by(Note.date).all()
    notes_with_users = []
    for note in all_notes:
        if note.adminStatus == 1:
            user = User.query.get(note.user_id).first_name
            user = '~' + user
            notes_with_users.append((codecs.decode(note.data, 'unicode_escape'), user, note.capsuleId, note.id)) # something changes the notes into r strings which makes it ignore
                                                                                        # the \n characters
    return render_template("home.html", user=current_user, notes=notes_with_users)

@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, capsuleId=current_user.first_name[0:2] + datetime.utcnow().strftime("%d-%m-%Y") + current_user.school_name.replace(' ', '_')+str(current_user.id))
            db.session.add(new_note)
            db.session.commit()
            print(current_user.id)
            flash('Note added!', category='success')
            # flash('Careful..! If you reload the page without clicking on any of these 1 button {Private/Public} It is gonna multiply the notes', category="error")

    updated_notes = []
    for note in current_user.notes:
        updated_notes.append((note.data, note.id))
    return render_template("user.html", user=current_user, notes=updated_notes)

@views.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    all_notes = Note.query.order_by(Note.date).all()
    notes_with_users = []
    for note in all_notes:
        if note.adminStatus == 0:
            user = User.query.get(note.user_id).first_name
            user = '~' + user
            notes_with_users.append((codecs.decode(note.data, 'unicode_escape'), user, note.id, note.capsuleId)) # something changes the notes into r strings which makes it ignore
                                                                                        # the \n characters
    return render_template("admin.html", user=current_user, notes=notes_with_users)

@views.route('/capsule', methods=['GET'])
def capsule():
    args = request.args
    capsule_id = args.get('id')
    
    return jsonify({})

@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# @views.route('/toggle-note-private', methods=['POST'])
# def toggle_note_private():
#     data = json.loads(request.data)
#     noteId = data['noteId']
#     note = Note.query.get(noteId)
#     private = data['private']
#     if note:
#         if note.user_id == current_user.id:
#             note.private = private
#             db.session.commit()

    # return jsonify({})

@views.route('/toggle-note-status', methods=['POST'])
def toggle_note_status():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    status = data['status']
    if note:
        if current_user.admin:
            note.adminStatus = status
            db.session.commit()

    return jsonify({})