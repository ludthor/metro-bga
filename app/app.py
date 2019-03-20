from flask_socketio import SocketIO
from flask import Flask, render_template, request
import json
from generator import Generator
from comunas import Comunas
import config

#@author ludhtor
app = Flask(__name__)
socketio = SocketIO(app)

#Array of Political partitions of the city of Bucaramanga called Comunas
comunas = []

#Endpoint for capture the Comunas polygons manually.
#All the polygons are stored on the comunas.json (Buggy)
@app.route('/captura', methods=['GET', 'POST'])
def captura():
    app.logger.debug("Entering captura endpoint")
    try:
        global comunas
        print("Ejecución:" + str(len(comunas)))
        if request.method == 'POST':
            app.logger.debug("POST handle logic")
            app.logger.debug(request.form['list'])
            g = Generator()
            g.createComuna(request.form['comuna'],processList(request.form['list']))
            #c.export()
            comunas.append(g)
            g.export()
            return '200'
        elif request.method == 'GET':
            return render_template('generate.html')
    except Exception as e:
        app.logger.error("Error loading captura endpoint: " + str(e), exc_info=True)
        return '500'

#IA processing and final Visualization of the 
@app.route('/estaciones')
def estaciones():
    app.logger.debug("Entering estaciones endpoint")
    try:    
        c = Comunas()
        c.loadComunas()
        c.createPolygons()
        c.createPoints(config.TOTAL_POBLACION)
        centros = c.createClusters().tolist()
        c.calculateMinimalRoads()
        caminos = c.roadsDraw()
        objret = {
            'centers' : centros,
            'roads' : caminos,    
        }
        return render_template('estaciones.html', objret=objret)
    except Exception as e:
        app.logger.error("Error loading estaciones endpoint" + str(e), exc_info=True)
        return '500'
    

"""
Sockets logic
For automatic map updating on data capture (Still Buggy)
"""
def messageReceived(methods=['GET', 'POST']):
   app.logger.debug("Message received")

@socketio.on('my_event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    app.logger.debug("Received my_event" + str(json))
    socketio.emit('my_response', json, callback=messageReceived)
                        

"""
Aux functions
"""
def processList(_list):
    app.logger.debug("Processing list of comunas")
    try:
        l = str(_list).split(',')
        lreturn = []
        for item in l:
            lreturn.append(tuple(item.split('#')))
        app.logger.debug(lreturn)
        return lreturn
    except Exception as e:
        app.logger.error("Error processing list " + str(e), exc_info=True)

# def drawComuna():
#     app.logger.debug("Creating JSON for real time comunas drawing")
#     try:
#         for c in comunas:
#             #l = list(c.comuna['poligono'])
#             #socketio.emit('draw_comuna', l)
#             c.export()
#     except Exception as e:
#         app.logger.debug("Error preparing data for draw" + str(e))

socketio.run(app, debug=True)