import random
import psycopg2
import pandas as pd
from faker import Faker
from datetime import datetime
from datetime import date

#########db setup
connection = psycopg2.connect(database = "Assignment", user = "postgres", password = "Alina6870", host = "localhost", port = "5432")
print ("Opened database successfully")

cursor = connection.cursor()


#helpers
faker = Faker()

today = date.today()

def fakeDate(start_date, end_date):
    return faker.date_between_dates(date_start=start_date, date_end=end_date)

def csvDatas(filename):
    df = pd.read_csv(filename)
    # creating column list for insertion
    cols = ",".join([str(i) for i in df.columns.tolist()])

    return df, cols


########## dataframe load to db
def user_employers():
    df_cols_tuple = csvDatas('user_employer.csv')

    for i, row in df_cols_tuple[0].iterrows():
        sql = "INSERT INTO User_Employers (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def platform():
    df_cols_tuple = csvDatas('platform.csv')

    for i, row in df_cols_tuple[0].iterrows():
        sql = "INSERT INTO Platform (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def course():
    df_cols_tuple = csvDatas('course.csv')

    for i, row in df_cols_tuple[0].iterrows():
        sql = "INSERT INTO Course (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def review():
    df_cols_tuple = csvDatas('review.csv')

    for i, row in df_cols_tuple[0].iterrows():
        sql = "INSERT INTO Review (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def training():
    df_cols_tuple = csvDatas('training.csv')

    for i, row in df_cols_tuple[0].iterrows():
        if row["finish_date"] == 'None':
            row['finish_date'] = None 
        sql = "INSERT INTO Ongoing_Training (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def certification(): 
    df_cols_tuple = csvDatas('certification.csv')

    for i, row in df_cols_tuple[0].iterrows():
        sql = "INSERT INTO Certification (" + df_cols_tuple[1] + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        connection.commit() 

    cursor.execute("SELECT userID, finish_date FROM Ongoing_Training WHERE completion_percentage = 100;")
    result = cursor.fetchall()
    sql = "UPDATE Certification SET completion_duration=%s, completion_date=%s WHERE userID=%s;"

    for r in result:
        records = (random.randint(20, 400), fakeDate(r[1], datetime(2022, 8, 30)), r[0])
        cursor.execute(sql, records)   
        connection.commit()
        print(cursor.rowcount, "record(s) affected")


##################insertion query
def generate():
    #user_employers() 
    #platform() 
    #course() 
    #review() 
    #training() 
    #certification()
    print("all generated")


#def generateEachTable(tablename):


