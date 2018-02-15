1.0 Introduction
This product can only work (at this stage) if your computer is connected to EERover. 
Our project consists of 5 parts: 

1.1 main.py
This python script is installed on the ESP8266 to interface with the colour sensor Adafruit-TCS34725. The address on the writeto() and readfrom() is inferred from the data sheet provided by Adafruit. It processes the raw colour data in the form of temperature, lux, RGB, hex and HSL, and sends to the Broker. 

1.2 client.py
client.py runs on the client (i.e your computer), and it connects to the Broker to receive the data which it subscribes to, i.e the data from the ESP8266 of the colour data. When message is received, it then transfers the data to server.py.

1.3 server.py
This script acts as an interface between the frontend website for demo and backend for receiving data from client.py. It utilises FLASK framework to get requests and return the required data back to the sender. It also renders the index.html in the folder 'template' which runs on the javascript and css in folder 'static'. 

1.4 Demo webpage
The demo webpage is rendered via FLASK framework, which reads from folders "template" and "static". To make the webpage runs as expected, one is required to install FLASK framework through command "pip3 install flask", and then go to the path containing server.py, run the command "FLASK_APP=server.py flask run". After then, the page can be visited through browser with address: http://127.0.0.1:5000 (local host). 

1.5 Marketing webpage
Marketing webpage can be visited in folder Marketing/Arcus. Simple open the index.html to view the webpage, as it is a static webpage. 