from PySide2.QtCore import QCoreApplication

s: str = "abc"
s = QCoreApplication.translate("GitFlowAdvanceIntBranch", "hidden", None)
s = QCoreApplication.translate("GitFlowAdvanceIntBranch", "hidden", "some help")
assert isinstance(s, str)
