
import sys

from PySide6.QtWidgets import QApplication

from ui import UnitConverter
from styles import APP_STYLE


def main():
    app = QApplication(sys.argv)

    # Apply the stylesheet
    app.setStyleSheet(APP_STYLE)

    window = UnitConverter()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()