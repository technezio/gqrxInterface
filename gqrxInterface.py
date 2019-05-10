################################################################################
# Remote control library for gqrx via telnet
#
# GPLv3
# luca@glgprograms.it
#
#
# List of available methods:
# Gqrx(host="127.0.0.1", port=7356)
# send_cmd(s)
# get_frequency()
# set_frequency(f)
# get_demodulator()
# set_demodulator(mode, width)
# get_signal()
# get_squelch()
# set_squelch(sql)
# start_recording()
# stop_recording()
################################################################################

import telnetlib
import sys
from time import sleep

class Gqrx:
	__tn_handler = None
	__open_socket = False
	
	def __init__(self, host="127.0.0.1", port=7356):
		try:
			self.__tn_handler = telnetlib.Telnet(host, port)
		except ConnectionRefusedError:
			raise ConnectionRefusedError

		self.__open_socket = True


	def send_cmd(self, s):
		""" Send a command via telnet and return the answer
		
		Args:
			s (str): command to send
		
		Return:
			str: gqrx answer
		"""

		if self.__open_socket == False:
			print("Connection is closed!")
			return False
		
		cmd = s + '\n'
		cmd = cmd.encode('UTF-8')
		self.__tn_handler.write(cmd)
		sleep(0.3)		# Wait answer
		try:
			ret = self.__tn_handler.read_eager()
		except EOFError:
			print("Connection closed")
			sys.exit(1)
		
		return ret.decode('UTF-8')


	def get_frequency(self):
		""" GET gqrx listening frequency

		Args: -
		
		Return:
			str: gqrx response + frequency
		"""

		return self.send_cmd('f')


	def set_frequency(self, f):
		""" SET listening frequency to f

		Args:
			f (int): target frequency
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('F ' + str(f))


	def get_demodulator(self):
		""" Get demodulator mode and passband [Hz]

		Args:
			None

		Return:
			(str, int): demodulator mode and passband [Hz]
		"""

		ret = self.send_cmd('m')
		ret = ret.split('\n')
		ret_tuple = (ret[0], int(ret[1]))	# (mode, passband width)
		return ret_tuple


	def set_demodulator(self, mode, width):
		""" Set demodulator mode and passband [Hz]

		Args:
			mode (str): demodulator mode (OFF RAW AM FM WFM WFM_ST WFM_ST_OIRT
			LSB USB CW CWU CWR CWL)
			width (int): passband filter width [Hz]

		Return:
			str: gqrx response
		"""

		width = str(width)

		return self.send_cmd('M ' + mode + ' ' + width)


	def get_signal(self):
		""" Get SIGNAL strenght [dBFS]

		Args:
			None
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('l STRENGTH')

	
	def get_squelch(self):
		""" Get SQUELCH level [dBFS]

		Args:
			None
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('l SQL')


	def set_squelch(self, sql):
		""" Set SQUELCH threshold to sql [dBFS]

		Args:
			sql (int): squelch level to be set
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('l SQL ' + str(sql))
 

	def start_recording(self):
		""" Start audio recording by sending AOS event

		Args:
			None
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('AOS')
	

	def stop_recording(self):
		""" Stop audio recording by sending LOS event

		Args:
			None
		
		Return:
			str: gqrx response
		"""

		return self.send_cmd('LOS')


if __name__ == "__main__":
	''' Test program '''

	gqrx_conn = Gqrx()					# Connect
	gqrx_conn.send_cmd('F 144800000')	# Set a random frequency
