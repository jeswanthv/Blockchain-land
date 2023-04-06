from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class ReviewerModel:
    def __init__(self, reviewerID = '',reviewerName = '',isActive = False):
        self.reviewerID = reviewerID
        self.reviewerName = reviewerName
        self.isActive = isActive
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Reviewer ORDER BY reviewerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ReviewerModel(dbrow[0],dbrow[1],dbrow[2])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT reviewerID, reviewerName FROM Reviewer ORDER BY reviewerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ReviewerModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Reviewer WHERE reviewerID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ReviewerModel(dbrow[0],dbrow[1],dbrow[2])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.reviewerID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Reviewer (reviewerID,reviewerName,isActive) VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (obj.reviewerID,obj.reviewerName,obj.isActive))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Reviewer SET reviewerName = ?,isActive = ? WHERE reviewerID = ?"
        cursor.execute(sqlcmd1,  (obj.reviewerName,obj.isActive,obj.reviewerID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Reviewer WHERE reviewerID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

