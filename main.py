#  __     ________ ______ _      _____ _____ _    _ _______   _____        _   _ ______ _      
#  \ \   / /  ____|  ____| |    |_   _/ ____| |  | |__   __| |  __ \ /\   | \ | |  ____| |     
#   \ \_/ /| |__  | |__  | |      | || |  __| |__| |  | |    | |__) /  \  |  \| | |__  | |     
#    \   / |  __| |  __| | |      | || | |_ |  __  |  | |    |  ___/ /\ \ | . ` |  __| | |     
#     | |  | |____| |____| |____ _| || |__| | |  | |  | |    | |  / ____ \| |\  | |____| |____ 
#  __ |_|  |______|______|______|_____\_____|_|  |_|  |_|    |_| /_/    \_\_| \_|______|______|
#  \ \    / /  ____|  __ \ / ____|_   _/ __ \| \ | | /_ |                                      
#   \ \  / /| |__  | |__) | (___   | || |  | |  \| |  | |                                      
#    \ \/ / |  __| |  _  / \___ \  | || |  | | . ` |  | |                                      
#     \  /  | |____| | \ \ ____) |_| || |__| | |\  |  | |                                      
#  __  \/   |______|_|_ \_\_____/|_____\____/|_| \_|  |_|                                      
#  \ \        / /\   | |    |_   _|  ____| \ | |                                               
#   \ \  /\  / /  \  | |      | | | |__  |  \| |                                               
#    \ \/  \/ / /\ \ | |      | | |  __| | . ` |                                               
#     \  /\  / ____ \| |____ _| |_| |____| |\  |                                               
#      \/  \/_/    \_\______|_____|______|_| \_|   







import sys
sys.path.insert(1, 'py_modules')

from flask import Flask, request, send_file
from yeelight import Bulb
app = Flask(__name__)
import json, os 




with open('settings.json') as json_file:
	settings = json.load(json_file)


def render_template(file):
	return open(file, "r").read()

def brighttocolor(p=0):
	if p < 10:
		return "rgb(19,19,19)"
	elif p < 20:
		return "rgb(39,39,39)"
	elif p < 30:
		return "rgb(61,61,61)"
	elif p < 40:
		return "rgb(84,84,84)"
	elif p < 50:
		return "rgb(109,109,109)"
	elif p < 60:
		return "rgb(134,134,134)"
	elif p < 70:
		return "rgb(160,160,160)"
	elif p < 80:
		return "rgb(187,187,187)"
	elif p < 90:
		return "rgb(215,215,215)"
	else:
		return "rgb(243,243,243)"



def lightcmd(ip=None, cmd=None):
	if ip == None or cmd == None:
		pass
	else:	
		try:
			bulb = Bulb(ip)
			if cmd == "TOGGLE":
				bulb.toggle()
				if bulb.get_properties()['power'] == "on":
					return "rgb(255, 255, 255)"
				else:
					return "rgb(0,0,0)"
			elif cmd == "DECREASE_BRIGHTNESS":
				bulb.set_brightness(int(bulb.get_properties()['bright'])-25)
				return brighttocolor(int(bulb.get_properties()['bright']))
			elif cmd == "INCREASE_BRIGHTNESS":
				bulb.set_brightness(int(bulb.get_properties()['bright'])+25)
				return brighttocolor(int(bulb.get_properties()['bright']))
			elif cmd == 'SET_COLOR" "255" "0" "0':
				bulb.set_rgb(255, 0, 0)
				RGBint = int(bulb.get_properties()['rgb'])
				R,G,B = (RGBint >> 16) & 255, (RGBint >> 8) & 255,RGBint & 255
				return f"rgb({R}, {G}, {B})"
			elif cmd == 'SET_COLOR" "0" "255" "0':
				bulb.set_rgb(0, 255, 0)
				RGBint = int(bulb.get_properties()['rgb'])
				R,G,B = (RGBint >> 16) & 255, (RGBint >> 8) & 255,RGBint & 255
				return f"rgb({R}, {G}, {B})"
			elif cmd == 'SET_COLOR" "100" "150" "200':
				bulb.set_rgb(100, 150, 200)
				RGBint = int(bulb.get_properties()['rgb'])
				R,G,B = (RGBint >> 16) & 255, (RGBint >> 8) & 255,RGBint & 255
				return f"rgb({R}, {G}, {B})"
			elif cmd == "DECREASE_TEMPERATURE":
				bulb.set_color_temp(int(bulb.get_properties()['ct'])+1000)
				return f"rgb{settings['kelvin_table'][bulb.get_properties()['ct']]}"
			elif cmd == "INCREASE_TEMPERATURE":
				bulb.set_color_temp(int(bulb.get_properties()['ct'])-1000)
				return f"rgb{settings['kelvin_table'][bulb.get_properties()['ct']]}"
		except Exception as e:
			print(e)
			return "<p style=\"color:red\">Erreur: La lumière n'est pas alimentée.</p>"


@app.route("/", methods=['GET', 'POST'])
def index():
	lights = ""
	for light in settings['lights']:
		name = light['name'].replace('_', ' ').capitalize()
		lights = f"{lights}<option value='{light['ip']}''>{name}</option>"
	return render_template("index.html").replace('@lightspy', lights)

@app.route('/style.css')
def style():
	return render_template("style.css")

@app.route('/get_image')
def get_image():
	file = request.args.get('filename')
	format = request.args.get('filename').split('.')[1]
	return send_file(file, mimetype=f'image{format}')

@app.route('/LightSettings')
def settingsLights():
	x = lightcmd(ip=request.args.get('ip'), cmd=request.args.get('cmd'))
	return {"return": x}


if __name__ == '__main__':
	app.run(debug=settings['debug'], host="0.0.0.0", port=settings['port'])
