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

def start_torProcess():

    print(term.format("Starting Tor:\n", term.Attr.BOLD))

    SOCKS_PORT = 9050
    CONTROL_PORT = 9051

    tor_process = stem.process.launch_tor_with_config(
        config = {
            'SocksPort': str(SOCKS_PORT)
            ,'ControlPort':str(CONTROL_PORT)
        },
        init_msg_handler = print_bootstrap_lines,
    )
    return tor_process

def createNewCircuit():
    with Controller.from_port('127.0.0.1',9051) as controller:
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

def checkTorLoop(driverPath):
    """
    check.torproject.org is a website to check whether you are connected using 
    tor network. This loop will open the website 5 times. You should see that 
    the webpage shows succesfully connected using tor. 

    It will also show your IP address. Ideally it should be different as you will 
    we are creating a new circuit every time.
    """

    check_tor_url = "https://check.torproject.org/"
    
    for i in range(5):
        print(f"Test : {i}")
        createNewCircuit()
        options = webdriver.ChromeOptions()
        proxy = '127.0.0.1:9050'
        options.add_argument('--proxy-server=socks5://' + proxy)   
        driver = webdriver.Chrome(executable_path=driverPath,options=options)
        print('Opening Page')
        driver.get(check_tor_url)  
        print('Waiting for 10 seconds')
        time.sleep(10)
        driver.close()
        print()

def twitterLoop(xpath,url,pathToDriver):

    count = 0
    prev = ""
    
    while True:

        print(f"Executing {count}")
        createNewCircuit()
        #randomSleep(20,30)
        options = webdriver.ChromeOptions()
        proxy = '127.0.0.1:9050'
        options.add_argument('--proxy-server=socks5://' + proxy)   
        driver = webdriver.Chrome(executable_path=pathToDriver,options=options)
        print('\tOpening Page')
        driver.get(url)  
        randomSleep(30,40)
        print('\tReading Page')
        try:
            element = driver.find_element_by_xpath(xpath)
            response = element.text
            if response == prev:
                print("\t\tNo new tweet")
                driver.close()
                print("------------------------------------------")
                continue
            prev = response 
            print("\t\t"+response)
        except:
            print("------------------------------------------")
            driver.close()
            continue
        print("------------------------------------------")
        driver.close()
        count+=1
        print()

if __name__ == "__main__":
    
    process = start_torProcess()
    url = "https://twitter.com/search?q=delhi%20verified%20(oxygen%20OR%20bed)&src=typed_query&f=live" 
    xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]'
    #Path to chrome driver
    driver_path = "/home/aditya/Desktop/chromedriver_linux64/chromedriver"
    #checkTorLoop() Uncomment to see if 
    twitterLoop(xpath,url,driver_path)