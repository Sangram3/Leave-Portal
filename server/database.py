from flask import  session
import smtplib
from flaskext.mysql import MySQL
from mail_service import MailService

MS = MailService()

class Database:
    def __init__(self , user , password , database , host , app) -> None:
        self.app = app
        self.user = user
        self.password = password
        self.database = database
        self.host = host

        self.app.config['MYSQL_DATABASE_USER'] = 'root'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = 'San@2017'
        self.app.config['MYSQL_DATABASE_DB'] = 'dep'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.db = MySQL(app)


    def is_valid_email(self,email_id):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE email_id = %s",(email_id))
        data = cursor.fetchall()
        if not data:
            session.clear()
            return 0
        else:
            return 1

    def get_user_data(self,email_id):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE email_id = %s",(email_id))
        data = cursor.fetchall()
        return data

    def insert_leave(self,l):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT user_id, department, position FROM user WHERE email_id = %s",(l['email']))
        data = cursor.fetchall()
        user_id = data[0][0]
        department = data[0][1]
        position = data[0][2]
        
        cursor.execute("INSERT INTO leaves\
            (department, user_id, nature, purpose, is_station, request_date, start_date, end_date, duration, status, level,file_uploaded) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
            (department, user_id, l['nature'], l['purpose'], l['isStation'], l['rdate'], l['sdate'], l['edate'], l['duration'], 'Pending', position,l['attached_documents']))
        connect.commit()
        return 1

    def initialize(self):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("drop table if exists leaves")
        cursor.execute("drop table if exists user")
        connect.commit()
        cursor.execute("CREATE TABLE user(      \
            user_id INT PRIMARY KEY AUTO_INCREMENT, \
            name VARCHAR(30),                       \
            email_id VARCHAR(50) UNIQUE,            \
            position VARCHAR(30),                   \
            department VARCHAR(10),                 \
            total_casual_leaves INTEGER,            \
            taken_casual_leaves INTEGER,            \
            total_restricted_leaves INTEGER,        \
            taken_restricted_leaves INTEGER,        \
            total_earned_leaves INTEGER,            \
            taken_earned_leaves INTEGER,            \
            total_vacation_leaves INTEGER,          \
            taken_vacation_leaves INTEGER,          \
            total_special_leaves INTEGER,           \
            taken_special_leaves INTEGER,           \
            total_commuted_leaves INTEGER,          \
            taken_commuted_leaves INTEGER,          \
            total_hospital_leaves INTEGER,          \
            taken_hospital_leaves INTEGER,          \
            total_study_leaves INTEGER,             \
            taken_study_leaves INTEGER,             \
            total_childcare_leaves INTEGER,         \
            taken_childcare_leaves INTEGER          \
        );")

        cursor.execute("CREATE TABLE leaves(        \
            leave_id INT PRIMARY KEY AUTO_INCREMENT,    \
            department VARCHAR(10),                     \
            user_id INT,                                \
            nature VARCHAR(100),                        \
            purpose VARCHAR(200),                       \
            is_station VARCHAR(10),                     \
            request_date TIMESTAMP,                     \
            start_date TIMESTAMP,                       \
            end_date TIMESTAMP,                         \
            authority_comment VARCHAR(200),             \
            duration INT,                               \
            status VARCHAR(30),                         \
            level VARCHAR(30),                          \
            file_uploaded VARCHAR(100),                 \
            FOREIGN KEY (user_id) REFERENCES user(user_id)\
        );")
        connect.commit()
    
    

    def get_user_dic(self,email):
        data = self.get_user_data(email)[0]
        dic = {}
        dic['user_id'] = data[0]
        dic['name'] = data[1]
        dic['email'] = data[2]
        dic['position'] = data[3]
        dic['department'] = data[4]
        dic['total_casual_leaves'] = data[5]
        dic['taken_casual_leaves'] = data[6]
        dic['total_restricted_leaves'] = data[7]
        dic['taken_restricted_leaves'] = data[8]
        dic['total_earned_leaves'] = data[9]
        dic['taken_earned_leaves'] = data[10]
        dic['total_vacation_leaves'] = data[11]
        dic['taken_vacation_leaves'] = data[12]
        dic['total_special_leaves'] = data[13]
        dic['taken_special_leaves'] = data[14]
        dic['total_commuted_leaves'] = data[15]
        dic['taken_commuted_leaves'] = data[16]
        dic['total_hospital_leaves'] = data[17]
        dic['taken_hospital_leaves'] = data[18]
        dic['total_study_leaves'] = data[19]
        dic['taken_study_leaves'] = data[20]
        dic['total_childcare_leaves'] = data[21]
        dic['taken_childcare_leaves'] = data[22]

        return dic
    
    
    def send_update_mail(self,leave_id):

        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT duration,request_date,start_date,end_date,status,authority_comment,user_id,nature FROM leaves WHERE leave_id = %s',(leave_id))
        tmp = cursor.fetchall()[0]
        duration = tmp[0]
        request_date = tmp[1]
        start_date = tmp[2]
        end_date = tmp[3]
        status = tmp[4]
        authority_comment = tmp[5]    
        user_id = tmp[6]
        nature = tmp[7]

        cursor.execute('SELECT total_casual_leaves,taken_casual_leaves,email_id,name FROM user WHERE user_id = %s',(user_id))
        tmp = cursor.fetchall()[0]
        total_leaves = tmp[0]
        taken_leaves = tmp[1]
        email_id = tmp[2]
        name = tmp[3]
        remaining_leaves = str(float(total_leaves) - float(taken_leaves))
        msg = """Hi {}, your leave application for {} has been {}.\n\n\
        Leave Information: \n\
            Leave Id - {} \n\
            Duration - {} days \n\
            Request Date - {} \n\
            Start Date - {} \n\
            End Date - {} \n\
            Status - {} \n\
            Authority Comment - {} \n\n\
        Updated Leaves Count: \n\
            Total Casual Leaves - {} days \n\
            Taken Casual Leaves - {} days \n\
            Remaining Casual Leaves - {} days \n\
        """.format(name,nature,status,leave_id,duration,request_date,start_date,end_date,status,authority_comment,total_leaves,taken_leaves,remaining_leaves)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leavemanagementiitropar@gmail.com", "gdpzrofppayyvscw")
        server.sendmail('IIT Ropar Leave OTP',email_id,msg)


    def findNextLeaveID(self):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("select max(leave_id) from leaves;")
        data = cursor.fetchall()
        if not data:
            return 1    
        if not data[0]:
            return 1
        try:
            return data[0][0]+1
        except:
            return 1

    def executeUpdate(self,query):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        
    def executeSelect(self,query):
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data


