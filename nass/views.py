from django.shortcuts import render
import requests
import mysql.connector
import datetime
import configparser
from time import sleep
import RPi.GPIO as GPIO
import os, subprocess, sys
import numpy, math
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="sprinkle"
)
led = 23
pin = ['10', '2', '3', '4', '17', '22', '27', '9']

def stop_process(request):
    subprocess.Popen(['pkill', '-f', 'run_all_sprinkle'])
    for i in pin:
        GPIO.setup((int(i), led), GPIO.OUT)
        if GPIO.input(int(i)):
            GPIO.output((int(i), led), GPIO.LOW) 
    result = "All sprinkling stopped."
    return render(request,'home.html',{'sprinkling':result})

def status_of_program():
    statuses = []
    percentage = []
    for i in pin:
        if i != '10':
            GPIO.setup((int(i), led), GPIO.OUT)
            statuses.append(GPIO.input(int(i)))
    whereweare = (int(statuses.index(1)) + 1)
    percentage.append(math.ceil(( (statuses.index(1) + 1) / len(statuses) * 100)))
    for x in range(0, statuses.index(1)):
        statuses[x] = 1
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password",
      database="sprinkle"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT gpioName FROM sprinkle_config WHERE gpioID = %s" % pin[whereweare])
    myresult = mycursor.fetchone()
    percentage.append(myresult)
    return(percentage)

def sprinkle_all(request):
    print("Starting run_all_sprinkle.py all") 
    pid = str(os.getpid())
    running = False
    for i in pin:
        GPIO.setup((int(i), led), GPIO.OUT)
        if GPIO.input(int(i)):
            running = True 
    if running:
        statuses = status_of_program()
        result = ["Some sprinkling is already ongoing. Please wait a while, or you can stop it.", statuses]
        runnable = False
    else:
        result="Sprinkling succesfully started. Blooming activated :)"
        runnable = True
    if runnable:
        try:
            subprocess.Popen(['python3.7', '/var/www/html/nass/nass/run_all_sprinkle.py', 'all'])
        finally:
            print("Finished program")
    
    
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
    mycursor.execute("SELECT * FROM sprinkle_log ORDER BY date_time DESC limit 100")
    myresult = mycursor.fetchall()
    return render(request,'home.html',{'data':myresult})

def individual(request):
    final = individual_template_page()

    return render(request,'home.html',{'individuals':final})

def individual_template_page():
    individual_runner = "<h1 style='color:white'>You can control the valves one-by-one here.</h1>"
    individual_statuses = individual_status()
    final = []
    final.append(individual_runner)
    final.append(individual_statuses)
    return(final)

def individual_status():
    individual_status = []
    pin = ['10', '2', '3', '4', '17', '22', '27', '9']
    for i in pin:
        GPIO.setup(int(i), GPIO.OUT)
        individual_status.append(GPIO.input(int(i)))
    return individual_status

def valve_switch(request):
    from .  import run_all_sprinkle

    gpioID = request.GET.get('gpioID')
    if individual_status():
        try:
            run_all_sprinkle.open_one_valve(gpioID)
        except:
            print("Some error occured when opening valve: %s" % gpioID)
    final = individual_template_page()
    #print("$s pressed" % gpioID)
    return render(request,'home.html',{'individuals':final})
