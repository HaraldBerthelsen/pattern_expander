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
        print "%d\n%s\n%d string(s)\n" % (no,line,len(gens))
        for gen in gens:
            print gen
        


#test()
read_stdin()

