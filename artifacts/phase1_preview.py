import os
os.environ['QT_QPA_PLATFORM']='offscreen'
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from ui.property_window import PropertyWindow
from core.game_engine import GameEngine

ROOT=Path(__file__).resolve().parents[1]
app=QApplication.instance() or QApplication([])
QFontDatabase.addApplicationFont('C:/Windows/Fonts/malgun.ttf')
w=PropertyWindow(ROOT,ROOT/'artifacts/phase1_preview_saves',ROOT/'artifacts/phase1_preview.ini')
w.prevent_autosave=True; w.engine=GameEngine(ROOT/'content',seed=7); w.engine.s['highest']=100; w.engine.refresh_shop(); w.show()
def capture(name):
    for _ in range(4): app.processEvents()
    w.grab().save(str(ROOT/'artifacts'/name))
w.selected.update(shop_kind='장비',shop_item='catalogue.v3.EQ090',shop_filter='전체',shop_search=''); w.resize(268,861); w.navigate('거점','상점'); capture('phase1_shop.png')
w.resize(250,400); capture('phase1_shop_minimum.png')
w.resize(268,861); w.engine.execute('enter',floor=50); w.engine.start_combat('boss'); w.engine.apply_status(1,'enemy','player',1); w.navigate('던전','전투'); capture('phase1_combat.png')
w.engine.s.update(mode='explore',enemy=None); w.engine.grant_item('catalogue.v3.CON001',110); w.navigate('가방','소비품'); capture('phase1_pending.png')
w.close()
