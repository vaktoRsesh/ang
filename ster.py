from bluedot import BlueDot
from signal import pause
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import time
import psycopg2
import sys
#import Adafruit_DHT
import serial
from pigpio_dht import DHT11
from time import time as t

pigpio_factory = PiGPIOFactory()

# SERVO PINOUT
servoL11=Servo(2,pin_factory=pigpio_factory)    # -1 max front
servoL12=Servo(3,pin_factory=pigpio_factory)    # -1 max opp
servoL13=Servo(24,pin_factory=pigpio_factory)    # 1 max opp
servoR11=Servo(10,pin_factory=pigpio_factory)   # 1 max front
servoR12=Servo(9,pin_factory=pigpio_factory)   # 1 max opp
servoR13=Servo(11,pin_factory=pigpio_factory)   # -1 max opp
servoL21=Servo(17,pin_factory=pigpio_factory)   # 1 max tył
servoL22=Servo(27,pin_factory=pigpio_factory)   # 1 max opp
servoL23=Servo(22,pin_factory=pigpio_factory)   # -1 max opp
servoR21=Servo(25,pin_factory=pigpio_factory)   # -1 max tył
servoR22=Servo(8,pin_factory=pigpio_factory)   # -1 max opp
servoR23=Servo(7,pin_factory=pigpio_factory)   # 1 max opp


#FUNCTIONS GPS

