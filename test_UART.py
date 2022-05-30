'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''



# import serial
# from time import sleep

# ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
# while True:
#     received_data = ser.read()              #read serial port
#     sleep(0.03)
#     data_left = ser.inWaiting()             #check for remaining byte
#     received_data += ser.read(data_left)
#     print (received_data)                   #print received data
#     ser.write(received_data)                #transmit data serially 

# import serial
# ser = serial.Serial("COM4", 9600)
# while True:
#      #ser.write("hello".encode())
#      test = str(10)
#      ser.write(test.encode())
#      #cc=str(ser.readline())
#      #print(cc[2:][:-5])



import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        print("{}".format(port))