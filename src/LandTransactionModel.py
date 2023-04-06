from Constants import connString
import pyodbc
import datetime
import uuid
import time    
from Constants import contract_address
from web3 import Web3, HTTPProvider
import json
import pprint
        
class LandTransactionModel:
    def __init__(self, transactionID = '',effDate = None,sellerID = '',buyerID = '',registrationOfficeID = '',reviewerID = '',registrarID = '',address1 = '',address2 = '',place = '',city = '',pincode = '',state = '',country = '',area = '',surveyNo = '',saleDeedFile = '',pattaNo = '',cithaNo = '',salesAmount = 0,registrationFees = 0,gst = 0,isBlockChainGenerated = False,hash = '',prevHash = '',sequenceNumber = 0,sellerModel = None,buyerModel = None,registrationOfficeModel = None,reviewerModel = None,registrarModel = None):
        self.transactionID = transactionID
        self.effDate = effDate
        self.sellerID = sellerID
        self.buyerID = buyerID
        self.registrationOfficeID = registrationOfficeID
        self.reviewerID = reviewerID
        self.registrarID = registrarID
        self.address1 = address1
        self.address2 = address2
        self.place = place
        self.city = city
        self.pincode = pincode
        self.state = state
        self.country = country
        self.area = area
        self.surveyNo = surveyNo
        self.saleDeedFile = saleDeedFile
        self.pattaNo = pattaNo
        self.cithaNo = cithaNo
        self.salesAmount = salesAmount
        self.registrationFees = registrationFees
        self.gst = gst
        self.isBlockChainGenerated = isBlockChainGenerated
        self.hash = hash
        self.prevHash = prevHash
        self.sequenceNumber = sequenceNumber
        self.sellerModel = sellerModel
        self.buyerModel = buyerModel
        self.registrationOfficeModel = registrationOfficeModel
        self.reviewerModel = reviewerModel
        self.registrarModel = registrarModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM LandTransaction ORDER BY effDate"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = LandTransactionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18],dbrow[19],dbrow[20],dbrow[21],dbrow[22],dbrow[23],dbrow[24],dbrow[25])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT transactionID, effDate FROM LandTransaction ORDER BY effDate"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = LandTransactionModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM LandTransaction WHERE transactionID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = LandTransactionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18],dbrow[19],dbrow[20],dbrow[21],dbrow[22],dbrow[23],dbrow[24],dbrow[25])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.transactionID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO LandTransaction (transactionID,effDate,sellerID,buyerID,registrationOfficeID,reviewerID,registrarID,address1,address2,place,city,pincode,state,country,area,surveyNo,saleDeedFile,pattaNo,cithaNo,salesAmount,registrationFees,gst,isBlockChainGenerated,hash,prevHash) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.transactionID,datetime.datetime.strptime(obj.effDate.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.sellerID,obj.buyerID,obj.registrationOfficeID,obj.reviewerID,obj.registrarID,obj.address1,obj.address2,obj.place,obj.city,obj.pincode,obj.state,obj.country,obj.area,obj.surveyNo,obj.saleDeedFile,obj.pattaNo,obj.cithaNo,obj.salesAmount,obj.registrationFees,obj.gst,obj.isBlockChainGenerated,obj.hash,obj.prevHash))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../LandRegistration-Truffle/build/contracts/LandTransactionContract.json'
        deployed_contract_address = contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.sellerID, obj.buyerID, obj.area, obj.saleDeedFile, int(obj.salesAmount)).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE LandTransaction SET effDate = ?,sellerID = ?,buyerID = ?,registrationOfficeID = ?,reviewerID = ?,registrarID = ?,address1 = ?,address2 = ?,place = ?,city = ?,pincode = ?,state = ?,country = ?,area = ?,surveyNo = ?,saleDeedFile = ?,pattaNo = ?,cithaNo = ?,salesAmount = ?,registrationFees = ?,gst = ?,isBlockChainGenerated = ?,hash = ?,prevHash = ? WHERE transactionID = ?"
        cursor.execute(sqlcmd1,  (datetime.datetime.strptime(obj.effDate.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.sellerID,obj.buyerID,obj.registrationOfficeID,obj.reviewerID,obj.registrarID,obj.address1,obj.address2,obj.place,obj.city,obj.pincode,obj.state,obj.country,obj.area,obj.surveyNo,obj.saleDeedFile,obj.pattaNo,obj.cithaNo,obj.salesAmount,obj.registrationFees,obj.gst,obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.transactionID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM LandTransaction WHERE transactionID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

