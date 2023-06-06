from rdflib import Graph,Namespace

import os

parameter = "temperature"


queryStr = """SELECT DISTINCT ?title ?affordance ?p
    WHERE {{
        ?a wottd:title ?title .
        {?a wottd:hasPropertyAffordance ?property .
        ?property rdf:type ?affordance .
        ?property wotdl:measures ?p .}
        UNION
        {?a wottd:hasActionAffordance ?action .
        ?action rdf:type ?affordance .
        ?action wotdl:affects ?p .}
        ?a wotdl:Parameters ?b .
        ?b ?c ?p
    }}"""
        


thisdir = os.getcwd() + "/instances/"
# print(thisdir)

for f in os.listdir(thisdir):

    g = Graph()

    g.parse(thisdir + f,format="json-ld")

    wottd = Namespace("https://www.w3.org/2019/wot/td#")
    wotdl = Namespace("http://vsr.informatik.tu-chemnitz.de/projects/2019/growth/wotdl#")
    http = Namespace("http://www.w3.org/2011/http#")

    g.bind("wottd", wottd)
    g.bind("wotdl", wotdl)
    g.bind("http", http)

    # import pprint
    # for stmt in g:
    #     pprint.pprint(stmt)
        
    qres = g.query(queryStr)

    for title, affordance, p in qres:
        if str(p).lower().find(parameter.lower()) != -1:
            if str(affordance).find("Measurement") != -1:
                print(" %-35s measures %s" % (title, parameter))
            else:
                print(" %-35s affects  %s" % (title, parameter))
    