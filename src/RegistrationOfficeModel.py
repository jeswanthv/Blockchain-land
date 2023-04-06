from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class RegistrationOfficeModel:
    def __init__(self, registrationOfficeID = '',registrationOfficeName = '',address1 = '',address2 = '',city = '',state = '',pincode = '',country = '',emailID = '',contactNbr = '',emailModel = None):
        self.registrationOfficeID = registrationOfficeID
        self.registrationOfficeName = registrationOfficeName
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.pincode = pincode
        self.country = country
        self.emailID = emailID
        self.contactNbr = contactNbr
        self.emailModel = emailModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM RegistrationOffice ORDER BY registrationOfficeName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RegistrationOfficeModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT registrationOfficeID, registrationOfficeName FROM RegistrationOffice ORDER BY registrationOfficeName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RegistrationOfficeModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM RegistrationOffice WHERE registrationOfficeID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = RegistrationOfficeModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.registrationOfficeID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO RegistrationOffice (registrationOfficeID,registrationOfficeName,address1,address2,city,state,pincode,country,emailID,contactNbr) VALUES(?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.registrationOfficeID,obj.registrationOfficeName,obj.address1,obj.address2,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.contactNbr))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE RegistrationOffice SET registrationOfficeName = ?,address1 = ?,address2 = ?,city = ?,state = ?,pincode = ?,country = ?,emailID = ?,contactNbr = ? WHERE registrationOfficeID = ?"
        cursor.execute(sqlcmd1,  (obj.registrationOfficeName,obj.address1,obj.address2,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.contactNbr,obj.registrationOfficeID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM RegistrationOffice WHERE registrationOfficeID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