def onoff(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(18,GPIO.HIGH)
    time.sleep(2.9)
    GPIO.output(18,GPIO.LOW)
    time.sleep(2)
    GPIO.cleanup()

def gps_on():
    global rec_buff
    rec_buff = ''
    ser.write(('AT+CGNSPWR=1'+'\r\n').encode())
    time.sleep(1)
    if ser.inWaiting():
        time.sleep(0.2)
        rec_buff = ser.read(ser.inWaiting())
        print (rec_buff.decode())
    if rec_buff.decode()=='AT+CGNSPWR=1\r\r\nOK\r\n':
        print ('wlaczono')

def get_pos():
    global x
    rec_buff2 = ''
    ser.write(('AT+CGNSINF'+'\r\n').encode())
    time.sleep(1)
    if ser.inWaiting():
        time.sleep(0.2)
        rec_buff2 = ser.read(ser.inWaiting())
        #print (rec_buff2.decode())
        x = rec_buff2.decode().split(',')
        print ('N = {}, E = {}'.format(x[3],x[4]))
    while len(x[3])==0:
        rec_buff2 = ''
        ser.write(('AT+CGNSINF'+'\r\n').encode())
        time.sleep(1)
        if ser.inWaiting():
            time.sleep(0.2)
            rec_buff2 = ser.read(ser.inWaiting())
            #print (rec_buff2.decode())
            x = rec_buff2.decode().split(',')
            print ('N = {}, E = {}'.format(x[3],x[4]))

def gps_off():
    global rec_buff
    ser.write(('AT+CGNSPWR=0'+'\r\n').encode())
    time.sleep(1)
    if ser.inWaiting():
        time.sleep(0.2)
        rec_buff = ser.read(ser.inWaiting())
        print (rec_buff.decode())
    if rec_buff.decode()=='AT+CGNSPWR=0\r\r\nOK\r\n':
        print ('wylaczono')

def brrr(): #
    get_pos()
    temp()
    send_to_DB(x[3],x[4],humidity,temperature,numerek)

#FUNCTIONS DT11

def connect():
    DB_NAME = "exwppxux"
    DB_USER = "exwppxux"
    DB_PASS = "SHk3Tbpw88UisiQ9tcGiabSITYvzBhda"
    DB_HOST = "tyke.db.elephantsql.com"
    DB_PORT = "5432"
    global conn
    conn = psycopg2.connect(database = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port= DB_PORT)
    print("connected")

def start_session():
    cur = conn.cursor()
    cur.execute(""" insert into sesja DEFAULT VALUES""")
    conn.commit()
    print("sesja rozpoczęta")
    
def get_number():
    cur = conn.cursor()
    cur.execute(""" SELECT max(sessionid) from sesja """)
    rows = cur.fetchall()
    rows=rows[0]
    global numerek
    numerek=rows[0]
    print('numer sesji: '+str(numerek))

def end_session():
    global numerek
    string = 'UPDATE sesja SET dateofend  = (SELECT CURRENT_TIMESTAMP), sessionstatus = false where sessionid = {};'.format(numerek)
    cur = conn.cursor()
    cur.execute(string)
    conn.commit()
    print("sesja zakończona")

def send_to_DB(a,b,c,d,e):
    string =' INSERT INTO dane(polozenie_n,polozenie_e,wilgotnosc,temperaturaot,sessionid) \n VALUES ({},{},{},{},{})'.format(a,b,c,d,e)
    cur = conn.cursor()
    cur.execute(string)
    conn.commit()
    print("wpisane")
 
def temp():
    global humidity, temperature, sensor
    result = sensor.read()
    temperature = result.get('temp_c')
    humidity = result.get('humidity')
    while (humidity==0):
        result = sensor.read()
        temperature = result.get('temp_c')
        humidity = result.get('humidity')
    print ('Temp: {} C  Humidity: {} %'.format(temperature, humidity))
    #humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print ('Temp: {} C  Humidity: {} %'.format(temperature, humidity))


#FUNCTIONS MOVEMENT

def zerowanie():
    servoL11.value=zeroL11
    servoL12.value=zeroL12
    servoL13.value=zeroL13
    servoR11.value=zeroR11
    servoR12.value=zeroR12
    servoR13.value=zeroR13
    servoL21.value=zeroL21
    servoL22.value=zeroL22
    servoL23.value=zeroL23
    servoR21.value=zeroR21
    servoR22.value=zeroR22
    servoR23.value=zeroR23

def frem():
    print('Wykonuję ruch naprzód')
    #1 ruch L1 do przodu
    for i in range(-30,31,2):
        posL11=-0.0033*i-0.9    # -0.8 -> -1
        if i<0:
            posL12=-0.0233*i-0.5 # 0.2 -> -0.5
        else:
            posL12=0.05*i-0.5   # -0.5 -> 1
        posL13=0.03*i+0.1     # -0.8 -> 1
        servoL11.value=posL11
        servoL12.value=posL12
        servoL13.value=posL13
    #2 ruch R1 do przodu
    for i in range(-30,31,2):
        posR11=0.0033*i+0.9     # 0.8 -> 1
        if i<0:
            posR12=0.0233*i+0.5 # -0.2 -> 0.5
        else:
            posR12=-0.05*i+0.5  # 0.5 -> -1
        posR13=-0.03*i-0.1    # 0.8 -> -1
        servoR11.value=posR11
        servoR12.value=posR12
        servoR13.value=posR13
    #3 czołganie do przodu
    for i in range(-30,31,2):
        posL12=-0.02*i+0.4    # 1 -> -0.2
        posL13=-0.03*i+0.1     # 1 -> -0.8
        posL21=0.0033*i+0.9      # 0.8 -> 1
        posL22=-0.0067*i-0.4   # -0.2 -> -0.6
        posL23=-0.03*i-0.1     # 0.8 -> -1
        posR12=0.02*i-0.4    # -1 -> 0.2
        posR13=0.03*i-0.1      # -1 -> 0.8
        posR21=-0.0033*i-0.9     # -0.8 -> -1
        posR22=0.0067*i+0.4     # 0.2 -> 0.6
        posR23=0.03*i+0.1      # -0.8 -> 1
        servoL13.value=posL13
        servoR13.value=posR13
        servoL21.value=posL21
        servoR21.value=posR21
        servoL22.value=posL22
        servoR22.value=posR22
        servoL23.value=posL23
        servoR23.value=posR23
        servoL12.value=posL12
        servoR12.value=posR12
    #4 powrót do zera L2 
    for i in range(-30,31,2):
        posL21=-0.0033*i+0.9     # 1 -> 0.8
        if i<0:
            posL22=0.02*i     # -0.6 -> 0 
        else:
            posL22=0.0067*i    # 0 -> 0.2
        posL23=0.03*i-0.1    # -1 -> 0.8
        servoL21.value=posL21
        servoL22.value=posL22
        servoL23.value=posL23
    #5 powrót do zera R2
    for i in range(-30,31,2):
        posR21=0.0033*i-0.9     # -1 -> -0.8
        if i<0:
            posR22=-0.02*i     # 0.6 -> 0
        else:
            posR22=-0.0067*i     # 0 -> -0.2
        posR23=-0.03*i+0.1     # 1 -> -0.8
        servoR21.value=posR21
        servoR22.value=posR22
        servoR23.value=posR23
    #6 przesuw do zera L1 i R1
    zerowanie()
    print('Zakończono wykonywanie ruchu naprzód')

def tilbake():
    print('Wykonuję ruch do tyłu')
    #1 ruch R2 do tyłu
    for i in range(-30,31,2):
        posR21=-0.0033*i-0.9        # -0.8 -> -1
        if i<0:
            posR22=-0.0233*i-0.5    # 0.2 -> -0.5
        else:
            posR22=0.05*i-0.5       # -0.5 -> 1
        posR23=0.03*i+0.1           # -0.8 -> 1
        servoR21.value=posR21
        servoR22.value=posR22
        servoR23.value=posR23
    #2 ruch L2 do tyłu
    for i in range(-30,31,2):
        posL21=0.0033*i+0.9         # 0.8 -> 1
        if i<0:
            posL22=0.0233*i+0.5     # -0.2 -> 0.5
        else:
            posL22=-0.05*i+0.5      # 0.5 -> -1
        posL23=-0.03*i-0.1          # 0.8 -> -1
        servoL21.value=posL21
        servoL22.value=posL22
        servoL23.value=posL23
    #3 czołganie do tyłu
    for i in range(-30,31,2):
        posR22=-0.02*i+0.4   # 1 -> -0.2
        posR23=-0.03*i+0.1   # 1 -> -0.8
        posR11=0.0033*i+0.9  # 0.8 -> 1
        posR12=-0.0067*i-0.4 # -0.2 -> -0.6
        posR13=-0.03*i-0.1   # 0.8 -> -1
        posL22=0.02*i-0.4    # -1 -> 0.2   
        posL23=0.03*i-0.1    # -1 -> 0.8
        posL11=-0.0033*i-0.9 # -0.8 -> -1
        posL12=0.0067*i+0.4  # 0.2 -> 0.6
        posL13=0.03*i+0.1    # -0.8 -> 1
        servoR23.value=posR23
        servoL23.value=posL23
        servoR11.value=posR11
        servoL11.value=posL11
        servoR12.value=posR12
        servoL12.value=posL12
        servoR13.value=posR13
        servoL13.value=posL13
        servoR22.value=posR22
        servoL22.value=posL22
    #4 powrót do zera R1
    for i in range(-30,31,2):
        posR11=-0.0033*i+0.9    # 1 -> 0.8
        if i<0:
            posR12=0.02*i       # -0.6 -> 0
        else:
            posR12=0.0067*i     # 0 -> 0.2
        posR13=0.03*i-0.1       # -1 -> 0.8
        servoR11.value=posR11
        servoR12.value=posR12
        servoR13.value=posR13
    #5 powrót do zera L1
    for i in range(-30,31,2):
        posL11=0.0033*i-0.9      # -1 -> -0.8
        if i<0:
            posL12=-0.02*i       # 0.6 -> 0
        else:
            posL12=-0.0067*i     # 0 -> -0.2
        posL13=-0.03*i+0.1       # 1 -> -0.8
        servoL11.value=posL11
        servoL12.value=posL12
        servoL13.value=posL13
    #6 przesuw do zera R2 i L2
    zerowanie()
    print('Zakończono wykonywanie ruchu do tyłu')
       
def opp():
    for i in range(-30,31,2):
        posL1R2_2=0.0083*i+0.05     # -0.2 -> 0.3
        posL1R2_3=0.005*i-0.65      # -0.8 -> -0.5
        posL2R1_2=-0.0083*i-0.05    # 0.2 -> -0.3
        posL2R1_3=-0.005*i+0.65     # 0.8 -> 0.5
        servoL12.value=posL1R2_2
        servoR22.value=posL1R2_2
        servoL22.value=posL2R1_2
        servoR12.value=posL2R1_2
        servoL13.value=posL1R2_3
        servoR23.value=posL1R2_3
        servoL23.value=posL2R1_3
        servoR13.value=posL2R1_3

def ned():
    for i in range(-30,31,2):
        posL1R2_2=-0.0083*i+0.05    # 0.3 -> -0.2
        posL1R2_3=-0.005*i-0.65     # -0.5 -> -0.8
        posL2R1_2=0.0083*i-0.05     # -0.3 -> 0.2
        posL2R1_3=0.005*i+0.65      # 0.5 -> 0.8
        servoL12.value=posL1R2_2
        servoR22.value=posL1R2_2
        servoL22.value=posL2R1_2
        servoR12.value=posL2R1_2
        servoL13.value=posL1R2_3
        servoR23.value=posL1R2_3
        servoL23.value=posL2R1_3
        servoR13.value=posL2R1_3
    
def ruchL1R2_2(index):
    if index<0:
        posL1R2_2=-0.0133*index-0.6 # -0.2 -> -0.6
    else:
        posL1R2_2=0.0133*index-0.6  # -0.6 -> -0.2
    return posL1R2_2

def ruchL1R2_3(index):
    if index<0:
        posL1R2_3=-0.0067*index-1   # -0.8 -> -1
    else:
        posL1R2_3=0.0067*index-1    # -1 -> -0.8
    return posL1R2_3
    
def ruchL2R1_2(index):
    if index<0:
        posL2R1_2=0.0133*index+0.6  # 0.2 -> 0.6
    else:
        posL2R1_2=-0.0133*index+0.6 # 0.6 -> 0.2
    return posL2R1_2

def ruchL2R1_3(index):
    if index<0:
        posL2R1_3=0.0067*index+1    # 0.8 -> 1
    else:
        posL2R1_3=-0.0067*index+1   # 1 -> 0.8
    return posL2R1_3

def hoyre():
      print('Wykonuję obrót w prawo')
      #1 Ruch R2
      for i in range(-30,31,2):    
          posR21=-0.0033*i-0.9    # -0.8 -> -1
          posR22=ruchL1R2_2(i)
          posR23=ruchL1R2_3(i)
          servoR21.value=posR21
          servoR22.value=posR22
          servoR23.value=posR23
      
      #2 Ruch L1
      for i in range(-30,31,5):    
          posL11=-0.0033*i-0.9    # -0.8 -> -1
          posL12=ruchL1R2_2(i)
          posL13=ruchL1R2_3(i)
          servoL11.value=posL11
          servoL12.value=posL12
          servoL13.value=posL13
      
      #3 Ruch R1
      for i in range(-30,31,2):    
          posR11=-0.0033*i+0.7    # 0.8 -> 0.6
          posR12=ruchL2R1_2(i)
          posR13=ruchL2R1_3(i)
          servoR11.value=posR11
          servoR12.value=posR12
          servoR13.value=posR13
      
      #4 Ruch L2
      for i in range(-30,31,2):
          posL21=-0.0033*i+0.7    # 0.8 -> 0.6
          posL22=ruchL2R1_2(i)
          posL23=ruchL2R1_3(i)
          servoL21.value=posL21
          servoL22.value=posL22
          servoL23.value=posL23
      
      #5 Uniesienie do góry
      opp()
      time.sleep(0.5)
      
      #6 Powrót do zera (obrót)
      for i in range(-30,31,2):
          posL11R21=0.0033*i-0.9   # -1 -> -0.8
          posL21R11=0.0033*i+0.7    # 0.6 -> 0.8
          servoL11.value=posL11R21
          servoR21.value=posL11R21
          servoL21.value=posL21R11
          servoR11.value=posL21R11
          
      #7 Opuszczenie na dół    
      ned()
      zerowanie()
      print('Zakończono wykonywanie obrotu w prawo')

def venstre():
      print('Wykonuję obrót w lewo')
      #1 Ruch L1
      for i in range(-30,31,2):
          posL11=0.0033*i-0.7    # -0.8 -> -0.6
          posL12=ruchL1R2_2(i)
          posL13=ruchL1R2_3(i)
          servoL11.value=posL11
          servoL12.value=posL12
          servoL13.value=posL13
      
      #2 Ruch R2  
      for i in range(-30,31,2):
          posR21=0.0033*i-0.7    # -0.8 -> -0.6
          posR22=ruchL1R2_2(i)
          posR23=ruchL1R2_3(i)
          servoR21.value=posR21
          servoR22.value=posR22
          servoR23.value=posR23
      
      #3 Ruch L2      
      for i in range(-30,31,2):
          posL21=0.0033*i+0.9    # 0.8 -> 1
          posL22=ruchL2R1_2(i)
          posL23=ruchL2R1_3(i)
          servoL21.value=posL21
          servoL22.value=posL22
          servoL23.value=posL23
      
      #4 Ruch R1      
      for i in range(-30,31,2):
          posR11=0.0033*i+0.9    # 0.8 -> 1
          posR12=ruchL2R1_2(i)
          posR13=ruchL2R1_3(i)
          servoR11.value=posR11
          servoR12.value=posR12
          servoR13.value=posR13
    
      #5 Uniesienie do góry
      opp()
      time.sleep(0.5)
      
      #6 Powrót do zera (obrót)
      for i in range(-30,31,2):
          posL11R21=-0.0033*i-0.7   # -0.6 -> -0.8
          posL21R11=-0.0033*i+0.9   # 1 -> 0.8
          servoL11.value=posL11R21
          servoR21.value=posL11R21
          servoL21.value=posL21R11
          servoR11.value=posL21R11
          
      #6 Opuszczenie na dół    
      ned()
      zerowanie()
      print('Zakończono wykonywanie obrotu w lewo')
      
def machanko():
    for i in range(-30,31,2):
        posL12=-0.0133*i-0.6     # -0.2 -> -1
        servoL12.value=posL12
    for j in range(2):
        for i in range(-30,31,2):
            if i<0:
                posL13=0.06*i+1     # -0.8 -> 1
            else:
                posL13=-0.06*i+1     # 1 -> -0.8
            servoL13.value=posL13
    for i in range(-30,31,2):
        posL12=0.0133*i-0.6     # -1 -> -0.2
        servoL12.value=posL12
   
def szaryPrawoGora():
    print("man/auto")
    global auto
    if(auto == True):
        auto = False
        print('manual')
    else:
        auto = True
        print('auto')

# SETUP
GPIO.cleanup()
conn =''
numerek = 0
#global def values
humidity=50.0 
temperature =18.0

ser = serial.Serial('/dev/ttyS0',9600)
ser.flushInput()
rec_buff =''

auto = False

zeroL11=zeroR21=-0.8
zeroL12=zeroR22=-0.2
zeroL13=zeroR23=-0.8
zeroL21=zeroR11=0.8
zeroL22=zeroR12=0.2
zeroL23=zeroR13=0.8
zerowanie()
 
# LOOP
  
bd = BlueDot(cols=3, rows=6) #definiowanie ilosci przyciskow

bd.square = True

bd[0,0].visible = False
bd[2,0].visible = False
bd[2,2].visible = False


bd[1,0].color = "red" # red - kolor strzalek gora/dol itp
bd[0,1].color = "red"
bd[1,2].color = "red"
bd[2,1].color = "red"

bd[1,1].color = (255, 0, 255) #kolor srodkowego

bd[0,4].color = (128, 128, 128) #szary, kolor dolnych przyciskow
bd[1,4].color = (128, 128, 128)
bd[2,4].color = (128, 128, 128)
bd[0,5].color = (128, 128, 128)
bd[1,5].color = (128, 128, 128)
bd[2,5].color = (128, 128, 128)
bd[0,3].color = (128, 128, 128)
bd[1,3].color = (128, 128, 128)
bd[2,3].color = (128, 128, 128)

bd[1,0].when_pressed = frem     # górny przycisk - krok naprzód
bd[1,2].when_pressed = tilbake  # dolny przycisk - krok do tyłu
bd[0,1].when_pressed = venstre  # lewy przycisk  - obrót w lewo
bd[2,1].when_pressed = hoyre  # prawy przycisk - obrót w prawo
bd[1,1].when_pressed = zerowanie # srodkowy przycisk - zerowanie

bd[0,2].when_pressed = machanko # szary lewy górny przycisk - machanie do fanów

bd[0,3].when_pressed = brrr
bd[1,3].when_pressed = gps_on
bd[2,3].when_pressed = gps_off
 
bd[0,4].when_pressed = onoff
bd[1,4].when_pressed = connect
bd[2,4].when_pressed = szaryPrawoGora

bd[0,5].when_pressed = start_session
bd[1,5].when_pressed = get_number
bd[2,5].when_pressed = end_session

ser.flushInput()
saved_time_1 = 0
saved_time_2 = 0
actual_time = 1
sensor = DHT11(21,2)

while True:
        actual_time = int(t()*1000)
        if((actual_time - saved_time_1 > 10000) and (auto == True) ):
            saved_time_1 = actual_time
            print('cykl co 10s')
            brrr()
        #if(actual_time - saved_time_2 > 2000 ):
        #    saved_time_2 = actual_time
        #    print('cykl co 2s')
        

pause()