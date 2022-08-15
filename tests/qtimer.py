# from typing_extensions import assert_type
from PySide2.QtCore import QTimer, Signal, SignalInstance

timout_sig_unbound: Signal = QTimer.timeout
assert isinstance(timout_sig_unbound, Signal)

timer = QTimer()
timeout_sig_bount: SignalInstance = timer.timeout
assert isinstance(timeout_sig_bount, SignalInstance)

timer.timeout.connect(lambda: None)
