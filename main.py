from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication
from ui.property_window import PropertyWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('INFINITE')
    app.setOrganizationName('InfiniteDungeon')
    window = PropertyWindow(Path(__file__).parent)
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
