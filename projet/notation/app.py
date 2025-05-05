from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import uuid

app = Flask(__name__)
DATABASE = "/data/notes.db"

# Crée le dossier si nécessaire
if not os.path.exists("/data"):
    os.makedirs("/data")

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            commande_id TEXT,
            note INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('note'))

@app.route('/notation/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        commande_id = request.form.get('commande_id')
        note = request.form.get('note')

        if not commande_id or not note or not note.isdigit() or int(note) not in range(1, 6):
            return render_template("note.html", erreur="Merci de saisir un ID valide et une note entre 1 et 5.")

        note_id = str(uuid.uuid4())

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO notes (id, commande_id, note) VALUES (?, ?, ?)", (note_id, commande_id, int(note)))
        conn.commit()
        conn.close()

        return redirect(url_for('notes'))

    return render_template("note.html")

@app.route('/notation/notes')
def notes():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT commande_id, note FROM notes")
    notes_list = c.fetchall()
    conn.close()
    return render_template("notes.html", notes=notes_list)
