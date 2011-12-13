from trends.analysis.listener import Listener
from trends.analysis.statistician import Statistician

import threading 
import signal

# Condition variable that initiates termination
terminate_please = threading.Event()

def do_exit(sig, stack):
	print "Main Thread: Termination Requested"
	terminate_please.set()

def main():
	"""
	Starts the worker threads, and handles termination.

    In Python, signals are received by the main thread. So, the main thread,
	captures the SIGINT signal, and sets an Event. The worker threads
	detect that the Event is set, and terminate.

	If a worker thread terminates prematurely, it will generate a SIGINT
	signal. The signal will be captured by the main thread, which will handle
	the graceful termination of all threads.
	"""

	# Create and start threads
	workers = (
		Listener(terminate_please),   	# Listen to the Streaming API
		Statistician(terminate_please), # Compute statistics about data
	)
	for worker in workers:
		worker.start()

    # Register handling of Ctrl-C
	signal.signal(signal.SIGINT, do_exit)
	# Pause and wait for Ctrl-C
	signal.pause()
	
	print "Main Thread: Waiting for (remaining) worker threads to finish"
	for worker in workers:
		# If the thread hasn't already finished
		if worker:
			worker.join()
	print "Main Thread: Terminating"

	
