import pytest
from PySide2.QtWidgets import QApplication


@pytest.fixture(name="qapplication", scope="session", autouse=True)
def qapplication_fixture() -> QApplication:
    application = QApplication.instance()
    if application is None:
        application = QApplication(["-platform", "minimal"])

    return application
