from django.shortcuts import render
import requests
import mysql.connector
import datetime
import configparser
from time import sleep
import RPi.GPIO as GPIO
import sys, os
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = 5

def sprinkledb_connect():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="sprinkle"
    )

def start_pump():
    print("Starting pump")
    # Opening Pump
    pump = 'Pump'
    GPIO.setup((10, led), GPIO.OUT)
    GPIO.output((10, led), GPIO.HIGH)
    # Report Pump
    sprinkle_report("10", pump, "infinity")

def stop_pump():
    print("Stopping pump")
    # Opening Pump
    pump = 'Pump'
    sprinkle_report_stop('10')
    GPIO.output((10, led), GPIO.LOW)
    
def start_sprinkle(gpioID, sprinkle_name, runtime): 
    print("Starting sprinkle %s:%s" % (gpioID, sprinkle_name))
    GPIO.setup(int(gpioID), GPIO.OUT)
    GPIO.output(int(gpioID), GPIO.HIGH)
    sprinkle_report(int(gpioID), sprinkle_name, runtime)

def stop_sprinkle(gpioID):
    print("Stopping sprinkle %s" % gpioID)
    print("This is before: %s" % GPIO.input(int(gpioID)))
    sprinkle_report_stop(gpioID)
    GPIO.output(int(gpioID), GPIO.LOW)
    print("This is after: %s" % GPIO.input(int(gpioID)))

def sprinkle_all():
    #pin = int(config['gpio_starter'])
    print("sprinkle_all")
    led = 27
    # pins on rpi. 10 is reserved for the pump
    pin = ['2', '3', '4', '17', '22', '27', '9']
    # time to sleep between operations in the main loop
    sprinkledb_connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sprinkle_config")
    myresult = mycursor.fetchall()
    print(myresult)
    fields = {}
    for row in myresult:
        #fields[row[0]] = [code for code in row[1].split(',')]
        fields[row[0]] = [row[1], row[2]]
    print(fields)
    #try:
    # Starting PUMP
    start_pump()
    
    for i in pin:
        print(i)
        sprinkle_name = fields.get(int(i))[0]
        runtime = fields.get(int(i))[1]
        start_sprinkle(i, sprinkle_name, runtime)
        sleep(runtime) # * 60)
        stop_sprinkle(i)

    stop_pump()

def open_one_valve(gpioID):
    sprinkledb_connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sprinkle_config WHERE gpioID = %s" % gpioID)
    myresult = mycursor.fetchone()
    fields = {myresult[0]: [myresult[1], myresult[2]]} 
    sprinkle_name = fields.get(int(gpioID))[0]
    runtime = "Manually started"
    print("%s, %s, %s" % (gpioID, sprinkle_name, runtime))
    GPIO.setup(int(gpioID), GPIO.OUT)
    if GPIO.input(int(gpioID)):
        stop_sprinkle(gpioID)
    else:
        start_sprinkle(gpioID, sprinkle_name, runtime)
  
def sprinkle_report_stop(gpioID):
    sprinkledb_connect()
    mycursor = mydb.cursor()
    sql2 = "UPDATE sprinkle_config SET status = %s WHERE gpioID = %s"
    val = ('Stopped', gpioID)
    mycursor.execute(sql2, val)
    mydb.commit()

def sprinkle_report(i, sprinkler_name, duration):
    gpioID = i
    sprinkler_name = sprinkler_name
    now = datetime.datetime.now()
    
    sprinkledb_connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO sprinkle_log (gpioID, gpioName, date_time, runtime) VALUES (%s, %s, %s, %s)"
    val = (i, sprinkler_name, now, duration)
    mycursor.execute(sql, val)
    mydb.commit()
    
    sprinkledb_connect()
    mycursor = mydb.cursor()
    sql2 = "UPDATE sprinkle_config SET status = %s WHERE gpioID = %s"
    val = ('Running', i)
    mycursor.execute(sql2, val)
    mydb.commit()
    # return render(request, 'home.html')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Standard mode
        main()
    elif len(sys.argv) == 2 and sys.argv[1] in ['2', '3', '4', '17', '22', '27', '9', '10']:
        # Tests connection to API
        # Make sure you run as root or this won't work
        open_one_valve(sys.argv[1])
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        # Runs sprinkler regardless of rainfall
        pid = str(os.getpid())
        pidfile = "/tmp/run_all_sp_daemon.pid"
        
        try:
            sprinkle_all()
        finally:
            os.unlink(pidfile)
    elif len(sys.argv) == 2 and sys.argv[1] == 'init':
        # Sets pin and led GPIOs to GPIO.LOW
        init()
    else:
        print("Unknown inputs", sys.argv)

