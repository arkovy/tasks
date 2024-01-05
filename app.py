from flask import Flask, render_template, redirect, request
from db import create_connection

app = Flask(__name__)


@app.route('/')
def add_music_from_db():
    with create_connection('db_music_list.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM music')
        musics = cursor.fetchall()
        context = {
            'musics': musics
        }

    return render_template(
        'index.html', **context
    )


@app.route('/add-music/', methods=['POST'])
def add_music():
    with create_connection('db_music_list.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO music (text) VALUES ('{request.form['input-text']}')")
        conn.commit()

    return redirect('/')


@app.route('/delete-music/', methods=['POST'])
def delete_music():
    with create_connection('db_music_list.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM music WHERE id = ?", (request.form['id'],))
        conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
