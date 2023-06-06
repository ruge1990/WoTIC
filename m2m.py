from urllib.parse import urlparse
from rdflib import Graph,Namespace
from collections import defaultdict
import yaml
import json
import os


queryStr = """SELECT ?title ?name ?type ?url ?property ?ptype
    WHERE {{
        ?id wottd:title ?title .
        {?id wottd:hasPropertyAffordance ?affordance }
        UNION
        {?id wottd:hasActionAffordance ?affordance}
        ?affordance wottd:title ?name .
        ?affordance rdf:type ?type .
        ?affordance wottd:hasForm ?form .
        ?form wottd:href ?url .
        OPTIONAL{
          ?form wotdl:httpBody ?body .
          ?body ?property ?p .
          ?p wottd:type ?ptype
        }
        }}
"""

dir = "./instances/"

paths = defaultdict(dict)
resources = defaultdict(list)

for f in os.listdir(dir):

    g = Graph()

    g.parse(dir + f, format="json-ld")

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

    for title, name, type, url, property, ptype in qres:

        # print(' %s\n %s\n %s\n %s\n %s\n %s' % (title, name, type, url, property, ptype))

        url = urlparse(url)
        if str(type).endswith("Measurement"):
            method = 'get'
            body = None
        else:
            method = 'post'
            body = None
            if(property):
                property = str(property).split('#')[1]

                body = {
                    'content': {
                        'application/x-www-form-urlencoded':{
                            'schema': {
                                'properties':{
                                    property: {
                                        'type': str(ptype)
                                    }
                                },
                                'required': [property],
                                'type': 'object'
                            }
                        },
                    },
                    'required': True
                }

        resources[url.path].append(
            {'method': method,
             'device': title,
             'name': name,
             'query_params': url.query,
             'body': body}
        )
        body = None
        # print(resources[url.path])

    for resource in resources:
        requests = resources[resource]
        paths[str(resource)] = {}
        responses = {}

        for request in requests:
            entry = {
                'operationId': str(request['name']),
                'summary': str(request['name']) + ' request on device ' + str(request['device'])
            }

            if request['body'] != None:
                entry['requestBody'] = request['body']

            if request['method'] == 'get':
                responses['200'] = {'description': 'OK'}
            elif request['method'] == 'post':
                responses['201'] = {'description': 'Created'}
            
            entry['responses'] = responses
            paths[str(resource)][str(request['method'])] = entry

port = 9000
open_api = {
    'openapi': '3.0.0',
    'info': {
        'version': '1.0.0',
        'title': 'Demo of WoT Interface Creation',
    },
    'servers': [{'url': 'https://192.168.178.22:' + str(port) + '/api'},
                {'url': 'coap://192.168.178.22'}],
    'paths': dict(paths)
}

with open('api.yaml', 'w') as yamlfile:
    yaml.dump(open_api, stream=yamlfile)

api_name = 'wot_api'
with open('config.json', 'w') as configfile:
    json.dump({'packageName': api_name, 'defaultController': api_name + '_controller', 'serverPort': port}, fp=configfile)