import eel
import serial
from serial.tools import list_ports
import threading
import requests
import webbrowser
import atexit
from pydantic.v1.typing import Optional


REPOS_OWNER = "Grigoriy457"
REPOS_NAME = "python-serial-projector"
VERSION = (1, 2)
event: Optional[threading.Event] = None


@eel.expose
def check_for_update():
	response = requests.get(f"https://api.github.com/repos/{REPOS_OWNER}/{REPOS_NAME}/tags")
	if response.status_code == 200:
		last_ver = tuple(map(int, response.json()[0]["name"][1:].split(".")))
		print("Latest version:", last_ver)
		return last_ver > VERSION, last_ver
	return False, VERSION


@eel.expose
def open_last_version(version: tuple):
	webbrowser.open_new(f"https://github.com/{REPOS_OWNER}/{REPOS_NAME}/releases/tag/v{'.'.join(map(str, version))}")


@eel.expose
def get_com_list():
	com_list = [i.name for i in list_ports.comports()]
	return com_list


def serial_reader(port, bit_rate, data_bits, parity_bit, stop_bits, event):
	bytesize = serial.EIGHTBITS
	if data_bits == "7":
		bytesize = serial.SEVENBITS

	parity = serial.PARITY_NONE
	if parity_bit == "odd":
		parity = serial.PARITY_ODD
	elif parity_bit == "even":
		parity = serial.PARITY_EVEN

	stopbits = serial.STOPBITS_ONE
	if stop_bits == "two":
		stopbits = serial.STOPBITS_TWO

	try:
		s = serial.Serial(port=port.split(" - ")[0], baudrate=int(bit_rate), parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=0)
	except serial.serialutil.SerialException:
		eel.sleep(0.05)
		eel.cant_connect()
		return
	while True:
		try:
			string = ""
			while True:
				if event.is_set():
					s.close()
					return
				if s.in_waiting != 0:
					symbol = s.readline()
					try:
						symbol = symbol.decode()
						string += symbol
						if symbol.endswith("\n"):
							break
					except UnicodeDecodeError:
						print("[ERROR]:", symbol)

			string = string.strip()
			if string != "":
				print("[SERIAL]:", string)
				eel.set_text(string)
		except serial.serialutil.SerialException:
			eel.device_lost()
			break


@eel.expose
def py_connect(port, bit_rate, data_bits, parity_bit, stop_bits):
	global event

	if port == "":
		return

	event = threading.Event()
	threading.Thread(target=serial_reader, args=(port, bit_rate, data_bits, parity_bit, stop_bits, event)).start()
	return 1


@eel.expose
def py_disconnect():
	if event is not None:
		event.set()
		eel.sleep(0.05)
	return 1


def close_callback(route, websockets):
	if not websockets:
		exit()


if __name__ == '__main__':
	eel.init('web')
	eel.start('main.html', size=(800, 500), close_callback=close_callback, port=18080)

	atexit.register(lambda: eel.close_window())
