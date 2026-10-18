"""Offscreen visual checks; all settings and saves remain in artifacts/."""
import copy
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from core.game_engine import GameEngine
from ui.property_window import PropertyWindow

ROOT=Path(__file__).resolve().parents[1]

def run():
    app=QApplication.instance() or QApplication([])
    QFontDatabase.addApplicationFont('C:/Windows/Fonts/malgun.ttf')
    w=PropertyWindow(ROOT,ROOT/'artifacts/phase2_preview_saves',ROOT/'artifacts/phase2_preview.ini')
    w.prevent_autosave=True; w.engine=GameEngine(ROOT/'content',seed=7); w.show()
    def capture(name):
        for _ in range(4): app.processEvents()
        assert w.tree.horizontalScrollBar().maximum()==0
        w.grab().save(str(ROOT/'artifacts'/name))
    for width,height,label in ((268,861,'normal'),(250,400,'minimum')):
        w.resize(width,height); w.engine=GameEngine(ROOT/'content',seed=7)
        w.selected['skill_view_액티브']='learn'; w.selected['skill_액티브']='phase2.skill.SKL006'; w.navigate('스킬','액티브'); capture(f'phase2_skill_{label}.png')
        w.engine.s.update(mode='event',event=copy.deepcopy(w.engine.content.by_id['phase2.event.EVT022'])); w.engine.p['hp']=1
        w.navigate('던전','이벤트'); capture(f'phase2_event_{label}.png')
        w.tree.scrollToBottom(); capture(f'phase2_event_bottom_{label}.png')
    w.close()

if __name__=='__main__': run()
