#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
import random
from flask import Flask, render_template, request, Markup

############# KETTLEBATTLE STATION ##############

REPS_PRESET = (200, 300)    #set absolute repetitions for preset buttons

# kettlebell exercises (name, min at preset 1, min at preset 2)
KB_EX = [("Squats (w/o)", 50, 50),
         ("Squats (w/)", 0, 0),
         ("Swings (one arm)", 50, 100),
         ("Swings (two arms)", 0, 0),
         ("Snatches", 0, 40),
         ("Clean & Jerks", 0, 0),
         ("Rows", 0, 0),
         ("Figure-8 curls", 0, 0),
         ("Halos", 0, 20),
         ("Deadlifts", 0, 0),
         ("Kettlebell circles", 0, 30),
]

MAX_EX = 4  #max number of exercises to generate workout, minimum presets are always counted

####################################################

FORM_PRESET = [("{} {}".format(REPS_PRESET[0], 1), REPS_PRESET[0]),
               ("{} {}".format(REPS_PRESET[1], 2), REPS_PRESET[1])]

def generate_workout(abs_reps, pos):
    #generate exercise list for chosen preset
    exercises = []
    for ex in KB_EX:
        exercises.append([ex[0], ex[pos]])
    #sum up minimum values
    min_reps = 0
    for ex in exercises:
        min_reps += ex[1]
    #choose random exercises from list, max number given in MAX_EX variable
    dothese = random.sample(exercises, MAX_EX)
    #add 10 repetitions to one of the random exercises to absolute repetition number
    for x in range(min_reps, abs_reps, 10):
        random.choice(dothese)[1] += 10
    return exercises

########### FLASK ###########

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['submit'] == 'generate':
            #create workout list, render template with this list instead of KB_EX so values are kept
            workout = []
            for ex in KB_EX:
                if request.form[ex[0]] == '':
                    rep = 0
                else:
                    rep = int(request.form[ex[0]])
                workout.append((ex[0], rep))
            #create list for sharing via c&p, don't list exercises w/ 0 reps
            battle = []
            total = 0
            for ex in workout:
                if ex[1] > 0:
                    battle.append((ex[0], ex[1]))
                    total += ex[1]
            return render_template('kettlebattle.html', form=request.form, reps=FORM_PRESET, exc=workout, battletext=battle, total=total, showgen=True)
        elif request.form['submit']:
            abs_reps, pos = request.form['submit'].split()
            workout = generate_workout(int(abs_reps), int(pos))
            return render_template('kettlebattle.html', form=request.form, reps=FORM_PRESET, exc=workout)
    elif request.method == 'GET':
        return render_template('kettlebattle.html', form=request.form, reps=FORM_PRESET, exc=KB_EX)

@app.route('/about')
def about():
    with open('README.md') as f:
        readme = f.read()
    readme = Markup(markdown.markdown(readme))
    return render_template('about.html', readme=readme)

if __name__ == '__main__':
    app.run(debug=True)

