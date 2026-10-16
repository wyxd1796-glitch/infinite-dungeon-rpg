"""Exercise production entry points with isolated saves and timed Qt shutdown."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[1]
HOOK = '''
import os
from pathlib import Path
from PySide6.QtCore import QTimer
from ui.property_window import PropertyWindow
original = PropertyWindow.__init__
def isolated(self, root, *args, **kwargs):
    target = Path(os.environ['INFINITE_RELEASE_SANDBOX'])
    original(self, root, target / 'saves', target / 'settings.ini')
    def finish():
        assert self.isVisible()
        assert self.engine.s['save_schema_version'] == 3
        self.close()
        (target / 'closed.txt').write_text('closed', encoding='utf-8')
    QTimer.singleShot(300, finish)
PropertyWindow.__init__ = isolated
'''


def run():
    results = []
    with tempfile.TemporaryDirectory(prefix='infinite-release-') as folder:
        target = Path(folder)
        (target / 'sitecustomize.py').write_text(HOOK, encoding='utf-8')
        env = dict(os.environ, QT_QPA_PLATFORM='offscreen',
                   PYTHONPATH=os.pathsep.join((folder, str(ROOT))),
                   INFINITE_RELEASE_SANDBOX=folder)
        commands = [('main.py', [sys.executable, str(ROOT / 'main.py')])]
        if os.name == 'nt':
            commands.append(('start.bat', [os.environ.get('COMSPEC', 'cmd.exe'), '/c', str(ROOT / 'start.bat')]))
        for name, command in commands:
            for cycle in (1, 2):
                marker = target / 'closed.txt'
                marker.unlink(missing_ok=True)
                result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=30)
                assert result.returncode == 0, (name, result.stderr)
                assert marker.exists(), (name, 'window did not close normally')
                saved = json.loads((target / 'saves/slot_1.json').read_text(encoding='utf-8'))
                assert saved['save_schema_version'] == 3
                results.append(dict(entry=name, cycle=cycle, exit_code=result.returncode, saved=True))
        if os.name == 'nt':
            failure = target / 'failure'
            failure.mkdir()
            shutil.copy2(ROOT / 'start.bat', failure / 'start.bat')
            (failure / 'main.py').write_text("raise RuntimeError('release-log-probe')\n", encoding='utf-8')
            failed_env = dict(env, PATH=str(Path(sys.executable).parent) + os.pathsep + env['PATH'])
            subprocess.run([os.environ.get('COMSPEC', 'cmd.exe'), '/c', str(failure / 'start.bat')],
                           cwd=failure, env=failed_env, input=b'\n', capture_output=True, timeout=30)
            logs = list(failure.glob('startup-*.log'))
            assert len(logs) == 1 and 'release-log-probe' in logs[0].read_text(encoding='utf-8')
            results.append(dict(entry='start.bat', injected_failure=True, error_log=True))
    destination = ROOT / 'artifacts/release_1_2'
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'launch.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results))


if __name__ == '__main__':
    run()
