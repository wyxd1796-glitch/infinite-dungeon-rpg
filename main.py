from pathlib import Path
import sys

# File associations may launch the system Python instead of the game environment.
if __name__ == '__main__' and sys.prefix == sys.base_prefix:
    import subprocess
    local_python = Path(__file__).parent / '.venv' / 'Scripts' / 'python.exe'
    if local_python.is_file():
        sys.exit(subprocess.call([str(local_python), str(Path(__file__).resolve()), *sys.argv[1:]]))

from PySide6.QtWidgets import QApplication
from ui.property_window import PropertyWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('INFINITE')
    app.setOrganizationName('InfiniteDungeon')
    window = PropertyWindow(Path(__file__).parent)
    window.show()
    window.raise_()
    window.activateWindow()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
