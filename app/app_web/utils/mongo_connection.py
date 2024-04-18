from pymongo import MongoClient

class MongoDBConnection: 

    def __init__(self):

        self._conn = MongoClient('mongodb', tlsAllowInvalidCertificates=True)
        self._db = self._conn['Sustainability']
    
        self._col_evaluation  = self._db['sustainabilityEvaluation']


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def client(self):
        return self._conn

    def close(self):
        self.client.close()


