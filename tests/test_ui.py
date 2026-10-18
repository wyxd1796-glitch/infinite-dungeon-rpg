import copy
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt,QPoint,QRect
from PySide6.QtGui import QFontMetrics
from PySide6.QtTest import QTest
from ui.property_window import PropertyWindow,SCREENS,WRAPPED_ROLE
from core.game_engine import GameEngine

ROOT=Path(__file__).resolve().parents[1]
app=QApplication.instance() or QApplication([])

class UITests(unittest.TestCase):
    def setUp(self):
        settings=ROOT/'artifacts/tests/ui.ini'
        if settings.exists(): settings.unlink()
        self.w=PropertyWindow(ROOT,ROOT/'artifacts/tests/ui_saves',settings); self.w.engine=GameEngine(ROOT/'content',seed=1); self.w.prevent_autosave=True; self.w.show(); app.processEvents()
    def tearDown(self): self.w.prevent_autosave=True; self.w.close(); app.processEvents()
    def test_22_screens_read_only(self):
        old=copy.deepcopy(self.w.engine.s); count=0
        for main,subs in SCREENS.items():
            for sub in subs:
                self.w.navigate(main,sub); app.processEvents(); self.assertGreater(self.w.tree.topLevelItemCount(),0); count+=1
        self.assertEqual(count,22); self.assertEqual(old,self.w.engine.s)
    def test_row_heights_resizing(self):
        w=self.w; w.navigate('캐릭터','정보'); app.processEvents(); group=w.tree.topLevelItem(0); row=group.child(0)
        self.assertEqual(w.tree.visualItemRect(group).height(),26); self.assertEqual(w.tree.visualItemRect(row).height(),25)
        w.resize(450,500); app.processEvents(); self.assertEqual(w.tree.visualItemRect(row).height(),25); self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)
    def test_click_value_once_and_screen(self):
        w=self.w; w.navigate('거점','휴식'); app.processEvents(); group=w.groups['탐험 준비']; item=group.child(1); rect=w.tree.visualItemRect(item); pos=QPoint(w.tree.columnWidth(0)+10,rect.center().y())
        QTest.mouseClick(w.tree.viewport(),Qt.LeftButton,Qt.NoModifier,pos); app.processEvents(); self.assertEqual(w.engine.s['mode'],'explore'); self.assertEqual(w.screen_key,'던전/탐험')
    def test_selection_no_turn(self):
        w=self.w; w.navigate('거점','상점'); app.processEvents(); old=copy.deepcopy(w.engine.s); combo=w.tree.itemWidget(w.groups['상품 선택'].child(1),1); combo.setCurrentIndex(1); app.processEvents(); self.assertEqual(old,w.engine.s)
    def test_combat_manual_browse(self):
        w=self.w; w.engine.execute('enter'); w.engine.start_combat(); old=copy.deepcopy(w.engine.s); w.navigate('캐릭터','정보'); app.processEvents(); self.assertEqual(w.screen_key,'캐릭터/정보'); self.assertEqual(old,w.engine.s)
    def test_collapse_restore(self):
        w=self.w; w.navigate('캐릭터','정보'); w.groups['일반'].setExpanded(False); w.navigate('던전','탐험'); w.navigate('캐릭터','정보'); self.assertFalse(w.groups['일반'].isExpanded())
    def test_relaunch_restores_ui_and_battle(self):
        w=self.w; w.engine.execute('enter'); w.engine.start_combat(); w.engine.execute('defend'); w.navigate('던전','전투'); w.resize(360,640); w.ratio=.62; w.groups['적 정보'].setExpanded(False); w.set_pin(True); w.prevent_autosave=False; w.close(); app.processEvents()
        restored=PropertyWindow(ROOT,w.store.directory,ROOT/'artifacts/tests/ui.ini'); restored.show(); app.processEvents()
        try:
            self.assertEqual(restored.engine.s['enemy'],w.engine.s['enemy']); self.assertEqual(restored.screen_key,'던전/전투'); self.assertEqual(restored.size(),w.size()); self.assertAlmostEqual(restored.ratio,.62); self.assertTrue(restored.pinned); self.assertFalse(restored.groups['적 정보'].isExpanded())
        finally:
            restored.prevent_autosave=True; restored.close(); app.processEvents()
            # Keep other test cases independent of this persisted battle.
            for file in w.store.directory.glob('slot_1.json*'): file.unlink()
    def test_event_description_spans_and_wraps_after_resize(self):
        w=self.w; text='낡은 문틈으로 푸른 빛이 새어 나옵니다. 안쪽에는 오래된 기록과 무너진 계단이 보입니다.\n문을 열거나 안전한 길을 따라 돌아갈 수 있습니다.'*3
        w.engine.s.update(mode='event',event=copy.deepcopy(w.engine.content['events'][0])); w.engine.s['event']['description']=text
        w.resize(268,861); w.navigate('던전','이벤트'); app.processEvents(); app.processEvents()
        item=w.groups['이벤트 정보'].child(2)
        self.assertTrue(item.isFirstColumnSpanned()); self.assertTrue(item.data(0,WRAPPED_ROLE)); self.assertEqual(item.text(0),text)
        rect=w.tree.visualItemRect(item); height=rect.height(); self.assertGreater(height,25)
        expected=QFontMetrics(w.tree.font()).boundingRect(QRect(0,0,rect.width()-10,100000),Qt.TextWordWrap,text).height()+12
        self.assertGreaterEqual(height,expected)
        w.resize(460,861); app.processEvents(); app.processEvents(); self.assertLess(w.tree.visualItemRect(item).height(),height)
        self.assertEqual(w.tree.visualItemRect(w.groups['이벤트 정보'].child(0)).height(),25)
        w.resize(250,400); app.processEvents(); app.processEvents(); app.processEvents()
        self.assertEqual(w.tree.columnWidth(0)+w.tree.columnWidth(1),w.tree.viewport().width())
        self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)
    def test_shop_description_refresh_is_read_only(self):
        w=self.w; w.navigate('거점','상점'); app.processEvents(); old=copy.deepcopy(w.engine.s); rng=w.engine.rng.getstate()
        kind=w.tree.itemWidget(w.groups['상품 선택'].child(0),1); kind.setCurrentText('장비'); app.processEvents(); app.processEvents()
        descriptions=[w.groups['상품 정보'].child(i) for i in range(w.groups['상품 정보'].childCount()) if w.groups['상품 정보'].child(i).data(0,WRAPPED_ROLE)]
        self.assertIn('공격력 +9~12',descriptions[0].text(0)); self.assertIn('무작위',descriptions[0].text(0))
        self.assertEqual(w.engine.s,old); self.assertEqual(w.engine.rng.getstate(),rng)
    def test_shortcuts_and_pin_state(self):
        w=self.w; old=copy.deepcopy(w.engine.s)
        for name,destination in [('record','기록/전투 통계'),('settings','설정/게임 설정'),('home','거점/휴식')]:
            QTest.mouseClick(w.shortcut_buttons[name],Qt.LeftButton); app.processEvents(); self.assertEqual(w.screen_key,destination)
        QTest.mouseClick(w.pin_button,Qt.LeftButton); app.processEvents()
        self.assertTrue(w.pinned); self.assertTrue(w.pin_button.isChecked()); self.assertTrue(w.windowFlags() & Qt.WindowStaysOnTopHint); self.assertIn('ON',w.pin_button.toolTip())
        on=w.pin_button.grab().toImage()
        self.assertEqual(on.pixelColor(1,11).name(),'#376d91')
        QTest.mouseClick(w.pin_button,Qt.LeftButton); app.processEvents(); self.assertFalse(w.pinned); self.assertFalse(w.pin_button.isChecked()); self.assertEqual(old,w.engine.s)

    def test_search_empty_and_filters_are_read_only(self):
        w=self.w; old=copy.deepcopy(w.engine.s); rng=w.engine.rng.getstate()
        for main,sub,key in [('거점','상점','shop_search'),('가방','장비','bag_search'),('가방','소비품','bag_search_소비품'),('가방','재료','bag_search_재료')]:
            w.navigate(main,sub); app.processEvents(); w.selected[key]='없는 이름 XYZ'; w.refresh(); app.processEvents()
            self.assertGreater(w.tree.topLevelItemCount(),0)
        self.assertEqual(old,w.engine.s); self.assertEqual(rng,w.engine.rng.getstate())

    def test_pending_loot_actions_and_minimum_width(self):
        w=self.w; w.engine.grant_item('catalogue.v3.CON001',110); w.navigate('가방','소비품'); w.resize(250,400)
        app.processEvents(); app.processEvents(); group=w.groups['획득 대기']
        self.assertTrue(any(group.child(i).text(0)=='받기' for i in range(group.childCount())))
        self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)

    def test_legacy_battle_render_does_not_add_fields(self):
        from core.legacy_engine import GameEngine as LegacyEngine
        w=self.w; old=LegacyEngine(ROOT/'content',seed=1); old.execute('enter'); old.start_combat()
        w.engine=GameEngine(ROOT/'content',old.s); before=copy.deepcopy(w.engine.s)
        w.navigate('던전','전투'); app.processEvents(); self.assertEqual(before,w.engine.s)

    def test_event_result_stays_visible_until_continue(self):
        w=self.w; w.engine.s.update(mode='event',event=copy.deepcopy(w.engine.content['events'][0])); w.navigate('던전','이벤트')
        w.run('event',index=1); app.processEvents(); self.assertEqual(w.screen_key,'던전/이벤트')
        self.assertNotIn('이벤트 선택',w.groups); self.assertIn('다음 진행',w.groups)
        result=w.groups['이벤트 결과'].child(3); self.assertTrue(result.isFirstColumnSpanned()); self.assertIn('지나갔습니다',result.text(0))
        turn=w.engine.s['turn']; w.run('continue_event'); app.processEvents()
        self.assertEqual(w.screen_key,'던전/탐험'); self.assertEqual(turn,w.engine.s['turn'])

    def test_phase2_skills_and_choices_at_both_sizes(self):
        w=self.w; e=w.engine
        for width,height in ((268,861),(250,400)):
            w.resize(width,height)
            w.selected['skill_view_액티브']='learn'; w.selected['skill_액티브']='phase2.skill.SKL006'; w.navigate('스킬','액티브')
            app.processEvents(); app.processEvents()
            self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)
            self.assertTrue(any('레벨 10' in w.groups['스킬 성장'].child(i).text(1) for i in range(w.groups['스킬 성장'].childCount())))
            e.s.update(mode='event',event=copy.deepcopy(e.content.by_id['phase2.event.EVT022'])); e.p['hp']=1
            before=copy.deepcopy(e.s); rng=e.rng.getstate(); w.navigate('던전','이벤트'); app.processEvents(); app.processEvents()
            group=w.groups['이벤트 선택']; wrapped=[group.child(i) for i in range(group.childCount()) if group.child(i).data(0,WRAPPED_ROLE)]
            self.assertTrue(any('사망' in item.text(0) for item in wrapped)); self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)
            for item in wrapped:
                rect=w.tree.visualItemRect(item)
                needed=QFontMetrics(w.tree.font()).boundingRect(QRect(0,0,rect.width()-10,100000),Qt.TextWordWrap,item.text(0)).height()+12
                self.assertGreaterEqual(rect.height(),needed)
            self.assertEqual(e.s,before); self.assertEqual(e.rng.getstate(),rng)
            e.s.update(mode='base',event=None); e.p['hp']=100

    def combo_values(self, group, label):
        rows=self.w.groups[group]
        row=next(rows.child(i) for i in range(rows.childCount()) if rows.child(i).text(0)==label)
        combo=self.w.tree.itemWidget(row,1)
        return [combo.itemData(i) for i in range(combo.count())]

    def test_owned_items_and_materials_refresh_after_last_consumed(self):
        w=self.w; e=w.engine
        for sub in ('소비품','재료'):
            candidates=e.available_items(sub); key=candidates[0]['id']
            for row in candidates: e.s['items'][row['id']]=0
            e.s['items'][key]=1
            w.navigate('가방',sub)
            self.assertEqual(self.combo_values('아이템 선택',sub),[key])
            e.s['items'][key]=0; w.refresh()
            self.assertEqual(self.combo_values('아이템 선택',sub),[])
            self.assertIsNone(w.selected['bag_'+sub])
        for key,_,_ in e.upgrade_materials(): e.s['items'][key]=0
        w.navigate('거점','강화')
        self.assertEqual(self.combo_values('강화 재료','사용 재료'),[])
        key=e.upgrade_materials()[0][0]; e.s['items'][key]=1; w.refresh()
        self.assertEqual(self.combo_values('강화 재료','사용 재료'),[key])

    def test_skill_owned_view_learning_and_empty_state(self):
        w=self.w; e=w.engine; key='phase2.skill.SKL003'
        before=copy.deepcopy(e.s); rng=e.rng.getstate()
        w.navigate('스킬','액티브')
        self.assertNotIn(key,self.combo_values('스킬 선택','스킬'))
        w.selected['skill_view_액티브']='learn'; w.selected['skill_액티브']=key; w.refresh()
        self.assertIn(key,self.combo_values('스킬 선택','스킬'))
        self.assertNotIn('전투 설정',w.groups)
        self.assertEqual(e.s,before); self.assertEqual(e.rng.getstate(),rng)
        e.p.update(level=5,skill_points=1); e.execute('upgrade_skill',key=key)
        w.refresh(); self.assertNotIn(key,self.combo_values('스킬 선택','스킬'))
        w.selected['skill_view_액티브']='owned'; w.refresh()
        self.assertIn(key,self.combo_values('스킬 선택','스킬'))
        e.execute('reset_skills'); w.refresh()
        self.assertNotIn(key,self.combo_values('스킬 선택','스킬'))
        for skill in e.s['skills']: e.s['skills'][skill]=0
        for sub in ('액티브','패시브'):
            w.navigate('스킬',sub); w.refresh()
            self.assertEqual(self.combo_values('스킬 선택','스킬'),[])
        w.navigate('던전','전투')
        self.assertEqual(self.combo_values('스킬 행동','선택 스킬'),[])

    def test_combat_only_learned_skills_keeps_unavailable_owned(self):
        w=self.w; e=w.engine; key='phase2.skill.SKL003'
        w.selected['battle_skill']=key; w.navigate('던전','전투')
        self.assertNotIn(key,self.combo_values('스킬 행동','선택 스킬'))
        e.p.update(level=5,skill_points=1); e.execute('upgrade_skill',key=key)
        e.execute('enter'); e.start_combat(); e.p['mp']=0
        w.selected['battle_skill']=key; w.refresh()
        self.assertIn(key,self.combo_values('스킬 행동','선택 스킬'))
        self.assertTrue(any('MP' in w.groups['스킬 행동'].child(i).text(1) for i in range(w.groups['스킬 행동'].childCount())))

    def test_phase2_skill_use_button_and_priority(self):
        w=self.w; e=w.engine; e.p.update(level=20,skill_points=1)
        e.execute('upgrade_skill',key='phase2.skill.SKL003'); e.execute('enter'); e.start_combat()
        e.s['skill_cooldowns']['phase2.skill.SKL003']=1; w.selected['battle_skill']='phase2.skill.SKL003'
        w.navigate('던전','전투'); app.processEvents()
        self.assertTrue(any('재사용 대기 1행동' in w.groups['스킬 행동'].child(i).text(1) for i in range(w.groups['스킬 행동'].childCount())))
        w.selected['skill_액티브']='phase2.skill.SKL003'; w.navigate('스킬','액티브'); app.processEvents()
        group=w.groups['전투 설정']; combo=w.tree.itemWidget(group.child(1),1)
        self.assertEqual(combo.count(),9)

    def test_auto_policy_controls_and_preview_are_read_only(self):
        w=self.w; e=w.engine; e.execute('enter'); e.start_combat()
        before=copy.deepcopy(e.s); rng=e.rng.getstate()
        for size in ((268,861),(250,400)):
            w.resize(*size); w.navigate('설정','게임 설정'); w.refresh()
            app.processEvents(); app.processEvents()
            self.assertEqual(self.combo_values('자동 전투','회복 정책'),['potion_first','skill_first','efficient'])
            self.assertEqual(w.tree.horizontalScrollBar().maximum(),0)
            w.navigate('던전','전투'); app.processEvents()
            self.assertIn('자동 행동',w.groups)
        self.assertEqual(before,e.s); self.assertEqual(rng,e.rng.getstate())
        w.navigate('설정','게임 설정')
        group=w.groups['자동 전투']
        row=next(group.child(i) for i in range(group.childCount()) if group.child(i).text(0)=='회복 정책')
        w.tree.itemWidget(row,1).setCurrentIndex(2); app.processEvents(); app.processEvents()
        self.assertEqual(e.s['settings']['recovery_policy'],'efficient')

if __name__=='__main__': unittest.main()
