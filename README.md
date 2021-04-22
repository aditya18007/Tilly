# Solange
Use tor proxies and selenium to get latest tweet from twitter
## Dependencies

### Tor 
To make our request appear not automatic and add bit of indirection, we will create tor circuits for every query and 
destroy all previous created circuits.

#### Tor daemon
Tor daemon process creates and destroys circuits. 
**NOTE : Tor browser is just a frontend to this process. Browser is not tor.**  

##### apt
```
sudo apt-get install tor
```

##### Build from source
* https://tor.stackexchange.com/questions/75/how-can-i-install-tor-from-the-source-code-in-the-git-repository 
* (works as of April,2021)

#### Stem
* Stem is a simple library that communicates with tor process and provides a python API to do the tasks.
```
pip3 install stem
```

### Selenium
* Selenium is a browser testing tool kit that can be used to repeat tasks. 
* You will need to install chrome selenium driver and set path. Search google on how to setup selenium.
```
pip3 install selenium

```

## What is happening ?

```
start_url = "https://twitter.com/search?q=delhi%20verified%20(oxygen%20OR%20bed)&src=typed_query&f=live" 
my_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]'
```
#### Opening page
If you open twitter without login and search something, and go to `latest` tab, `start_url` is the kind of link you will get. In the above url, my search was `delhi verified (oxygen OR bed)`. Try it on browser and you should see results. Selenium will simply open it on a browser. 
#### MLabour
* This is manual stuff. Go to a tweet and `inspect` on chrome. It will giv you how it looks in html. Go over the `div` and right-clik to copy its `full xpath` You have to extract its xpath. Seleniumn will use this xpath to access `div`. 
* After it has div, selenium will get the text.

#### Random sleeps
* After `driver.get(start_url) ` there is a sleep. This is because it takes time to get the webpage. If this sleep is not there, selenium will simply find the element and give error as full webpage is not loaded. 
* At the start of every loop there is a sleep. Its purpose is to make queries appear not automatic. I do not know if it has any impact.
