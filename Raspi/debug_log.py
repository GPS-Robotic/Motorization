# This is a function to control console-output and to safe it to a file

import time

class debug_print:
	def __init__(self, debug_level=0, save_debug=False, filename="", save_level="", time_stamp=False):
		self.save_level=save_level
		if save_level == "":
			self.save_level = debug_level
		
		self.filename = filename
		if filename == "":
			self.filename="debug"+str(time.time())+".txt"

		self.debug_level = debug_level
		self.time_stamp = time_stamp
		self.save_debug = save_debug

		if save_debug:
			self.log_file=open(self.filename, 'a')
			self.opened = True

	def prt(self, message, level, instance=""):
		total_message = "[" + str(level) + "] "
		if self.time_stamp:
			total_message += str(time.time()) + " "
		if instance != "":
			total_message += str(instance) + ": "
		total_message +=  str(message)

		if level >= self.debug_level:
			print total_message

		if level >= self.save_level and self.save_debug:
			self.log_file.write(total_message + "\n")			

	def stop(self):
		if self.opened:
			self.log_file.close()
			self.opened = False
