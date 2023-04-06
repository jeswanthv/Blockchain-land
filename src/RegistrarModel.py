from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class RegistrarModel:
    def __init__(self, registrarID = '',registrarName = '',isActive = False):
        self.registrarID = registrarID
        self.registrarName = registrarName
        self.isActive = isActive
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Registrar ORDER BY registrarName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RegistrarModel(dbrow[0],dbrow[1],dbrow[2])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT registrarID, registrarName FROM Registrar ORDER BY registrarName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RegistrarModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Registrar WHERE registrarID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = RegistrarModel(dbrow[0],dbrow[1],dbrow[2])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.registrarID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Registrar (registrarID,registrarName,isActive) VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (obj.registrarID,obj.registrarName,obj.isActive))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Registrar SET registrarName = ?,isActive = ? WHERE registrarID = ?"
        cursor.execute(sqlcmd1,  (obj.registrarName,obj.isActive,obj.registrarID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Registrar WHERE registrarID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

