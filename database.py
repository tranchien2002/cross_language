# -*- coding: utf-8 -*-
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456tmc",
  database="cross_language"
)
mycursor = mydb.cursor()


def insert(query, val):
  mycursor.execute(query, val)
  mydb.commit()

def execute_query(query):
  mycursor.execute(query)
  result = mycursor.fetchall()
  return result

def execute_query1(query, val):
  mycursor.execute(query, val)
  result = mycursor.fetchall()
  return result

def update(query):
  mycursor.execute(query)
  mydb.commit()
# import MySQLdb
#
# mydb = MySQLdb.connect("localhost", "root", "123456tmc", "cross_language")
# mycursor = mydb.cursor()
#
# def insert(query):
#   mycursor.execute(query)
#   mydb.commit()
#
# def execute_query(query):
#   mycursor.execute(query)
#   result = mycursor.fetchall()
#   return result