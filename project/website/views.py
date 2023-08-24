from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from .models import Note, User
import json
from website import db
views = Blueprint('views', __name__) # views é o que é importado no init

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        public_notes = Note.query.filter_by(public=True).all()
        for note in public_notes:
            user =  User.query.filter_by(id=note.user_id).first()
            note.username = user.name
        return render_template("index.html", user=current_user, public_notes=public_notes)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must be logged in to add a note', category='error')
            return redirect(url_for('auth.login'))
        note = request.form.get('note')
        public = request.form.get('public') #on off 
        public = True if public == 'on' else False
        if not note:
            flash('Note is empty', category='error')
            return
        new_note = Note(text=note, user_id=current_user.id, public=public)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added', category='success')
        return redirect(url_for('views.home'))
    


@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note_to_delete = Note.query.get(note_id)
    if note_to_delete:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()
            flash('Note deleted', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('You cannot delete this note', category='error')
            return redirect(url_for('views.home'))
    return jsonify({})