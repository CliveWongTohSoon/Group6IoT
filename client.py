import paho.mqtt.client as mqtt
import json
import math
import requests

#Check whether client is connected
print("Hello World!")

#Create a list of database for matching
#Can use a map to match colour to list of products to send to server
color_in_hsl = {"dark brown": '24,83,33', "dark yellow": "44,100,50", "orange": "24,100,46", "black": '0,0,0', "white": '0,0,100', "red": '0,100,57', "green": '120,100,50', "yellow": '58,100,50', "blue": '240,62,39', "purple": '270,100,50'}
color_r = {"brown1": '662200', "brown2": '802b00', "brown4": 'cc4400', "brown5": 'e64d00', "yellow1": "ffcc00", "yellow2": "ffd11a", "yellow3": "ffdb4d", "yellow4": "ffe066", "yellow5": "ffe680", "black": '000000', "white": "ffffff", "red1": 'cc0000', "red2": 'ff0000', "red3": 'ff1a1a', "red4": 'ff4d4d', "red5": 'b30000',"red6": '990000', "red7": '800000'}
color_g = {"green1": '003300', "green2": '006600', "green3": '009900', "green4": '00cc00', "green5": '00ff00'}
color_b = {"blue1": '000099', "blue2": '0000cc', "blue3": '0000ff', "blue4": '1a1aff', "blue5": '3333ff', "purple1": '1a0033', "purple2": '400080', "purple3": '5900b3', "purple4": '6600cc', "purple5": '8000ff'}

#Colour matching using hex/RGB
def getClosestColor(hex_val):
    closest_color = list(color_r.keys())[0]
    #Set the maximum possible matching parameter
    y = 255**2.0 + 255**2.0 + 255**2.0
    min_val = math.sqrt(y)

    #color from sensor
    R = int(hex_val[:2], 16)
    G = int(hex_val[2:4], 16)
    B = int(hex_val[4:], 16)

    if(R>=G and R>=B):
        colors=color_r
    elif(G>=B):
        colors=color_g
    else:
        colors=color_b

    for color_name, color_value in colors.items():
        #color from data
        r = int(color_value[:2], 16)
        g = int(color_value[2:4], 16)
        b = int(color_value[4:], 16)
        #Color matching algorithm using sensitivity and colour difference
        #human eye sensitivity is 0.3 to red, 0.59 to green, and 0.11 to blue
        diff = 0.3 * abs(r - R) + 0.59 * abs(g - G) + 0.11 * abs(b - B)

        if diff < min_val:
            min_val = diff
            closest_color = color_name
            closest_color_value = color_value

    closest_color = str(closest_color_value)
    your_color = hex_val

    #Send to server
    data_to_send = {'closest': closest_color, 'ori-color': your_color}
    res = requests.post('http://127.0.0.1:5000/tests', json=data_to_send)
    #Give notice when connected to server
    print('response from server:', res.text)

#Alternative method of using HSL to match colour 
def get_closest_color(hue, saturation, lightness):
    closest_color = list(color_r.keys())[0]
    min_val = 47.5 * 360 + 28.75 * 100 + 23.75 * 100

    for color_name, color_value in color_in_hsl.items():
        #hsl from data
        h = int(color_value.split(',')[0])
        s = int(color_value.split(',')[1])
        l = int(color_value.split(',')[2])

        #color from sensor
        H = hue
        S = saturation
        L = lightness

        #human eye sensitivity is 0.3 to red, 0.59 to green, and 0.11 to blue
        diff = 47.5 * abs(h - H) / 3.6 + 28.75 * abs(s - S) + 23.75 * abs(l - L)

        if diff < min_val:
            min_val = diff
            closest_color = color_name

    print ('hue:', hue, 'saturation:', saturation, 'lightness:', lightness, "is closest to color:", closest_color)

#When connected, gives notice
def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("esys/Arcus/#")

#On Message, send the data to server
def on_message(client, userdata, msg):
    color_hex_input = json.loads(msg.payload)
    hex_val = color_hex_input['hex']
    hue = color_hex_input['Hue']
    saturation = color_hex_input['Saturation']
    lightness = color_hex_input['Lightness']

    #We are sending hex_val in this case, data from get_closest_color is not used to send to the server
    getClosestColor(hex_val)
    get_closest_color(hue, saturation, lightness)

#main
def main():
	client = mqtt.Client()
	client.subscribe("esys/Arcus/color")
	client.on_connect = on_connect
	client.on_message = on_message
	#Connect to EERover
	client.connect('192.168.0.10')
	client.loop_forever()

if __name__ == "__main__":
	main()