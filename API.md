# API and Usage

## `start_torProcess()`

* Start tor process is going to start a tor daemon with configuration  

  * ```python
    SOCKS_PORT = 9050
    CONTROL_PORT = 9051
    tor_process = stem.process.launch_tor_with_config(
        config = {
            'SocksPort': str(SOCKS_PORT)
            ,'ControlPort':str(CONTROL_PORT)
        },
       init_msg_handler = print_bootstrap_lines,
    )
    ```

  * `print_bootstrap_lines` is simply going to print tor messages on terminal.

  * Directly from here : https://stem.torproject.org/tutorials.html

* Remember to call this function before beginning scrapping. 
* Any communications using `SOCKS_PORT` will go through tor network.
* We can send messages to `CONTROL_PORT` and control how tor process and get information from tor process .
* `stem` provides `Controller` object.

## `createNewCircuit()`

* To create indirection, we will create new circuits for every query.

* We create a controller to communicate with tor. 

  * ```python
    with Controller.from_port('127.0.0.1',9051) as controller:
    ```

* Each circuit has a circuit ID associated with it.

* First step is to get ID of all active circuits and close them 

  * ```python
    active_circuits = []
    
    for i in controller.get_circuits():
        for controlLine in i:
            id = controlLine.split(' ')[1]
    		active_circuits.append(id)
    for id in active_circuits:
        controller.close_circuit(id)        
    ```

  * `i` is a string.

* Next step is to create a circuit. 

  * Passing 0 as circuit ID, controller will create a circuit.

  * ```python
    controller.extend_circuit(0)
    ```

## `randomSleep(start,end)`

* Generate a random int from start to end and wait for that many seconds.

## `checkTorLoop(driverPath)`

* `driverPath` : Path to chrome web driver executable. 
* Download from here : https://chromedriver.chromium.org/downloads
* https://check.torproject.org/ is a website to check whether you are connected using  tor network. 

* This loop will open the website 5 times. You should see that the web page shows successfully connected using tor. 

* It will also show your IP address. Ideally it should be different as we are creating a new circuit every time.
* Run it to test if selenium is correctly connecting using tor. 

## `twitterLoop(xpath,url,pathToDriver)`

* `xpath` : full `xpath` of the `html` element you want .
* `url` : `url` of the website you want to access. 
* `pathToDriver` : Path to chrome web driver executable. 

* What it does is, opens the page, gets the division and prints the text. If there is some error it will connect again.
* **NOTE**  : Wait before getting element from division is to ensure that web page is loaded fully. It takes time and is slower on tor.  It is random to add some sort of indirection. 