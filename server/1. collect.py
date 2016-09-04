import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import random
import time
import uuid
from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

"""
inline functions:
* c(colour, text)
* s(shape, text)

colour - str(colour or hex value w(/o) "#")
shape - str(square || triange || square || star || ...)

"""

def randomcolourshape(exception):
    # exception = [(), (), ...]
    # exception = (str(colour),str(shape)) -> [(str(colour),str(shape))]
    if type(exception) is tuple: exception = [exception]
    colours = ['green', 'red', 'blue', 'yellow']
    shape = ['circle', 'square', 'triangle', 'star']
    r = random.choice
    result = (r(colours), r(shape))
    while (result[0], result[1]) in exception:
        result = (r(colours), r(shape))
    return result

questionsArr = [
    # colour text shape
    'red red circle',
    'green green square',
    'blue blue triangle',
    'red red circle',
    'green green square',
    'blue blue triangle',
    'red red circle',
    'green green square',
    'blue blue triangle',
    'red red circle',
    'green green square',
    'blue blue triangle',
    'red blue circle', # 13
    'green green square',
    'blue blue triangle',
    'green red circle', # 16
    'green green square',
    'blue blue triangle',
    'red red circle',
    'blue green square', # 20
    'green blue triangle', # 21
    'red red circle',
    'green green square',
    'blue blue triangle',
]

def generatePageData(qid):
  qa = questionsArr[qid-1].split()
  answer = (qa[1],qa[2])
  fakeanswer = (qa[0],qa[2])
  options = ([randomcolourshape(answer) for _ in range(3)] if qa[0] == qa[1] else [randomcolourshape([answer, fakeanswer]) for _ in range(2)] + [fakeanswer]) + [answer]
  options.sort(key=lambda k: random.random())
  return {
    'infotext': [qa[0].replace('yellow', 'gold').replace('blue','dodgerblue').replace('red','lightcoral')] + qa[1:],
    'options': options,
    'correct': options.index(answer) + 1
  }

@app.route('/startc/', methods=['GET', 'POST'])
@app.route('/start/', methods=['GET', 'POST'])
def startPuzzle():
  global questionsArr
  questions = len(questionsArr)
  if 'cq' not in session:
    qa = range(1,questions+1)
    session['questionorder'] = sorted(qa, key=lambda k: random.random()) if 'startc' in request.url_rule.rule else qa
    session['questions'] = [generatePageData(i) for i in session['questionorder']]
    session['responses'] = []
    session['cq'] = 1
    session['start'] = int(time.time())
    session['token'] = random.randint(0,9)
    session['id'] = str(uuid.uuid4())[-12:]
    print("New%s session %s created from user (%s)" % (' control' if 'startc' in request.url_rule.rule else '', session['id'], request.environ['REMOTE_ADDR']))
  if request.method == 'POST':
    if int(request.form['token']) == session['token']:
      print("[%s] Q%s - %s submitted choice %s (Correct: %s)" % (request.environ['REMOTE_ADDR'],session['cq'],session['id'],request.form['option'],session['questions'][session['cq']-1]['correct']))
      session['responses'].append(int(request.form['option']))
      session['cq'] += 1
      if session['cq'] > questions:
        print("%s finished the task!" % session['id'])
        with open('2. results.dat','a') as f:
          f.write("%s,%s,%s,%s,%s\n" % ('control' if 'startc' in request.url_rule.rule else '', str(session['start']), str(int(time.time())), ",".join(["%s-%s" % (str(session['responses'][i]), str(session['questions'][i]['correct'])) for i in range(questions)]),"-".join([str(x) for x in session['questionorder']])))
        session.clear()
        return '<html><head><meta http-equiv="refresh" content="2;url=/" /><title>Thank You</title></head>Thank you for completing the puzzle! Redirecting...</html>'
      session['token'] = random.randint(0,9)
    return redirect(request.url_rule.rule)
  return render_template('quizpage.html', data=session['questions'][session['cq']-1], token=session['token'], question=session['cq'])

@app.route('/')
def landing():
  return render_template('landing.html')

import os
app.secret_key = os.urandom(24)

if __name__ == '__main__':
  import socket
  __port = 8080
  from os import system
  system("title %s:%s ^| Psychology Test Server" % (str(socket.gethostbyname(socket.gethostname())),str(__port)))
  print("Opening web server at %s:%s\n" % (str(socket.gethostbyname(socket.gethostname())),str(__port)))
  app.run(host='0.0.0.0', port=__port, threaded=True)