from flask import Flask, jsonify, request, session, Response
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
import random
import os
import pandas as pd
from pydrive.drive import GoogleDrive
import os

from google_drive import GoogleDrive
from helper_functions import empty_the_folder
from database import Database
from database import MS
# --------------------------------------------------------- # 

app = Flask(__name__)
CORS(app, supports_credentials=True)

oauth = OAuth(app)

USER = 'root'
PASSWORD = '******'
DATABASE = 'dep'
HOST = 'localhost'

DB = Database(user = USER , password=PASSWORD, database= DATABASE, host = HOST, app = app)

success_code = Response(status=200)
failiure_code = Response(status=400)

access_token = "ya29.a0Aa4xrXPfOzBn-6ZfDM18ySPUnCdY7b8akhyOtDPEKylmsRAD7GaFRnZIhyjiMGG1TZHQTeC7awqPfH3EHIyxawMZjx3ERLnmZaXDfZDgzI_fNvDFFltvfJXW7sb5K427IkdL3l3TsjRUu-M7GszaHJ9wo4X7aCgYKATASARISFQEjDvL9IDANAyXVGEd_q4jAqG0mCg0163"

GD = GoogleDrive(access_token)

@app.route('/login_oauth', methods = ['POST'])
def login_oauth():
    user_info = request.json["user_info"]
    email = user_info['email']
    if DB.is_valid_email(email):
        session['logged_in'] = True
        session['user_info'] = user_info
        session.permanent = True
        data = DB.get_user_data(email)
        return jsonify(data)
    else:
        return failiure_code

def send_otp(email):
    
    OTP = random.randint(10**5,10**6-1)
    session['otp'] = OTP

    query = "INSERT INTO otp (email_id, otp) VALUES('%s', '%s') ON DUPLICATE KEY UPDATE email_id = '%s' , otp = '%s'"%(email, OTP, email, OTP)
    DB.executeUpdate(query)
    MS.send_otp(email,OTP)

@app.route('/login_otp', methods = ['POST'])
def login_otp():
    email = request.json['email']
    if DB.is_valid_email(email):
        send_otp(email)
        session['user_info'] = dict()
        session['user_info']['email'] = email
        return success_code
    else:
        return failiure_code

def validateOtp(otp , email):
    query = "SELECT otp FROM otp WHERE email_id = '%s'"%(email)
    data = DB.executeSelect(query)
    data = list(data)    
    return (data[0][0] == otp)

@app.route('/validate_otp' , methods = ['POST'])
def validate_otp():
    otp = request.json['otp']
    email = session['user_info']['email']

    if validateOtp(otp , email):
        
        session['logged_in'] = True
        session['user_info']['imageUrl'] = ""

        return success_code
    else:
        session.clear()
        return failiure_code

@app.route('/@me')
def get_current_user():
    if 'user_info' in session:
        email = session['user_info']['email']
        user_data = DB.get_user_data(email)
        user_data = user_data[0]

        data = dict()
        data['name'] = user_data[1]
        data['email'] = user_data[2]
        data['level'] = user_data[3]
        data['department'] = user_data[4]
        data['total_leaves'] = user_data[5]
        data['av_leaves'] = user_data[6]
        if 'imageUrl' in 'user_info':
            data['imageURL'] = session['user_info']['imageUrl']
        else:
            data['imageURL'] = ""

        return jsonify(data)
    else:
        return jsonify("")

@app.route('/leave_application', methods=['POST'])
def leave_application():
    dataa = request.form.copy()
    if 'docc' in request.files:
        dataa['docc'] = request.files['docc']
        ff = dataa['docc']
        file_name = 'doc{}.pdf'.format(DB.findNextLeaveID())
        ff.save(os.getcwd()+'\\files\\' + file_name)
        dataa['docc'] = os.getcwd()+'.\\files\\' + file_name
        attached_documents = GD.uploadFile(dataa['docc'], file_name)
        dataa['attached_documents'] = attached_documents
        empty_the_folder(os.getcwd()+'\\files')

    else:
        dataa['docc'] = ""
        dataa['attached_documents'] = ""
    status = DB.insert_leave(dataa)
    if status:
        return success_code
    else:
        return failiure_code
        
