from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from statistics import mode

app = Flask('__name__')
CORS(app)

valor_Humedad = {'sensor':'FC28','variable':'Humedad','unidades':'humedad_%'}  

medicion = [
    {'id':1,'fecha':'2019-06-21 11:24:06',**valor_Humedad,'valor':500},
    {'id':2,'fecha':'2019-06-22 11:24:06',**valor_Humedad,'valor':14},
]

@app.route('/mediciones',methods=['POST'])
def postOne():
    body = request.json
    t = False
    preid=1
    for x in medicion:
        if x['id'] != preid:
            body['id'] = preid
            t = True
            break        
        preid = preid + 1    
    if t == False:
        body['id'] = preid
    now = datetime.now()
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    medicion.append({**body,**valor_Humedad})
    return jsonify(medicion)

@app.route('/mediciones',methods=['GET'])
def getAll():
    return jsonify(medicion)

@app.route('/mediciones/<string:val>',methods=['DELETE'])
def delmedi(val):
    vali=int(val)
    deta = [medicion for medicion in medicion if medicion['id'] == vali]
    medicion.remove(deta[0])
    return jsonify(medicion)

@app.route('/mediciones/<string:val>',methods=['PUT'])
def editone(val):
    vali=int(val)
    deta = [medicion for medicion in medicion if medicion['id'] == vali]
    deta[0]['valor'] = request.json['valor']
    now = datetime.now()
    deta[0]['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    return jsonify({'medicion' : deta[0]})

@app.route('/media',methods=['GET'])
def getMedia():
    Lvalores = []
    for x in medicion:
     Lvalores.append(x['valor'])
    sumt = sum(Lvalores)
    N = float(len(Lvalores))
    Me= sumt/N
    return jsonify(valor = Me)

@app.route('/')
def test():
    return "Medicion de Humedad con su Media"

app.run(port=8080,debug=True)