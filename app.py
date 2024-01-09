from flask import Flask, render_template, redirect, request, g
from db import create_connection

app = Flask(__name__)


db_name = 'db_music_list.sqlite3'

app.config['DB_CONN'] = '/' + db_name


def get_db():
    if 'db' not in g:
        g.db = create_connection(db_name)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def add_music_from_db():
    conn = get_db()
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
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO music (text) VALUES (?)", (request.form['input-text'],))
    conn.commit()

    return redirect('/')


@app.route('/delete-music/', methods=['POST'])
def delete_music():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM music WHERE id = ?", (request.form['id'],))
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
