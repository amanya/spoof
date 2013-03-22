from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from model import Move, session
import json

# configuration
DATABASE = '/tmp/spoof.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('spoof.html')

@app.route('/mkmove', methods = ['POST'])
def mkmove():
    move = Move(request.form['initiator'],
                request.form['adversary'],
                request.form['initiator_hold'],
                request.form['initiator_guess'])
    session.add(move)
    session.commit()
    data = {'moveid': move.moveid}
    js = json.dumps(data)
    session.close()
    resp = Response(js, status=200, mimetype="application/json")
    return resp

@app.route('/m/<moveid>')
def challenge(moveid):
    return render_template('challenge.html', moveid=moveid)

@app.route('/f/<moveid>', methods = ['POST'])
def finish(moveid):
    move = session.query(Move).filter_by(moveid=moveid)[0]
    move.adversary_hold = request.form['adversary_hold']
    move.adversary_guess = request.form['adversary_guess']
    session.commit()
    totals = move.adversary_hold + move.initiator_hold
    if move.adversary_guess == move.initiator_guess:
        # Empates
        session.close()
        return "Empate!"
    else:
        initiator_aprox = abs(move.initiator_guess - totals)
        adversary_aprox = abs(move.adversary_guess - totals)
        session.close()
        if initiator_aprox < adversary_aprox:
            # Guanya initiator
            return "You lose!"
        else:
            # Guanya adversary
            return "You win!"



if __name__ == '__main__':
    app.run()
