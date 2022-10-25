from flask import  session
from flaskext.mysql import MySQL
from mail_service import MS

class Database:
    """
        Database class handles all the queries related to database.
        Singleton class, one instance created per session.
        Takes, username, password, database name, host, and flask app instance as input
    """
    def __init__(self , user , password , database , host , app) -> None:
        self.app = app
        self.user = user
        self.password = password
        self.database = database
        self.host = host

        self.app.config['MYSQL_DATABASE_USER'] =  user
        self.app.config['MYSQL_DATABASE_PASSWORD'] = password
        self.app.config['MYSQL_DATABASE_DB'] = database
        self.app.config['MYSQL_DATABASE_HOST'] = host
        self.db = MySQL(app)

    def is_valid_email(self,email_id):
        """
            This function performs email authentication.
        """
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE email_id = %s",(email_id))
        data = cursor.fetchall()
        if not data:
            session.clear()
            return False
        else:
            return True

    def get_user_data(self,email_id):
        """
            This function returns the data of the user corresponding to email_id.
        """
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE email_id = %s",(email_id))
        data = cursor.fetchall()
        return data

    def insert_leave(self,leave):
        """
            This function inserts a new leave into the database.
        """
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute("SELECT user_id, department, position FROM user WHERE email_id = %s",(leave['email']))
        data = cursor.fetchall()
        user_id = data[0][0]
        department = data[0][1]
        position = data[0][2]
        
        cursor.execute("INSERT INTO leaves\
            (department, user_id, nature, purpose, is_station, request_date, start_date, end_date, duration, status, level,file_uploaded) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
            (department, user_id, leave['nature'], leave['purpose'], leave['isStation'], leave['rdate'], leave['sdate'], leave['edate'], leave['duration'], 'Pending', position,leave['attached_documents']))
        connect.commit()
        return True

    def initialize(self):
        """
            Initializes the database.
            Creates tables if they do not exist in the database.
        """
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
        mapping = ['user_id','name','email','position','department','total_casual_leaves','taken_casual_leaves','total_restricted_leaves','taken_restricted_leaves',\
                   'total_earned_leaves','taken_earned_leaves','total_vacation_leaves','taken_vacation_leaves','total_special_leaves','taken_special_leaves',\
                   'total_commuted_leaves','taken_commuted_leaves','total_hospital_leaves','taken_hospital_leaves','total_study_leaves','taken_study_leaves',\
                   'total_childcare_leaves','taken_childcare_leaves']
        dic = {}
        for i in range(23):
            dic[mapping[i]] = data[i]
        return dic
    
    
    def send_update_mail(self,leave_id):
        """
            Send update on applied leave, to the leave applicant.
        """
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

        MS.send_mail(receiver=email_id , message=msg , subject="Leave Update - IIT Ropar Leave Management Portal")

    def findNextLeaveID(self):
        """
            This function returns the the unique new id that can be used to to assign for a leave.
        """
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
        """
            Function to execute general update query on a table.
        """
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        
    def executeSelect(self,query):
        """
            Function to execute general select query on a table.
        """
        connect = self.db.connect()
        cursor = connect.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data


