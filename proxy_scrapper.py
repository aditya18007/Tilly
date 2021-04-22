from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import random
from platform import node
import stem.process
import time
from stem.util import term
from stem.control import Controller

def print_bootstrap_lines(line):
    #From https://stem.torproject.org/tutorials.html
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.RED))

print(term.format("Starting Tor:\n", term.Attr.BOLD))

SOCKS_PORT = 9050
CONTROL_PORT = 9051
LARGE_VALUE = str(999999)
TRUE = str(1)
FALSE = str(0)


tor_process = stem.process.launch_tor_with_config(
    config = {
        'SocksPort': str(SOCKS_PORT)
        ,'ControlPort':str(CONTROL_PORT)
    },
    init_msg_handler = print_bootstrap_lines,
)

def createNewCircuit():
    with Controller.from_port('127.0.0.1',CONTROL_PORT) as controller:
        print("\tCreating Circuit")
        active_circuits = []
        controller.authenticate()
        for i in controller.get_circuits():
            for controlLine in i:
                id = controlLine.split(' ')[1]
                active_circuits.append(id)

        for id in active_circuits:
            controller.close_circuit(id)        

        controller.extend_circuit(0)
        print('\t\tDone Creating Circuit')

def randomSleep(start,end):
    rand_sleep = random.randint(start,end) 
    print(f"\tWaiting for {rand_sleep} seconds")
    time.sleep(rand_sleep)

count = 0
prev = ""

start_url = "https://twitter.com/search?q=delhi%20verified%20(oxygen%20OR%20bed)&src=typed_query&f=live" 
my_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]'
#Path to chrome driver
path = "/home/aditya/Desktop/chromedriver_linux64/chromedriver"
while True:

    print(f"Executing {count}")
    createNewCircuit()
    randomSleep(20,30)
    driver = webdriver.Chrome(executable_path=path)
    print('\tOpening Page')
    driver.get(start_url)  
    randomSleep(10,20)
    print('\tReading Page')
    element = driver.find_element_by_xpath(my_xpath)
    response = element.text
    if response == prev:
        print("\t\tNo new tweet")
        driver.close()
        print("------------------------------------------")
        continue
    prev = response 
    print("\t\t"+response)
    print("------------------------------------------")
    driver.close()
    count+=1
    print()