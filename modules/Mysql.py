import mysql


__Mysql = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)


def Init():
    global __Mysql

    Cursor = __Mysql.cursor()

    Cursor.execute(
        """
            CREATE DATABASE `ATTENDENCE_SYSTEM`;
            
            USE `ATTENDENCE_SYSTEM`;
            
            CREATE TABLE `Users`(
                
                User_id VARCHAR(100) NOT NULL PRIMARY KEY,
                
                Name VARCHAR(100) NOT NULL,
                Job VARCHAR(100) NOT NULL,
                Degree VARCHAR(100) NOT NULL,

                Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

            )ENGINE=InnoDB;

            CREATE TABLE `Attendence`(

                Attendence_id INT NOT NULL AUTO_INCREMENT PRMARY KEY,

                User_id INT NOT NULL REFRENCES 
            )ENGINE=InnoDB

        """
    )


def Insert_User(_ID, _UserName, _Job, _Degree):
    global __Mysql

    Cursor = __Mysql.cursor()

