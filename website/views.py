from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    all_notes = Note.query.order_by(Note.date).all()
    notes_with_users = []
    for note in all_notes:
        notes_with_users.append((note, User.query.get(note.user_id).first_name))
    return render_template("home.html", user=current_user, notes=notes_with_users)

@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("user.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/toggle-note', methods=['POST'])
def toggle_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            note.private = data['private']
            db.session.commit()

    return jsonify({})