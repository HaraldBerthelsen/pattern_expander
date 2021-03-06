# -*- coding: utf-8 -*-

import exrex
import re, sys

def generate(regexp):

    #check parentheses and brackets..
    if regexp.count("(") != regexp.count(")") or regexp.count("[") != regexp.count("]"):
        msg = "ERROR in \n%s\n%s" % (regexp, "unbalanced parentheses")
        print(msg)
        return ([],msg.split("\n"))

    
    #Because the format isn't actually regexp..
    org_regexp = regexp

    regexp = re.sub("\.", "\.", regexp)
    regexp = re.sub("\?", "\?", regexp)


    regexp = re.sub("\[", "(", regexp) 
    regexp = re.sub("\]", ")?", regexp)

    try:
        gens = list(exrex.generate(regexp))

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

        return (mod_gens, [])




    except:
        #msg = "ERROR in %s: %s %s" % (regexp, sys.exc_info()[0], sys.exc_info()[1])
        msg = "ERROR in \n%s\n%s" % (org_regexp, sys.exc_info()[1])
        print(msg)
        return ([],msg.split("\n"))


def test():

    test = u"(ring | [(börja | starta | ring) [ett]] samtal [till] | telefon)"
    #test = "[en] bil | [ett] tåg"
    
    gens = generate(test)
    for gen in gens:
        print(gen)
        


def read_stdin():

    import codecs
    char_stream = codecs.getreader("utf-8")(sys.stdin)
    #lines = sys.stdin.readlines()
    lines = char_stream.readlines()
    result = process(lines)
    for line in result:
        print(line)


def process(lines, compareAlternateLines=True):
    result = []
    no = 0
    prevline = "first line"

    for line in lines:
        line = line.strip()

        #A way to comment lines if needed
        if line.startswith("//"):
            continue
        if line == "":
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

        (gens, errors) = generate(line)


        if compareAlternateLines:
            #Check that prevline is included, if line contains expansion pattern
            #This should not always happen, but most of the time.. (?)
            #only do this when the current linenr is even (odd: main, even: extended)
            #and use this list to ignore some specific lines 
            ignore_lines = [222,326,384,388,390,406,410,416,418,420,422]


            #if re.search(r"\[|\(",line) and (no % 2 == 0) and no not in ignore_lines:
            #removed the constraint only to do this if the line has [,|, or ("
            if (no % 2 == 0) and no not in ignore_lines:

            #not only even
            #if re.search(r"\[|\(",line) and no not in ignore_lines:
                found = False

                old_version = False
                if old_version:
                    for gen in gens:

                        p = prevline.decode("utf-8")
                        p = p.strip()
                        p = re.sub(u"[^\u0627-\u064aa-zåäö]",r"",p)
                        
                        g = gen.strip()
                        g = re.sub(u"[^\u0627-\u064aa-zåäö]",r"",g)

                        #print("COMPARING\n#%s#\n#%s#\n" % (p, g))
                        #sys.exit()
                        if p == g:
                            found = True
                    if found == False:
                        #print("WARNING line %d: main not in expanded\n%s" % (no,prevline))
                        result.append(u"WARNING line %d: main not in expanded" % (no,))
                        result.append(u"%s" % (prevline,))
                        #sys.exit()

                else:
                    #also expand prevline in case it has an expansion pattern
                    #persian line 41 for instance
                    for prevline in prevgens:                            
                        found = False
                        for gen in gens:

                            #p = prevline.decode("utf-8")
                            p = prevline
                            p = p.strip()
                            p = re.sub(u"[^\u0627-\u064aa-zåäö]",r"",p)
                        
                            g = gen.strip()
                            g = re.sub(u"[^\u0627-\u064aa-zåäö]",r"",g)

                            #print("COMPARING\n#%s#\n#%s#\n" % (p, g))
                            #sys.exit()
                            if p == g:
                                found = True
                        if found == False:
                            #print("WARNING line %d: main not in expanded\n%s" % (no,prevline))
                            result.append(u"<span dir='ltr'>WARNING line %d: previous line not found in generated strings.</span>" % (no,))
                            #Maybe adding the previous line here is just confusing
                            #result.append(u"%s" % (prevline,))
                        #sys.exit()




            prevline = line
            prevgens = gens
        #end if check_prev

        #print("%d\n%s\n%d string(s)\n" % (no,line,len(gens)))
        result.append(u"<span dir='ltr'>input line %d:</span>" % (no,))

        if re.match(u"^[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F |()\[\]]+$",line):
            result.append(u"<span dir='rtl'>%s</span>" % (line,))
        else:
            result.append(u"%s" % (line,))

        if len(gens) < 2:
            result.append(u"<span dir='ltr'>%d string generated:</span>" % (len(gens),))
        else:
            result.append(u"<span dir='ltr'>%d strings generated:</span>" % (len(gens),))

        for gen in gens:
            #print(gen)
            if re.match(u"^[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F |()\[\]]+$",gen):
                result.append(u"<span dir='rtl'>%s</span>" % (gen,))
            else:
                result.append(gen)

        for error in errors:
            #print(gen)
            result.append(error)
    return result    

if __name__ == "__main__":
    #test()
    read_stdin()

