#!/usr/bin/env python3

import connexion
import subprocess
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os, sys, time

from wot_api import encoder

IMPLEMENTATION_FOLDER = '../implementations'
INSTANCE_FOLDER = '../instances'

app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder

app.add_api('openapi.yaml',
            arguments={'title': 'Demo of WoT Interface Creation'},
            pythonic_params=True)

proc = None


@app.route("/add-device", methods=['GET', 'POST'])
def add_device():


    if request.method == 'POST':
        implementation = request.files['implementation']
        filename = secure_filename(implementation.filename)
        implementation.save(IMPLEMENTATION_FOLDER + '/' + filename)
        
        instance = request.files['instance']
        filename = secure_filename(instance.filename)
        instance.save(INSTANCE_FOLDER + '/' + filename)
        
        proc = subprocess.Popen(cwd = os.path.abspath('..'), args = 'bash pi_redeploy.sh', shell=True)
        return render_template("add_device.html")
    

    return render_template("add_device.html")

def waiting():
    while proc.poll() is None:
        print("still running...")
        time.sleep(1)

if __name__ == '__main__':
    app.run(port=9000, debug=True)
