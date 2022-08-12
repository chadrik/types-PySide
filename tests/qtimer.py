# from typing_extensions import assert_type
from PySide2.QtCore import QTimer, Signal, SignalInstance

timout_sig_unbound: Signal = QTimer.timeout

timer = QTimer()
timeout_sig_bount: SignalInstance = timer.timeout

timer.timeout.connect(lambda: None)