@app.route('/dashboard',methods = ["POST","GET"])
def dashboard():
    data = DB.get_user_dic(session['user_info']['email'])
    return jsonify(data)

@app.route('/fetchLeaves', methods = ['POST'])
def fetchLeaves():
    email = session['user_info']['email']
    data = DB.get_user_data(email)[0]
    user_id = data[0]

    query = "SELECT * FROM leaves WHERE user_id = %s"%(user_id)
    data = DB.executeSelect(query)
    payload = []
    for i in data:
        # department, user_id, nature, purpose, is_station, request_date, start_date, end_date, duration, status, level
        content = {'id': i[0], 'department': i[1], 'user_id': i[2],'nature': i[3],'purpose': i[4],'is_station': i[5],'request_date': i[6],'start_date': i[7],'end_date': i[8], 'authority_comment': i[9], 'duration': i[10],'status': i[11],'level': i[12], 'attached_documents': i[13]}
        user_id = i[2]

        query = 'SELECT email_id FROM user WHERE user_id = %s'%(user_id)
        data = DB.executeSelect(query)
        email = data[0][0]
        cur_user = DB.get_user_dic(email)
        content['email'] = cur_user['email']
        content['name'] = cur_user['name']
        nature = i[3]
        c_st1 = "Total " + nature + 's'
        c_st2 = "Taken " + nature + 's'
        nature = nature.lower().split()
        nature = '_'.join(nature)
        u_st1 = 'total_' + nature + 's'
        u_st2 = 'taken_' + nature + 's'
        
        content[c_st1] = cur_user[u_st1]
        content[c_st2] = cur_user[u_st2]
        content["key1"] = c_st1
        content["key2"] = c_st2
        
        payload.append(content)

    return jsonify(result=payload)

@app.route('/check_leaves',methods = ['GET','POST'])
def check_leaves():
    email = session['user_info']['email']
    data = DB.get_user_dic(email)
    user_id = data['user_id']
    department = data['department']
    position = data['position']

    query = ""
    if position == "hod":
        query = 'SELECT * FROM leaves WHERE\
            department = %s and level = %s'%(department, "Faculty")

    elif position == 'dean':
        query = 'SELECT * FROM leaves'

    elif position == 'establishment':
        query = "SELECT * FROM leaves"

    leaves = DB.executeSelect(query)

    payload = []

    for i in leaves:
        content = {'id': i[0], 'department': i[1], 'user_id': i[2],'nature': i[3],'purpose': i[4],'is_station': i[5],'request_date': i[6],'start_date': i[7],'end_date': i[8], 'authority_comment': i[9], 'duration': i[10],'status': i[11],'level': i[12], 'attached_documents': i[13]}
        user_id = i[2]

        query = 'SELECT email_id FROM user WHERE user_id = %s'%(user_id)
        data = DB.executeSelect(query)
        email = data[0][0]
        cur_user = DB.get_user_dic(email)
        content['email'] = cur_user['email']
        content['name'] = cur_user['name']
        nature = i[3]
        c_st1 = "Total " + nature + 's'
        c_st2 = "Taken " + nature + 's'
        nature = nature.lower().split()
        nature = '_'.join(nature)
        u_st1 = 'total_' + nature + 's'
        u_st2 = 'taken_' + nature + 's'
        
        content[c_st1] = cur_user[u_st1]
        content[c_st2] = cur_user[u_st2]
        content["key1"] = c_st1
        content["key2"] = c_st2
        if position == 'dean':
            if (nature=="casual_leave" or nature=="restricted_leave") and (content['level'] == 'hod'):
                payload.append(content)
            elif nature == "casual_leave" or nature == "restricted_leave":
                continue
            elif content['status'] == 'Approved By Hod' or content['status'] == 'Approved By Dean' or content['status'] == 'Disapproved By Dean':
                payload.append(content)
        elif position == 'hod':
            payload.append(content)
        elif position == 'establishment':
            if content['status'] == 'Approved By Hod':
                payload.append(content)

    return jsonify(result = payload)

