# -*- coding: utf-8 -*-

from flask import Flask, request, json, render_template
from expand_translation_expr import *

app = Flask(__name__)
@app.route('/', methods=['GET'])
def form():
    text=u"""
 لغو کن
 (لغو کن | حذف کن | تمام کن) [عمل کن |مورد | تنظیم| انتخاب کن]
"""
    text = ""
    direction = "ltr"
    return render_template("form.html", direction=direction, initial_text=text)

@app.route('/', methods=['POST'])
def form_post():

    print(request)
    print(request.form)

    text = request.form['text']

    direction = "ltr"
    if 'direction' in request.form:
        direction = request.form['direction']

    compAlt = False
    compAltChecked = ""
    if 'compareAlternateLines' in request.form:
        compAlt = True
        compAltChecked = "checked"

    #lines = text.encode("utf-8").split("\n")
    lines = text.split("\n")
    out = process(lines, compareAlternateLines=compAlt)
    return render_template("form.html", direction=direction, compAltChecked=compAltChecked, initial_text=text, data=out)


@app.route('/expand/', methods=["GET", "POST"])
def expand():
    input = getParam("input").encode("utf-8")
    lines = input.split("\n")
    out = []
    for line in lines:
        print("LINE: %s" % line)
        gens = generate(line)
        print("GENS: %s" % gens)
        print("NR GEN: %d" % len(gens))
        out.append(gens)
    return json.dumps(out)

if __name__ == '__main__':
    app.run(port=54321, debug=True)