def insertCertification(user_id, course_id, duration, date):
    insert_query = """INSERT INTO Certification (userID, courseID, completion_duration, completion_date) VALUES (%s, %s, %s, %s);"""
    insert_records = (user_id, course_id, duration, date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into certification table")

def insertCourse(name, platform_id, duration, date, tags, photo, rec_begin_date):
    insert_query = """INSERT INTO Course (course_name, platformID, duration, creation_date, tags, photo, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (name, platform_id, duration, date, tags, photo, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into course table")

def insertOngoingTraining(user_id, course_id, status, percentage, start_date, finish_date, last_update, rec_begin_date):
    insert_query = """INSERT INTO Ongoing_Training (userID, courseID, status, completion_percentage, start_date, finish_date, last_updated, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (user_id, course_id, status, percentage, start_date, finish_date, last_update, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into training table")

def insertPlatform(name, path, rec_begin_date):
    insert_query = """INSERT INTO Platform (platform_name, hyperlink_path, recBeginDate) VALUES (%s, %s, %s);"""
    insert_records = (name, path, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into platform table")

def insertReview(user_id, course_id, feedback, like_dislike, score, rec_begin_date):
    insert_query = """INSERT INTO Review (userID, courseID, feedback, like_dislike, ranking_score, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s);"""
    insert_records = (user_id, course_id, feedback, like_dislike, score, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into review table")

def insertUserEmployers(employer_number, creation_date, uname, pwd, level, rec_begin_date):
    insert_query = """INSERT INTO User_Employers (employer_number, creation_date, username, pwd, lvl, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s);"""
    insert_records = (employer_number, creation_date, uname, pwd, level, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into user table")

## default null

def insertCertificationWithNulls(user_id, course_id, recBeginDate, duration=None, date=None):
    cursor.execute(" SELECT certificationID FROM Certification ORDER BY certificationID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1
    
    insert_query = """INSERT INTO Certification (certificationID, userID, courseID, completion_duration, completion_date, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, user_id, course_id, duration, date, recBeginDate)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into certification table")
    

def insertCourseWithNulls(platform_id, rec_begin_date, name=None, duration=None, date=None, tags=None, photo=None):
    cursor.execute(" SELECT courseID FROM Course ORDER BY courseID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Course (courseID, course_name, platformID, duration, creation_date, tags, photo, recBeginDate) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, name, platform_id, duration, date, tags, photo, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into course table")

def insertOngoingTrainingWithNulls(user_id, course_id, rec_begin_date, status=None, percentage=None, start_date=None, finish_date=None, last_update=None):
    cursor.execute(" SELECT trainingID FROM Ongoing_Training ORDER BY trainingID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Ongoing_Training (trainingID, userID, courseID, status, completion_percentage, start_date, finish_date, last_updated, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id , user_id, course_id, status, percentage, start_date, finish_date, last_update, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into training table")

def insertPlatformWithNulls(rec_begin_date, name=None, path=None):
    cursor.execute(" SELECT platformID FROM Platform ORDER BY platformID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Platform (platformID, platform_name, hyperlink_path, recBeginDate) VALUES (%s, %s, %s, %s);"""
    insert_records = (next_id, name, path, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into platform table")

def insertReviewWithNulls(user_id, course_id, rec_begin_date, feedback=None, like_dislike=None, score=None):
    cursor.execute(" SELECT reviewID FROM Review ORDER BY reviewID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Review (reviewID, userID, courseID, feedback, like_dislike, ranking_score, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, user_id, course_id, feedback, like_dislike, score, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into review table")

def insertUserEmployersWithNulls(uname, rec_begin_date, employer_number, creation_date=None, pwd=None, level=None):
    cursor.execute(" SELECT userID FROM User_Employers ORDER BY userID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO User_Employers (userID, employer_number, creation_date, username, pwd, lvl, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, employer_number, creation_date, uname, pwd, level, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into user table")

## default value parameter

def insertCertificationWithDefault(user_id=1, course_id=1, duration=1, date=today.strftime('%Y-%m-%d'), recBeginDate=today.strftime('%Y-%m-%d')):
    cursor.execute(" SELECT certificationID FROM Certification ORDER BY certificationID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Certification (certificationID, userID, courseID, completion_duration, completion_date, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, user_id, course_id, duration, date, recBeginDate)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into certification table")

def insertCourseWithDefault(platform_id=1, rec_begin_date=today.strftime('%Y-%m-%d'), name='', duration=1, date=today.strftime('%Y-%m-%d'), tags='', photo=None):
    cursor.execute(" SELECT courseID FROM Course ORDER BY courseID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Course (courseID, course_name, platformID, duration, creation_date, tags, photo, recBeginDate) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, name, platform_id, duration, date, tags, photo, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into course table")

def insertOngoingTrainingWithDefault(user_id=1, course_id=1, rec_begin_date=today.strftime('%Y-%m-%d'), status='', percentage=0, start_date=today.strftime('%Y-%m-%d'), finish_date=today.strftime('%Y-%m-%d'), last_update=today.strftime('%Y-%m-%d')):
    cursor.execute(" SELECT trainingID FROM Ongoing_Training ORDER BY trainingID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Ongoing_Training (trainingID, userID, courseID, status, completion_percentage, start_date, finish_date, last_updated, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id , user_id, course_id, status, percentage, start_date, finish_date, last_update, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into training table")

def insertPlatformWithDefault(rec_begin_date=today.strftime('%Y-%m-%d'), name='', path=''):
    cursor.execute(" SELECT platformID FROM Platform ORDER BY platformID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Platform (platformID, platform_name, hyperlink_path, recBeginDate) VALUES (%s, %s, %s, %s);"""
    insert_records = (next_id, name, path, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into platform table")

def insertReviewWithDefault(user_id=1, course_id=1, rec_begin_date=today.strftime('%Y-%m-%d'), feedback='', like_dislike=False, score=0):
    cursor.execute(" SELECT reviewID FROM Review ORDER BY reviewID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO Review (reviewID, userID, courseID, feedback, like_dislike, ranking_score, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, user_id, course_id, feedback, like_dislike, score, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into review table")

def insertUserEmployersWithDefault(uname='', rec_begin_date=today.strftime('%Y-%m-%d'), employer_number=000000, creation_date=today.strftime('%Y-%m-%d'), pwd='', level=''):
    cursor.execute(" SELECT userID FROM User_Employers ORDER BY userID DESC LIMIT 1;")
    result = cursor.fetchall()
    next_id = result[0][0] + 1

    insert_query = """INSERT INTO User_Employers (userID, employer_number, creation_date, username, pwd, lvl, recBeginDate) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    insert_records = (next_id, employer_number, creation_date, uname, pwd, level, rec_begin_date)
    cursor.execute(insert_query, insert_records)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into user table")



################## select query
def select(table_name, columns, where):
    cursor.execute("SELECT " + columns + " FROM " + table_name + " WHERE " + where +";")
    result = cursor.fetchall()
    for r in result:
        print(cursor.rowcount, "record(s) affected")
        return r
        

################## delete query
def activate(table_name, where):
    cursor.execute("UPDATE " + table_name + " SET active='y', recBeginDate= '" + str(today.strftime("%Y-%m-%d")) + "', recEndDate= '" + str(datetime(9999, 12, 31)) + "' WHERE " + where + ";")
    connection.commit()
    print(cursor.rowcount, "record(s) affected")

def deactivate(table_name, where):
    cursor.execute("UPDATE " + table_name + " SET active='n', recEndDate= '" + str(today.strftime("%Y-%m-%d")) + "' WHERE " + where + ";")
    connection.commit()
    print(cursor.rowcount, "record(s) affected")

def delete_permanent(table_name, where):
    cursor.execute("DELETE FROM " + table_name + " WHERE " + where + ";")
    connection.commit()
    print(cursor.rowcount, "record(s) affected")

################## update query
def update(table_name, columns_with_values, where):
    cursor.execute("UPDATE " + table_name + " SET " + columns_with_values + " WHERE " + where + ";")
    connection.commit()
    print(cursor.rowcount, "record(s) affected")

################## function calls
#generate()
#select("User_Employers", "userID, username", "active='y'")
#deactivate("ongoing_training", "userID=5")
#update("ongoing_training", "userid=5", "courseid=403")
#insertUserEmployersWithNulls("kafka333", today.strftime("%Y-%m-%d"), 999999)
#insertReviewWithNulls(2, 4, today.strftime("%Y-%m-%d"))

connection.close()