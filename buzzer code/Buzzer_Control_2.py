import RPi.GPIO as GPIO
import time

# Define the buzzer pin
BUZZER_PIN = 23

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

GPIO.cleanup()
# Set the buzzer pin as output
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# def activate_buzzer(active_time):
#     GPIO.output(BUZZER_PIN, GPIO.HIGH)
#     time.sleep(active_time)
#     GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    
a = int(input("Enter a number 0,1or 2: "))
if(a==0):
    for x in range(3):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)
if(a==1):
    for x in range(2):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)
if(a==2):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(1)
        
    GPIO.cleanup()    
        
# time.sleep()
# GPIO.cleanup()   

# if(a ==1):
#     for i in range(3):
#         activate_buzzer(1)
#         time.sleep(1)
#         GPIO.cleanup()   
        

     
        
                