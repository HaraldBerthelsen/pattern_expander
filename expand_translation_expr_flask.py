# -*- coding: utf-8 -*-

import re, sys
import exrex

from flask import Flask, request, json, render_template

def generate(regexp):

    #Because the format isn't actually regexp..
    regexp = re.sub("\.", "\.", regexp)
    regexp = re.sub("\?", "\?", regexp)


    regexp = re.sub("\[", "(", regexp) 
    regexp = re.sub("\]", ")?", regexp)

    try:
        gens = list(exrex.generate(regexp))
    except:
        print "ERROR in %s: %s %s" % (regexp, sys.exc_info()[0], sys.exc_info()[1])
        gens = []
        #sys.exit()
    
    #print "Generated %d string(s)" % len(gens)
    mod_gens = []
    for gen in gens:    
        gen = gen.strip()
        gen = re.sub(" +"," ",gen)
        mod_gens.append(gen)
    return mod_gens



def test():

    test = "(ring | [(börja | starta | ring) [ett]] samtal [till] | telefon)"
    #test = "[en] bil | [ett] tåg"
    
    gens = generate(test)
    for gen in gens:
        print gen
        


def read_stdin():
    lines = sys.stdin.readlines()
    no = 0
    for line in lines:
        line = line.strip()
        no = no+1
        gens = generate(line)
        print "%d\t%s\t%d string(s)" % (no,line,len(gens))
        for gen in gens:
            print gen
        


def getParam(param,default=None):
    value = None
    print("getParam %s, request.method: %s" % (param, request.method))
    if request.method == "GET":
        value = request.args.get(param)
    elif request.method == "POST":
        if param in request.form:
            value = request.form[param]
    print("VALUE: %s" % value)
    if value == None:
        value = default
    return value



#test()
#read_stdin()



app = Flask(__name__)
@app.route('/', methods=['GET'])
def form():
    return render_template("form.html")

@app.route('/', methods=['POST'])
def form_post():

    text = request.form['text']
    lines = text.encode("utf-8").split("\n")
    out = []
    for line in lines:
        print("LINE: %s" % line)
        gens = generate(line)
        print("GENS: %s" % gens)
        print("NR GEN: %d" % len(gens))
        out.append(gens)
    return render_template("form.html", text=text, data=out)


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
