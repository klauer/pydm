import epics
import numpy as np
from .plugin import PyDMPlugin, PyDMConnection
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject, Qt

class Connection(PyDMConnection):
	def __init__(self, widget, pv, parent=None):
		super(Connection, self).__init__(widget, pv, parent)
		self.add_listener(widget)
		self.pv = epics.PV(pv, callback=self.send_new_value, connection_callback=self.send_connection_state, form='ctrl')
	
	def send_new_value(self, pvname=None, value=None, severity=None, *args, **kws):
		self.new_value_signal.emit(str(value))
		if severity != None:
			self.new_severity_signal.emit(int(severity))
			
	def send_connection_state(self, pvname=None, conn=None, *args, **kws):
		self.connection_state_signal.emit(conn)
	
	@pyqtSlot(str)
	def put_value(self, new_val):
		self.pv.put(new_val)
		
	def add_listener(self, widget):
		self.connection_state_signal.connect(widget.connectionStateChanged, Qt.QueuedConnection)
		self.new_value_signal.connect(widget.recieveValue, Qt.QueuedConnection)
		self.new_severity_signal.connect(widget.alarmSeverityChanged, Qt.QueuedConnection)
		widget.send_value_signal.connect(self.put_value, Qt.QueuedConnection)

class EPICSPlugin(PyDMPlugin):
	protocol = "ca://"
	connection_class = Connection
			
