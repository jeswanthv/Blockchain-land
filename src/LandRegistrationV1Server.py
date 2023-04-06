
from flask import Flask, request, render_template, redirect, url_for
import os
import pyodbc
import uuid
import time
from datetime import datetime
from Constants import connString

from BuyerModel import BuyerModel
from LandTransactionModel import LandTransactionModel
from RegistrarModel import RegistrarModel
from RegistrationOfficeModel import RegistrationOfficeModel
from ReviewerModel import ReviewerModel
from RoleModel import RoleModel
from SellerModel import SellerModel
from UsersModel import UsersModel




app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""
role_object = None
message = ""
msgType = ""
uploaded_file_name = ""

def initialize():
    global message, msgType
    message = ""
    msgType = ""

def process_role(option_id):

    
    if option_id == 0:
        if role_object.canBuyer == False:
            return False
        
    if option_id == 1:
        if role_object.canLandTransaction == False:
            return False
        
    if option_id == 2:
        if role_object.canRegistrar == False:
            return False
        
    if option_id == 3:
        if role_object.canRegistrationOffice == False:
            return False
        
    if option_id == 4:
        if role_object.canReviewer == False:
            return False
        
    if option_id == 5:
        if role_object.canRole == False:
            return False
        
    if option_id == 6:
        if role_object.canSeller == False:
            return False
        
    if option_id == 7:
        if role_object.canUsers == False:
            return False
        

    return True



@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")

@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid, role_object
    emailid = request.form["emailid"]
    password = request.form["password"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + password + "' AND isActive = 1";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template("Login.html", processResult="Invalid Credentials")
    user_id = row[0]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template("Login.html", processResult="Invalid Role")

    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7], row2[8], row2[9])

    return render_template("Dashboard.html")


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template("ChangePassword.html", msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template("ChangePassword.html", msg="New Password and Confirm Password are NOT same")

    conn2 = pyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE Users SET password = '" + newPassword + "' WHERE emailid = '" + emailid + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    return render_template("Dashboard.html")


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)


@app.route("/BuyerListing")
def Buyer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canBuyer = process_role(0)

    if canBuyer == False:
        message = "You Don't Have Permission to Access Buyer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = BuyerModel.get_all()

    return render_template("BuyerListing.html", records=records)

@app.route("/BuyerOperation")
def Buyer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canBuyer = process_role(0)

    if not canBuyer:
        message = "You Don't Have Permission to Access Buyer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = BuyerModel("", "")

    Buyer = BuyerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = BuyerModel.get_by_id(unique_id)

    return render_template("BuyerOperation.html", row=row, operation=operation, Buyer=Buyer, )

