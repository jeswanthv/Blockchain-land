from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class SellerModel:
    def __init__(self, sellerID = '',sellerName = '',title = '',address1 = '',address2 = '',city = '',state = '',pincode = '',country = '',emailID = '',mobileNbr = '',addressProofFile = '',photoProofFile = '',emailModel = None):
        self.sellerID = sellerID
        self.sellerName = sellerName
        self.title = title
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.pincode = pincode
        self.country = country
        self.emailID = emailID
        self.mobileNbr = mobileNbr
        self.addressProofFile = addressProofFile
        self.photoProofFile = photoProofFile
        self.emailModel = emailModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Seller ORDER BY sellerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = SellerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT sellerID, sellerName FROM Seller ORDER BY sellerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = SellerModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Seller WHERE sellerID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = SellerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.sellerID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Seller (sellerID,sellerName,title,address1,address2,city,state,pincode,country,emailID,mobileNbr,addressProofFile,photoProofFile) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.sellerID,obj.sellerName,obj.title,obj.address1,obj.address2,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.mobileNbr,obj.addressProofFile,obj.photoProofFile))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Seller SET sellerName = ?,title = ?,address1 = ?,address2 = ?,city = ?,state = ?,pincode = ?,country = ?,emailID = ?,mobileNbr = ?,addressProofFile = ?,photoProofFile = ? WHERE sellerID = ?"
        cursor.execute(sqlcmd1,  (obj.sellerName,obj.title,obj.address1,obj.address2,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.mobileNbr,obj.addressProofFile,obj.photoProofFile,obj.sellerID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Seller WHERE sellerID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

