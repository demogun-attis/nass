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
pin = ['9', '14', '5', '23', '12', '3', '2', '17']

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
        if i != '9':
            #GPIO.setup((int(i), led), GPIO.OUT)
            statuses.append(GPIO.input(int(i)))
    try:
        whereweare = (int(statuses.index(1)) + 1)
        percentage.append(math.ceil(( whereweare / len(statuses) * 100)))
        for x in range(0, (whereweare - 1)):
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
    except ValueError:
        print("List does not contain value")
        myresult = ['100%', 'Not Running']
        percentage = myresult
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
        runnable = False
    else:
        runnable = True
    if runnable:
        try:
            subprocess.Popen(['python3.7', '/var/www/html/nass/nass/run_all_sprinkle.py', 'all'])
            sleep(3)
            statuses = status_of_program()
            result = ["Sprinkling program started. Blooming in progress :)", statuses]
        finally:
            print("Finished program")
    else:
        result = program_page_common()
    print("RRRRRRRRRRRRESULT: \n%s" % result) 
    return render(request,'home.html',{'sprinkling':result})
    #return render(request, 'home.html')

def program_page_common():
    print("Starting run_all_sprinkle.py all") 
    pid = str(os.getpid())
    running = False
    for i in pin:
        GPIO.setup((int(i), led), GPIO.OUT)
        if GPIO.input(int(i)):
            running = True 
    statuses = status_of_program()
    if running:
        result = ["Sprinkling program started. Blooming in progress :)", statuses]
        runnable = False
    else:
        result = ["Hey There. Are you ready to sprinkle your garden?", statuses]
        runnable = True
    return result
    
def program_page(request):
    result = program_page_common()
    return render(request,'home.html',{'sprinkling':result})

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
    pin = ['9', '14', '5', '23', '12', '3', '2', '17']
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
