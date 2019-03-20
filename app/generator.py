import json
import logging
import logging

class Generator():

    def createComuna(self, _n, _l):
        logging.debug("Entering createComuna")
        try: 
            self.comuna = {}
            self.comuna['numero'] = _n
            self.comuna['poligono'] = _l
        except Exception as e:
            logging.error("Error creating the Comuna object: " + str(e), exc_info=True)


    def export(self):
        try:
            with open('comunas.json', 'a') as fp:
                json.dump(self.comuna, fp)
        except Exception as e:
            logging.error("Error exporting the Comuna files: " + str(e), exc_info=True)