@app.route("/ProcessBuyerOperation", methods=["POST"])
def process_Buyer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canBuyer = process_role(0)
    if not canBuyer:
        message = "You Don't Have Permission to Access Buyer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = BuyerModel("", "")

    if operation != "Delete":
       obj.buyerID = request.form['buyerID']
       obj.buyerName = request.form['buyerName']
       obj.title = request.form['title']
       obj.address1 = request.form['address1']
       obj.address2 = request.form['address2']
       obj.city = request.form['city']
       obj.state = request.form['state']
       obj.pincode = request.form['pincode']
       obj.country = request.form['country']
       obj.emailID = request.form['emailID']
       obj.mobileNbr = request.form['mobileNbr']
       if len(request.files) != 0 :
        
                file = request.files['addressProofFile']
                if file.filename != '':
                    addressProofFile = file.filename
                    obj.addressProofFile = addressProofFile
                    f = os.path.join('static/UPLOADED_FILES', addressProofFile)
                    file.save(f)
                else:
                    obj.addressProofFile = request.form['haddressProofFile']
                
                file = request.files['photoProofFile']
                if file.filename != '':
                    photoProofFile = file.filename
                    obj.photoProofFile = photoProofFile
                    f = os.path.join('static/UPLOADED_FILES', photoProofFile)
                    file.save(f)
                else:
                    obj.photoProofFile = request.form['hphotoProofFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.buyerID = request.form["buyerID"]
        obj.update(obj)

    if operation == "Delete":
        buyerID = request.form["buyerID"]
        obj.delete(buyerID)


    return redirect(url_for("Buyer_listing"))
                    
@app.route("/LandTransactionListing")
def LandTransaction_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canLandTransaction = process_role(1)

    if canLandTransaction == False:
        message = "You Don't Have Permission to Access LandTransaction"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = LandTransactionModel.get_all()

    return render_template("LandTransactionListing.html", records=records)

@app.route("/LandTransactionOperation")
def LandTransaction_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canLandTransaction = process_role(1)

    if not canLandTransaction:
        message = "You Don't Have Permission to Access LandTransaction"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = LandTransactionModel("", "")

    LandTransaction = LandTransactionModel.get_all()
    seller_list = SellerModel.get_name_id()
    buyer_list = BuyerModel.get_name_id()
    registrationOffice_list = RegistrationOfficeModel.get_name_id()
    reviewer_list = ReviewerModel.get_name_id()
    registrar_list = RegistrarModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = LandTransactionModel.get_by_id(unique_id)

    return render_template("LandTransactionOperation.html", row=row, operation=operation, LandTransaction=LandTransaction, seller_list = seller_list,buyer_list = buyer_list,registrationOffice_list = registrationOffice_list,reviewer_list = reviewer_list,registrar_list = registrar_list)

@app.route("/ProcessLandTransactionOperation", methods=["POST"])
def process_LandTransaction_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canLandTransaction = process_role(1)
    if not canLandTransaction:
        message = "You Don't Have Permission to Access LandTransaction"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = LandTransactionModel("", "")

    if operation != "Delete":
       obj.transactionID = request.form['transactionID']
       obj.effDate = request.form['effDate']
       obj.sellerID = request.form['sellerID']
       obj.buyerID = request.form['buyerID']
       obj.registrationOfficeID = request.form['registrationOfficeID']
       obj.reviewerID = request.form['reviewerID']
       obj.registrarID = request.form['registrarID']
       obj.address1 = request.form['address1']
       obj.address2 = request.form['address2']
       obj.place = request.form['place']
       obj.city = request.form['city']
       obj.pincode = request.form['pincode']
       obj.state = request.form['state']
       obj.country = request.form['country']
       obj.area = request.form['area']
       obj.surveyNo = request.form['surveyNo']
       obj.pattaNo = request.form['pattaNo']
       obj.cithaNo = request.form['cithaNo']
       obj.salesAmount = request.form['salesAmount']
       obj.registrationFees = request.form['registrationFees']
       obj.gst = request.form['gst']
       if len(request.files) != 0 :
        
                file = request.files['saleDeedFile']
                if file.filename != '':
                    saleDeedFile = file.filename
                    obj.saleDeedFile = saleDeedFile
                    f = os.path.join('static/UPLOADED_FILES', saleDeedFile)
                    file.save(f)
                else:
                    obj.saleDeedFile = request.form['hsaleDeedFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.transactionID = request.form["transactionID"]
        obj.update(obj)

    if operation == "Delete":
        transactionID = request.form["transactionID"]
        obj.delete(transactionID)


    return redirect(url_for("LandTransaction_listing"))
                    
@app.route("/RegistrarListing")
def Registrar_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRegistrar = process_role(2)

    if canRegistrar == False:
        message = "You Don't Have Permission to Access Registrar"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RegistrarModel.get_all()

    return render_template("RegistrarListing.html", records=records)

@app.route("/RegistrarOperation")
def Registrar_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRegistrar = process_role(2)

    if not canRegistrar:
        message = "You Don't Have Permission to Access Registrar"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RegistrarModel("", "")

    Registrar = RegistrarModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RegistrarModel.get_by_id(unique_id)

    return render_template("RegistrarOperation.html", row=row, operation=operation, Registrar=Registrar, )

@app.route("/ProcessRegistrarOperation", methods=["POST"])
def process_Registrar_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRegistrar = process_role(2)
    if not canRegistrar:
        message = "You Don't Have Permission to Access Registrar"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RegistrarModel("", "")

    if operation != "Delete":
       obj.registrarID = request.form['registrarID']
       obj.registrarName = request.form['registrarName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.registrarID = request.form["registrarID"]
        obj.update(obj)

    if operation == "Delete":
        registrarID = request.form["registrarID"]
        obj.delete(registrarID)


    return redirect(url_for("Registrar_listing"))
                    
@app.route("/RegistrationOfficeListing")
def RegistrationOffice_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRegistrationOffice = process_role(3)

    if canRegistrationOffice == False:
        message = "You Don't Have Permission to Access RegistrationOffice"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RegistrationOfficeModel.get_all()

    return render_template("RegistrationOfficeListing.html", records=records)

@app.route("/RegistrationOfficeOperation")
def RegistrationOffice_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRegistrationOffice = process_role(3)

    if not canRegistrationOffice:
        message = "You Don't Have Permission to Access RegistrationOffice"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RegistrationOfficeModel("", "")

    RegistrationOffice = RegistrationOfficeModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RegistrationOfficeModel.get_by_id(unique_id)

    return render_template("RegistrationOfficeOperation.html", row=row, operation=operation, RegistrationOffice=RegistrationOffice, )

@app.route("/ProcessRegistrationOfficeOperation", methods=["POST"])
def process_RegistrationOffice_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRegistrationOffice = process_role(3)
    if not canRegistrationOffice:
        message = "You Don't Have Permission to Access RegistrationOffice"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RegistrationOfficeModel("", "")

    if operation != "Delete":
       obj.registrationOfficeID = request.form['registrationOfficeID']
       obj.registrationOfficeName = request.form['registrationOfficeName']
       obj.address1 = request.form['address1']
       obj.address2 = request.form['address2']
       obj.city = request.form['city']
       obj.state = request.form['state']
       obj.pincode = request.form['pincode']
       obj.country = request.form['country']
       obj.emailID = request.form['emailID']
       obj.contactNbr = request.form['contactNbr']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.registrationOfficeID = request.form["registrationOfficeID"]
        obj.update(obj)

    if operation == "Delete":
        registrationOfficeID = request.form["registrationOfficeID"]
        obj.delete(registrationOfficeID)


    return redirect(url_for("RegistrationOffice_listing"))
                    
@app.route("/ReviewerListing")
def Reviewer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canReviewer = process_role(4)

    if canReviewer == False:
        message = "You Don't Have Permission to Access Reviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ReviewerModel.get_all()

    return render_template("ReviewerListing.html", records=records)

@app.route("/ReviewerOperation")
def Reviewer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canReviewer = process_role(4)

    if not canReviewer:
        message = "You Don't Have Permission to Access Reviewer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ReviewerModel("", "")

    Reviewer = ReviewerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ReviewerModel.get_by_id(unique_id)

    return render_template("ReviewerOperation.html", row=row, operation=operation, Reviewer=Reviewer, )

@app.route("/ProcessReviewerOperation", methods=["POST"])
def process_Reviewer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canReviewer = process_role(4)
    if not canReviewer:
        message = "You Don't Have Permission to Access Reviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ReviewerModel("", "")

    if operation != "Delete":
       obj.reviewerID = request.form['reviewerID']
       obj.reviewerName = request.form['reviewerName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.reviewerID = request.form["reviewerID"]
        obj.update(obj)

    if operation == "Delete":
        reviewerID = request.form["reviewerID"]
        obj.delete(reviewerID)


    return redirect(url_for("Reviewer_listing"))
                    
@app.route("/RoleListing")
def Role_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(5)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RoleModel.get_all()

    return render_template("RoleListing.html", records=records)

@app.route("/RoleOperation")
def Role_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(5)

    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RoleModel("", "")

    Role = RoleModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RoleModel.get_by_id(unique_id)

    return render_template("RoleOperation.html", row=row, operation=operation, Role=Role, )

@app.route("/ProcessRoleOperation", methods=["POST"])
def process_Role_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRole = process_role(5)
    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RoleModel("", "")

    if operation != "Delete":
       obj.roleID = request.form['roleID']
       obj.roleName = request.form['roleName']
       obj.canRole = 0 
       if request.form.get("canRole") != None : 
              obj.canRole = 1       
       obj.canUsers = 0 
       if request.form.get("canUsers") != None : 
              obj.canUsers = 1       
       obj.canBuyer = 0 
       if request.form.get("canBuyer") != None : 
              obj.canBuyer = 1       
       obj.canLandTransaction = 0 
       if request.form.get("canLandTransaction") != None : 
              obj.canLandTransaction = 1       
       obj.canRegistrar = 0 
       if request.form.get("canRegistrar") != None : 
              obj.canRegistrar = 1       
       obj.canRegistrationOffice = 0 
       if request.form.get("canRegistrationOffice") != None : 
              obj.canRegistrationOffice = 1       
       obj.canReviewer = 0 
       if request.form.get("canReviewer") != None : 
              obj.canReviewer = 1       
       obj.canSeller = 0 
       if request.form.get("canSeller") != None : 
              obj.canSeller = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.roleID = request.form["roleID"]
        obj.update(obj)

    if operation == "Delete":
        roleID = request.form["roleID"]
        obj.delete(roleID)


    return redirect(url_for("Role_listing"))
                    
@app.route("/SellerListing")
def Seller_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canSeller = process_role(6)

    if canSeller == False:
        message = "You Don't Have Permission to Access Seller"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = SellerModel.get_all()

    return render_template("SellerListing.html", records=records)

@app.route("/SellerOperation")
def Seller_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canSeller = process_role(6)

    if not canSeller:
        message = "You Don't Have Permission to Access Seller"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = SellerModel("", "")

    Seller = SellerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = SellerModel.get_by_id(unique_id)

    return render_template("SellerOperation.html", row=row, operation=operation, Seller=Seller, )

@app.route("/ProcessSellerOperation", methods=["POST"])
def process_Seller_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canSeller = process_role(6)
    if not canSeller:
        message = "You Don't Have Permission to Access Seller"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = SellerModel("", "")

    if operation != "Delete":
       obj.sellerID = request.form['sellerID']
       obj.sellerName = request.form['sellerName']
       obj.title = request.form['title']
       obj.address1 = request.form['address1']
       obj.address2 = request.form['address2']
       obj.city = request.form['city']
       obj.state = request.form['state']
       obj.pincode = request.form['pincode']
       obj.country = request.form['country']
       obj.emailID = request.form['emailID']
       obj.mobileNbr = request.form['mobileNbr']
       if len(request.files) != 0 :
        
                file = request.files['addressProofFile']
                if file.filename != '':
                    addressProofFile = file.filename
                    obj.addressProofFile = addressProofFile
                    f = os.path.join('static/UPLOADED_FILES', addressProofFile)
                    file.save(f)
                else:
                    obj.addressProofFile = request.form['haddressProofFile']
                
                file = request.files['photoProofFile']
                if file.filename != '':
                    photoProofFile = file.filename
                    obj.photoProofFile = photoProofFile
                    f = os.path.join('static/UPLOADED_FILES', photoProofFile)
                    file.save(f)
                else:
                    obj.photoProofFile = request.form['hphotoProofFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.sellerID = request.form["sellerID"]
        obj.update(obj)

    if operation == "Delete":
        sellerID = request.form["sellerID"]
        obj.delete(sellerID)


    return redirect(url_for("Seller_listing"))
                    
@app.route("/UsersListing")
def Users_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(7)

    if canUsers == False:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UsersModel.get_all()

    return render_template("UsersListing.html", records=records)

@app.route("/UsersOperation")
def Users_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(7)

    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UsersModel("", "")

    Users = UsersModel.get_all()
    role_list = RoleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UsersModel.get_by_id(unique_id)

    return render_template("UsersOperation.html", row=row, operation=operation, Users=Users, role_list = role_list)

@app.route("/ProcessUsersOperation", methods=["POST"])
def process_Users_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUsers = process_role(7)
    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UsersModel("", "")

    if operation != "Delete":
       obj.userID = request.form['userID']
       obj.userName = request.form['userName']
       obj.emailid = request.form['emailid']
       obj.password = request.form['password']
       obj.contactNo = request.form['contactNo']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       obj.roleID = request.form['roleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.userID = request.form["userID"]
        obj.update(obj)

    if operation == "Delete":
        userID = request.form["userID"]
        obj.delete(userID)


    return redirect(url_for("Users_listing"))
                    


import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM LandTransaction WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM LandTransaction WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM LandTransaction WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    if blocksCreated != 0:
        connx = pyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM LandTransaction WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        if dbrowx:
            uniqueID = dbrowx[25]
            conny = pyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM LandTransaction WHERE sequenceNumber < '" + str(uniqueID) + "' ORDER BY sequenceNumber DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM LandTransaction WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[25])

        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE LandTransaction SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE sequenceNumber = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM LandTransaction WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM LandTransaction ORDER BY sequenceNumber DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = LandTransactionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18],dbrow[19],dbrow[20],dbrow[21],dbrow[22],dbrow[23],dbrow[24],dbrow[25])
        records.append(row)
    return render_template('BlockChainReport.html', records=records)         

            

 
if __name__ == "__main__":
    app.run()

                    