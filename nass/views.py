from django.shortcuts import render
import requests
import mysql.connector
import datetime
import configparser
from time import sleep
import RPi.GPIO as GPIO
import os, subprocess, sys
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="sprinkle"
)

def sprinkle_all(request):
    print("Starting run_all_sprinkle.py all") 
    pid = str(os.getpid())
    pidfile = "/tmp/mydaemon.pid"
    if os.path.isfile(pidfile):
        print("%s already exists. This means that the sprinkling is ongoing. please come back later" % pidfile)
        result="Some sprinkling is already ongoing. Please wait a while."
        runnable = False
    else:
        open(pidfile, 'w').write(pid)
        result="Sprinkling succesfully started. Blooming activated :)"
        runnable = True
    if runnable:
        try:
            subprocess.Popen(['python3.7', '/var/www/html/nass/nass/run_all_sprinkle.py', 'all'])
        finally:
            print("Running in finally")
    
    
    return render(request,'home.html',{'sprinkling':result})
    #return render(request, 'home.html')

def button(request):

    return render(request,'home.html')

def output(request):
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password",
      database="sprinkle"
    )
    
    mycursor = mydb.cursor()
    
    #sql = "INSERT INTO sprinkle_log (gpioID, gpioName, date_time, runtime) VALUES (%s, %s, %s, %s)"
    #val = ("3", "Terrace", "2020-05-11 17:25", "runtime")
    #mycursor.execute(sql, val)
    mycursor.execute("SELECT * FROM sprinkle_log ORDER BY date_time DESC")

    myresult = mycursor.fetchall()
    print(myresult)
    return render(request,'home.html',{'data':myresult})

def start_individual_sprinkle():
    print("Starting one sprinkle")

def individual(request):
    individual_runner = "<h1 style='color:blue'>You can control the valves one-by-one here</h1>"
    individual_statuses = individual_status()
    print("individually: %s" % individual_statuses)
    final = []
    final.append(individual_runner)
    final.append(individual_statuses)
    print(final)
    return render(request,'home.html',{'individuals':final})

def individual_status():
    individual_status = []
    pin = ['10', '2', '3', '4', '17', '22', '27', '9']
    for i in pin:
        GPIO.setup(int(i), GPIO.OUT)
        individual_status.append(GPIO.input(int(i)))
    return individual_status

