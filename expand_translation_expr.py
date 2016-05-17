# -*- coding: utf-8 -*-

import exrex
import re, sys

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

    #build a dictionary to check for doubles
    gen_count = {}
    for gen in gens:    
        gen = gen.strip()
        gen = re.sub(" +"," ",gen)
        if gen in gen_count:
            gen_count[gen] += 1
        else:
            gen_count[gen] = 1



    mod_gens = []
    for gen in gens:    
        gen = gen.strip()
        gen = re.sub(" +"," ",gen)
        if gen_count[gen] > 1:
            mod_gens.append("WARNING --- DOUBLE %d" % gen_count[gen])
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

        #A way to comment lines if needed
        if line.startswith("//"):
            continue


        no = no+1
        #if re.search("[a-zA-Z]", line):
        #    print("WARNING: Latin characters in line %d: %s" % (no, line))

        #number each "esh esh esh" in persian
        i = 0
        esh = r"ششش"

        if re.search(esh+".*"+esh, line):
            #sys.stderr.write("A\n")
            #sys.stderr.write(line+"\n")

            while re.search(esh+"[^0-9]", line):
                line = re.sub("("+esh+r")([^0-9])", r"\g<1>"+str(i)+r"\g<2>", line, count=1) 
                i += 1

            #sys.stderr.write("B\n")
            #sys.stderr.write(line+"\n")
            #sys.exit()

        gens = generate(line)
        print("%d\n%s\n%d string(s)\n" % (no,line,len(gens)))
        for gen in gens:
            print(gen)
        


#test()
read_stdin()

