from shapely.geometry import Polygon, Point
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

import numpy as np
from random import uniform
import logging
import json
import config

class Comunas():

    def loadComunas(self):
        logging.debug("Entering cargar Comunas")
        try:
            with open('comunas.json') as f:
                self.file = json.load(f)
        except Exception as e:
            logging.error("Error loading comunas JSON: " + str(e), exc_info=True)

    def createPolygons(self):
        try:
            self.comunas = []
            for f in self.file:
                logging.debug("Processing comuna # " + f['numero'])
                #Creating Polygons for each Comuna
                l = []
                for p in f['poligono']:
                    l.append(tuple((float(p[0]), float(p[1]))))
                    logging.debug(str(l))
                pp = Polygon(l)
                self.comunas.append(pp)
            logging.debug("Total of comunas correctly processed: " + str(len(self.comunas)))
        except Exception as e:
            logging.error("Error creating Comuna polygons: " + str(e), exc_info=True)

    def createPoints(self, _total):
        try:
            self.puntos = []
            for i in range(len(self.comunas)):
                ratio = config.PORCENTAJES[i]
                limit = int(_total*ratio)
                logging.debug("Generating " + str(limit) + " points for the Comuna # : " + str(i))
                for _ in range(int(_total*ratio)):
                    self.puntos.append(self.randPoint(self.comunas[i]))
        except Exception as e:
            logging.error("Error creating Comuna random points: " + str(e), exc_info=True)
    
    def createClusters(self):
        try:
            puntos = self.convertPoint(self.puntos)
            kmeans = KMeans(n_clusters=config.NUMERO_ESTACIONES, random_state=0, init='k-means++').fit(puntos)
            logging.debug("Acá están las coordenadas estimadas de cada estación:")
            self.centros = kmeans.cluster_centers_
            return self.centros
        except Exception as e:
            logging.error("Error calculating the clusters: " + str(e), exc_info=True)

    def calculateMinimalRoads(self):
        try:
            matrix = np.linalg.norm(self.centros - self.centros[:,None], axis=-1)
            logging.debug(matrix)

            X = csr_matrix(matrix)
            tree = minimum_spanning_tree(X)
            self.distancias = tree.toarray()
            self.caminos = self.distancias.copy()
            for i in range(len(self.distancias)):
                for j in range(len(self.distancias)):
                    if self.distancias[i][j] > 0.0:
                        self.caminos[i][j] = 1
            logging.debug(self.caminos)
        except Exception as e:
            logging.error("Error calcularing the MSP: " + str(e), exc_info=True)

    def roadsDraw(self):
        try:
            l = []
            for i in range(len(self.caminos)):
                for j in range(len(self.caminos)):
                    if self.caminos[i][j] == 1:
                        temp = [i,j]
                        l.append(temp)
            logging.debug("List of nodes connected: " + str(l))
            return l
        except Exception as e:
            logging.error("Error calcularing the roads for draw: " + str(e), exc_info=True)


    """
    Auxiliar Functions
    """
    def randPoint(self, poly):
        try:
            xrand = uniform(poly.bounds[0], poly.bounds[2])
            yrand = uniform(poly.bounds[1], poly.bounds[3])
            rp = Point(xrand,yrand)
            if poly.contains(rp):
                return rp
            else:
                return self.randPoint(poly)
        except Exception as e:
            logging.error("Error calculating random the points: " + str(e), exc_info=True)
            

    def convertPoint(self, puntos):
        try:
            l = []
            for p in puntos:
                temp = [p.x, p.y]
                l.append(temp)
            return l
        except Exception as e:
            logging.error("Error converting Points into array of floats: " + str(e), exc_info=True)

