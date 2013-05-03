from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from flaskext.babel import Babel, gettext
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
babel = Babel(app)

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
    data = {'moveid': move.moveid,
            'text': gettext('You have been challenged!')}
    js = json.dumps(data)
    session.close()
    resp = Response(js, status=200, mimetype="application/json")
    return resp

@app.route('/m/<moveid>')
def challenge(moveid):
    move = session.query(Move).filter_by(moveid=moveid)[0]
    return render_template('challenge.html', 
                           initiator_guess=move.initiator_guess,
                           moveid=moveid)

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

@app.route('/info/<moveid>')
def info(moveid):
    move = session.query(Move).filter_by(moveid=moveid)[0]
    data = {'moveid': move.moveid,
            'initiator_guess': move.initiator_guess}
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype="application/json")
    return resp
    
@app.route('/done/<moveid>')
def done(moveid):
    move = session.query(Move).filter_by(moveid=moveid)[0]
    if move.adversary_hold and move.adversary_guess:
        # Finished
        if move.adversary_guess == move.initiator_guess:
            # Empates
            session.close()
            return "Empate!"
        else:
            totals = move.adversary_hold + move.initiator_hold
            initiator_aprox = abs(move.initiator_guess - totals)
            adversary_aprox = abs(move.adversary_guess - totals)
            session.close()
            if initiator_aprox < adversary_aprox:
                # Guanya initiator
                return "You win!"
            else:
                # Guanya adversary
                return "You lose!"
    else:
        return ""

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ca', 'en'])


if __name__ == '__main__':
    app.run()
