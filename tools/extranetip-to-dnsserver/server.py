#!/usr/bin/python3
#coding=utf-8
import sys
import os
import hashlib
from flask import Flask, jsonify, request
from flask import json

# This script is run into the docker container running bind.

app = Flask(__name__)

@app.route('/')
def index():
    return "Wecome to index!"

@app.route('/dns/update', methods=['POST'])
def predict():
    # Get parameters
    sign = request.args.get('sign')
    r = request.args.get('r')
    #ipaddr = request.args.get("ipaddr")
    ipaddr = request.remote_addr

    # Check signture
    key = 'au43hwe9dfkl'
    orgin = "%s%s" % (r,key)
    hl = hashlib.md5()
    hl.update(orgin.encode(encoding='utf-8'))
    _sign = hl.hexdigest()

    if sign != _sign:
        print('Calculation signture: %s, request singture: %s' % (sign, _sign))
        return jsonify({"code":"Illegal signture"})

    print("DNS update for : "+ipaddr)
    os.system("%s %s"%("/root/dns-update-tool.sh", ipaddr))

    return jsonify({"code":"ok","ipaddr":ipaddr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4008)
