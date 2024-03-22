import sqlite3
import os
def gradesDatabaseManager():
    connection=sqlite3.connect(r'grade')
    c=connection.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='Grades'")
    tableExistence=c.fetchone()
    if tableExistence is None:
        c.execute("CREATE TABLE Grades('Grade' TEXT UNIQUE, 'Value' Integer, 'Status' TEXT, 'Attendance' TEXT)")
        c.execute("INSERT INTO Grades VALUES('A+', 10,'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('A', 9, 'P', 'PRESENT')")
        c.execute("INSERT INTO Grades VALUES('B', 8, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('C', 7, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('D', 6, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('E', 5, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('F', 0, 'F','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('ABSENT', 0, 'F','ABSENT')")
        c.execute("INSERT INTO Grades VALUES('AB', 0, 'F','ABSENT')")
        c.execute("INSERT INTO Grades VALUES('COMPLETED', 0, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('COMPLE', 0, 'P','PRESENT')")
        c.execute("INSERT INTO Grades VALUES('MP', 0,'F','PRESENT')")
    def add(grade,value):
        c.execute("INSERT INTO Grades VALUES(?, ?)",(grade,value))
    def delete(grade):
        c.execute("DELETE FROM Grades WHERE grade=?",(grade,))
    c.execute("SELECT * From Grades")
    grades=c.fetchall()
    connection.commit()
    connection.close()
    return grades

def branchCodeDatabaseManager():
    connection=sqlite3.connect(r'C:\Users\yasas\OneDrive\Desktop\grade')
    c=connection.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='BranchCodes'")
    tableExistence=c.fetchone()
    if tableExistence is None:
        c.execute("CREATE TABLE BranchCodes('Branch' TEXT, 'Code' TEXT UNIQUE, 'Abbrevation' TEXT)")
        c.execute("INSERT INTO BranchCodes VALUES('Civil Engineering', '01', 'CE')")
        c.execute("INSERT INTO BranchCodes VALUES('Electrical and Electronics Engineering', '02', 'EEE')")
        c.execute("INSERT INTO BranchCodes VALUES('Mechanical Engineering', '03', 'ME')")
        c.execute("INSERT INTO BranchCodes VALUES('Electronics and Communication Engineering', '04', 'ECE')")
        c.execute("INSERT INTO BranchCodes VALUES('Computer Science and Engineering', '05', 'CSE')")
    c.execute("SELECT * From BranchCodes")
    branchCodes=c.fetchall()
    connection.commit()
    connection.close()
    return branchCodes