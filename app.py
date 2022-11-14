import eel
import serial
from serial.tools import list_ports
import threading
import json
import os



event = None



@eel.expose
def get_com_list():
	com_list = [str(i) for i in list_ports.comports()]
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
		if event.is_set():
			break
		try:
			string = ""
			while True:
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
	global event

	if event is not None:
		event.set()
	return 1


def close_callback(route, websockets):
	if not websockets:
		exit()


if __name__ == '__main__':
	eel.init('web')
	eel.start('main.html', size=(800, 500), close_callback=close_callback)