@app.route('/approve_leave', methods = ['POST'])
def approve_leave():
    leave_id = request.json['leave_id']

    if "approved" not in session:
        session['approved'] = {}

    if leave_id in session['approved']:
        return success_code

    session['approved'][leave_id] = 1
    user = DB.get_user_dic(session['user_info']['email'])

    if user["position"] == "hod":
        query = "UPDATE leaves SET status = 'Approved By Hod' WHERE leave_id = %s"%(leave_id)
        DB.executeUpdate(query)

    elif user["position"] == "dean":
        query = "UPDATE leaves SET status = 'Approved By Dean' WHERE leave_id = %s"%(leave_id)
        DB.executeUpdate(query)

    query = "Select user_id, nature, duration from leaves where leave_id = %s"%(leave_id)
    data = DB.executeSelect(query)
    user_id = data[0]
    nature = data[1]
    duration = float(data[2])

    nature = nature.lower().split()
    nature = '_'.join(nature)
    u_st2 = 'taken_' + nature + 's'
    query = "Select %s from user where user_id = %s" % (u_st2, user_id)

    data = DB.executeSelect(query)
    taken_cnt = float(data[0]) + duration
    if (nature == "casual_leave" or nature == "restricted_leave") and (user['position']=='hod' or user['position']=='dean'):
        query = "Update user set %s = %s where user_id = %s" % (u_st2, taken_cnt, user_id)
        DB.executeUpdate(query)

    elif nature != "casual_leave" and nature != "restricted_leave" and user['position']=='dean':
        query = "Update user set %s = %s where user_id = %s" % (u_st2, taken_cnt, user_id)
        DB.executeUpdate(query)
    # send_update_mail(leave_id)
    return success_code

@app.route('/disapprove_leave', methods = ['POST'])
def disapprove_leave():
    leave_id = request.json['leave_id']
    query = "UPDATE leaves SET status = 'Disapproved By Hod' WHERE leave_id = %s"%(leave_id)
    DB.executeUpdate(query)
    return success_code

@app.route('/add_comment', methods = ['POST'])
def add_comment():
    leave_id = request.json['leave_id']
    comment = request.json['comment']
    query = "UPDATE leaves SET authority_comment = %s WHERE leave_id = %s"%(comment, leave_id)
    DB.executeUpdate(query)
    return success_code

@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    file = request.files['file']
    file.save("data.xlsx")
    dfs = pd.read_excel("data.xlsx", sheet_name=None)
    d = dfs["Sheet1"]
    DB.initialize()
    for i in range (len(d)):
        query = "insert into user(name, email_id, position, department, total_casual_leaves, taken_casual_leaves, total_restricted_leaves, taken_restricted_leaves, total_earned_leaves, taken_earned_leaves, total_vacation_leaves, taken_vacation_leaves, total_special_leaves, taken_special_leaves, total_commuted_leaves, taken_commuted_leaves, total_hospital_leaves, taken_hospital_leaves, total_study_leaves, taken_study_leaves, total_childcare_leaves, taken_childcare_leaves) values ('%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (d.iloc[i,0], d.iloc[i,1], d.iloc[i,2], d.iloc[i,3], d.iloc[i,4], d.iloc[i,5], d.iloc[i,6], d.iloc[i,7], d.iloc[i,8], d.iloc[i,9], d.iloc[i,10], d.iloc[i,11], d.iloc[i,12], d.iloc[i,13], d.iloc[i,14], d.iloc[i,15], d.iloc[i,16], d.iloc[i,17], d.iloc[i,18], d.iloc[i,19], d.iloc[i,20], d.iloc[i,21])
        DB.executeUpdate(query)

    return success_code

@app.route('/logout')
def logout():
    session.clear()
    return success_code

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
