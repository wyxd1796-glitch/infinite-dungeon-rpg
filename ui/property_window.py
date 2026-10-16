import math
import json
import time
from pathlib import Path
from PySide6.QtCore import Qt, QSize, QSettings, QTimer, QPoint, QRect, QEvent
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QPixmap, QIcon, QPolygon, QFontMetrics
from PySide6.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QToolButton,QComboBox,QTreeWidget,QTreeWidgetItem,QStyledItemDelegate,QSpinBox,QLineEdit,QMessageBox,QHeaderView)
from core.game_engine import GameEngine, RuleError, SLOTS, STAT_NAMES
from core.save_manager import SaveManager
from core.catalogue import PERCENT_STATS

def stat_value(key,value):
    return f"{value*100:g}%p" if key in PERCENT_STATS else f"{value:g}"

SCREENS={'캐릭터':['정보','능력치','성장'],'던전':['탐험','전투','이벤트'],'장비':['착용 장비','장비 상세'],'가방':['장비','소비품','재료'],'스킬':['액티브','패시브'],'거점':['휴식','상점','강화','보관함'],'기록':['전투 통계','탐험 기록','업적'],'설정':['게임 설정','저장 관리']}
ROLE=Qt.ItemDataRole.UserRole
WRAPPED_ROLE=ROLE+1
STYLE='''
QWidget { background:#424C58; color:#E2E7EB; font-family:"Malgun Gothic"; font-size:12px; }
QWidget#window { border:1px solid #313841; }
QWidget#title, QWidget#title QLabel, QWidget#title QToolButton {background:#515C69; border:0;}
QWidget#title QToolButton#pin:checked {background:#376D91;}
QToolButton {border:0; border-radius:0; padding:0;}
QToolButton:hover {background:#66717E;}
QComboBox {border:1px solid #515D66; border-radius:0; padding:1px 3px; min-height:19px;}
QComboBox::drop-down {width:16px; border:0;}
QComboBox QAbstractItemView {background:#424C58; border:1px solid #79848F; selection-background-color:#5B6774;}
QTreeWidget {border:0; outline:0; background:#424C58;}
QTreeWidget::item {border:0; padding:0;}
QTreeWidget::item:selected {background:#505E6B;}
QScrollBar:vertical {background:#3A3F45; width:12px; margin:0;}
QScrollBar::handle:vertical {background:#64707D; min-height:22px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {height:0;}
QSpinBox {border:0; padding:0 3px; selection-background-color:#657381;}
QMessageBox QPushButton {background:#515C69; border:1px solid #79848F; padding:4px 12px;}
'''

def small_icon(kind,color='#E2E7EB'):
    """Paint crisp, font-independent CAD-size navigation icons."""
    pixmap=QPixmap(32,32); pixmap.setDevicePixelRatio(2); pixmap.fill(Qt.transparent)
    painter=QPainter(pixmap); painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(QColor(color),1.2)); painter.setBrush(Qt.NoBrush)
    if kind=='record':
        painter.drawRect(3,2,10,12)
        for y in (5,8,11): painter.drawLine(5,y,11,y)
    elif kind=='settings':
        painter.drawEllipse(4,4,8,8); painter.drawEllipse(6,6,4,4)
        for angle in range(0,360,45):
            painter.save(); painter.translate(8,8); painter.rotate(angle); painter.drawLine(0,-5,0,-7); painter.restore()
    elif kind=='home':
        painter.drawPolyline(QPolygon([QPoint(1,7),QPoint(8,1),QPoint(15,7)]))
        painter.drawPolyline(QPolygon([QPoint(3,6),QPoint(3,14),QPoint(13,14),QPoint(13,6)])); painter.drawRect(6,9,4,5)
    elif kind=='pin':
        painter.setBrush(QColor(color))
        painter.drawPolygon(QPolygon([QPoint(5,2),QPoint(11,2),QPoint(10,4),QPoint(10,7),QPoint(12,9),QPoint(4,9),QPoint(6,7),QPoint(6,4)]))
        painter.drawLine(8,9,8,14)
    painter.end(); return QIcon(pixmap)

class Selector(QComboBox):
    def paintEvent(self,event):
        super().paintEvent(event)
        painter=QPainter(self); painter.setPen(Qt.NoPen); painter.setBrush(QColor('#E2E7EB'))
        from PySide6.QtGui import QPolygon
        x=self.width()-11; y=self.height()//2
        painter.drawPolygon(QPolygon([QPoint(x-4,y-2),QPoint(x+4,y-2),QPoint(x,y+2)]))
    def showPopup(self):
        super().showPopup()
        popup=self.view().window()
        popup.move(self.mapToGlobal(QPoint(0,self.height())))

class Delegate(QStyledItemDelegate):
    def sizeHint(self,option,index):
        if index.data(WRAPPED_ROLE):
            width=max(40,self.parent().viewport().width()-self.parent().indentation()-10)
            height=QFontMetrics(option.font).boundingRect(QRect(0,0,width,100000),Qt.TextWordWrap,str(index.data())).height()
            return QSize(80,max(25,height+12))
        return QSize(80,26 if not index.parent().isValid() else 25)
    def paint(self,painter,option,index):
        if index.data(WRAPPED_ROLE):
            painter.save(); painter.fillRect(option.rect,QColor('#424C58')); painter.setFont(option.font); painter.setPen(QColor('#E2E7EB'))
            painter.drawText(option.rect.adjusted(5,6,-5,-6),Qt.AlignLeft|Qt.AlignTop|Qt.TextWordWrap,str(index.data()))
            painter.setPen(QColor('#515D66')); painter.drawRect(option.rect.adjusted(0,0,-1,-1)); painter.restore()
        elif not index.parent().isValid():
            painter.fillRect(option.rect,QColor('#3A3F45'))
            painter.setPen(QColor('#E2E7EB'))
            painter.drawText(option.rect.adjusted(5,0,-20,0),Qt.AlignVCenter|Qt.AlignLeft,index.data())
            item=self.parent().itemFromIndex(index)
            painter.drawText(option.rect.adjusted(0,0,-6,0),Qt.AlignVCenter|Qt.AlignRight,'▾' if item.isExpanded() else '▸')
        else:
            super().paint(painter,option,index)
            painter.setPen(QColor('#515D66')); painter.drawRect(option.rect.adjusted(0,0,-1,-1))

class Title(QWidget):
    def __init__(self,window):
        super().__init__(); self.owner=window; self.setObjectName('title'); self.setAttribute(Qt.WA_StyledBackground); self.setFixedHeight(22)
        layout=QHBoxLayout(self); layout.setContentsMargins(7,0,0,0); layout.setSpacing(0)
        label=QLabel('특성'); label.setAttribute(Qt.WA_TransparentForMouseEvents); layout.addWidget(label); layout.addStretch()
        for text,tip,handler in [('−','최소화',window.showMinimized),('·','항상 위',window.toggle_pin),('×','닫기',window.close)]:
            button=QToolButton(); button.setText(text); button.setToolTip(tip); button.setFixedSize(22,22); button.clicked.connect(handler); layout.addWidget(button)
            if text=='·':
                window.pin_button=button; button.setText(''); button.setObjectName('pin'); button.setCheckable(True); button.setIconSize(QSize(16,16)); button.setAccessibleName('항상 위')
    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton: self.owner.windowHandle().startSystemMove()

class PropertyTree(QTreeWidget):
    def viewportEvent(self,event):
        result=super().viewportEvent(event)
        if event.type()==QEvent.Resize:
            QTimer.singleShot(0,self.relayout_viewport)
        return result
    def relayout_viewport(self):
        owner=self.window()
        if hasattr(owner,'tree'): owner.columns()
        self.doItemsLayout()
    def mousePressEvent(self,event):
        x=event.position().x()
        if event.button()==Qt.LeftButton and abs(x-self.columnWidth(0))<4:
            self.resizing=True; return
        self.resizing=False
        super().mousePressEvent(event)
    def mouseMoveEvent(self,event):
        if getattr(self,'resizing',False):
            owner=self.window(); owner.ratio=max(.25,min(.8,(event.position().x()-16)/max(1,self.viewport().width()-16))); owner.columns(); return
        super().mouseMoveEvent(event)
    def mouseReleaseEvent(self,event):
        self.resizing=False; super().mouseReleaseEvent(event)

class PropertyWindow(QWidget):
    def __init__(self,root,save_dir=None,settings_path=None):
        super().__init__(); self.root=Path(root); self.setObjectName('window'); self.setWindowTitle('INFINITE · 무한 던전 RPG')
        self.setWindowFlags(Qt.Window|Qt.FramelessWindowHint); self.setMinimumSize(250,400); self.resize(268,861); self.setMouseTracking(True)
        self.store=SaveManager(save_dir or self.root/'saves')
        self.settings=QSettings(str(settings_path or self.store.directory/'ui.ini'),QSettings.IniFormat)
        self.slot=int(self.settings.value('active_slot',1)); self.target_slot=self.slot
        self.engine=GameEngine(self.root/'content'); self.start_notice=''; self.prevent_autosave=False
        if self.store.path(self.slot).exists():
            try: self.engine=GameEngine(self.root/'content',self.store.load(self.slot)); self.start_notice=self.store.notice
            except (ValueError,KeyError,TypeError,OSError) as exc: self.start_notice=str(exc)+' · 새 상태는 기존 슬롯에 자동 저장하지 않습니다.'; self.prevent_autosave=True
        self.selected={}; self.busy=False; self.groups={}; self.actions={}; self.view_state={}; self.screen_key=''; self.last_sub={}
        self.ratio=float(self.settings.value('column_ratio',127/223)); self.pinned=self.settings.value('always_on_top','false')=='true'
        for key in ('view_state','last_sub','selected'):
            try: setattr(self,key,json.loads(self.settings.value(key,'{}')))
            except (ValueError,TypeError): pass
        self.session_time=time.monotonic()
        layout=QVBoxLayout(self); layout.setContentsMargins(1,0,1,1); layout.setSpacing(0); layout.addWidget(Title(self))
        body=QWidget(); body_layout=QVBoxLayout(body); body_layout.setContentsMargins(6,6,20,0); body_layout.setSpacing(2)
        self.main_selector=Selector(); self.main_selector.addItems(list(SCREENS)); self.main_selector.setFixedHeight(23)
        self.sub_selector=Selector(); self.sub_selector.setFixedHeight(23)
        selector_row=QHBoxLayout(); selector_row.setContentsMargins(0,0,0,0); selector_row.setSpacing(1)
        self.main_selector.setMinimumWidth(0); selector_row.addWidget(self.main_selector,1)
        self.shortcut_buttons={}
        for icon,tip,main,sub in [('record','기록','기록','전투 통계'),('settings','설정','설정','게임 설정'),('home','거점','거점','휴식')]:
            button=QToolButton(); button.setIcon(small_icon(icon)); button.setIconSize(QSize(16,16)); button.setFixedSize(20,23); button.setToolTip(tip); button.setAccessibleName(tip)
            button.clicked.connect(lambda checked=False,m=main,s=sub:self.navigate(m,s)); selector_row.addWidget(button); self.shortcut_buttons[icon]=button
        body_layout.addLayout(selector_row); body_layout.addWidget(self.sub_selector)
        self.tree=PropertyTree(); self.tree.setColumnCount(2); self.tree.setHeaderHidden(True); self.tree.setIndentation(16); self.tree.setRootIsDecorated(False)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff); self.tree.setVerticalScrollMode(QTreeWidget.ScrollPerPixel); self.tree.setTextElideMode(Qt.ElideRight); self.tree.setItemDelegate(Delegate(self.tree))
        self.tree.header().setStretchLastSection(False); self.tree.header().setSectionResizeMode(QHeaderView.Fixed)
        self.tree.itemClicked.connect(self.clicked); self.tree.setContextMenuPolicy(Qt.CustomContextMenu); self.tree.customContextMenuRequested.connect(self.full_text)
        body_layout.addWidget(self.tree,1); layout.addWidget(body,1)
        self.main_selector.currentTextChanged.connect(self.main_changed); self.sub_selector.currentTextChanged.connect(self.sub_changed)
        self.restore_geometry(); self.apply_style()
        QApplication.instance().installEventFilter(self)
        main=self.settings.value('main','던전')
        if main not in SCREENS: main='던전'
        self.main_selector.setCurrentText(main); self.main_changed(main)
        if self.engine.s.get('event_result'): self.navigate('던전','이벤트')
        self.set_pin(self.pinned)
        if self.start_notice: QTimer.singleShot(0,lambda:QMessageBox.warning(self,'저장 안내',self.start_notice))
        if self.engine.content.errors: QTimer.singleShot(0,lambda:QMessageBox.warning(self,'콘텐츠 안내','\n'.join(self.engine.content.errors)))

    def apply_style(self): self.setStyleSheet(STYLE.replace('font-size:12px',f"font-size:{self.engine.s['settings']['font_size']}px"))
    def restore_geometry(self):
        self.resize(max(250,int(self.settings.value('width',268))),max(400,int(self.settings.value('height',861))))
        x=int(self.settings.value('x',120)); y=int(self.settings.value('y',100)); rect=QRect(x,y,self.width(),self.height())
        screens=QApplication.screens(); available=next((sc.availableGeometry() for sc in screens if sc.availableGeometry().contains(rect)),None)
        if available is None:
            available=QApplication.primaryScreen().availableGeometry(); self.resize(min(self.width(),available.width()),min(self.height(),available.height())); x=max(available.left(),min(x,available.right()-self.width()+1)); y=max(available.top(),min(y,available.bottom()-self.height()+1))
        self.move(x,y)
    def set_pin(self,value):
        self.pinned=value; self.setWindowFlag(Qt.WindowStaysOnTopHint,value); self.pin_button.setChecked(value)
        self.pin_button.setIcon(small_icon('pin','#FFD782' if value else '#E2E7EB')); self.pin_button.setToolTip('항상 위: '+('ON · 켜짐' if value else 'OFF · 꺼짐'))
        self.settings.setValue('always_on_top','true' if value else 'false')
    def toggle_pin(self): self.set_pin(not self.pinned); self.show()
    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            pos=event.position(); edges=Qt.Edges()
            if pos.x()<6: edges|=Qt.LeftEdge
            if pos.x()>self.width()-7: edges|=Qt.RightEdge
            if pos.y()<5: edges|=Qt.TopEdge
            if pos.y()>self.height()-7: edges|=Qt.BottomEdge
            if edges: self.windowHandle().startSystemResize(edges)
    def eventFilter(self,watched,event):
        if event.type()==QEvent.MouseButtonPress and event.button()==Qt.LeftButton and isinstance(watched,QWidget) and watched.window()==self:
            pos=self.mapFromGlobal(event.globalPosition().toPoint()); edges=Qt.Edges()
            if pos.x()<4: edges|=Qt.LeftEdge
            if pos.x()>=self.width()-4: edges|=Qt.RightEdge
            if pos.y()<3: edges|=Qt.TopEdge
            if pos.y()>=self.height()-4: edges|=Qt.BottomEdge
            if edges and self.windowHandle(): return self.windowHandle().startSystemResize(edges)
        return super().eventFilter(watched,event)
    def resizeEvent(self,event):
        super().resizeEvent(event)
        if hasattr(self,'tree'): self.columns()
    def columns(self):
        width=self.tree.viewport().width(); first=16+int((width-16)*self.ratio)
        self.tree.setColumnWidth(0,first); self.tree.setColumnWidth(1,max(30,width-first))
    def capture_view(self):
        if self.screen_key:
            collapsed=[self.tree.topLevelItem(i).text(0) for i in range(self.tree.topLevelItemCount()) if not self.tree.topLevelItem(i).isExpanded()]
            self.view_state[self.screen_key]={'collapsed':collapsed,'scroll':self.tree.verticalScrollBar().value()}
    def main_changed(self,main):
        self.capture_view(); self.sub_selector.blockSignals(True); self.sub_selector.clear(); self.sub_selector.addItems(SCREENS[main]); self.sub_selector.setCurrentText(self.last_sub.get(main,SCREENS[main][0])); self.sub_selector.blockSignals(False); self.sub_changed(self.sub_selector.currentText())
    def sub_changed(self,sub):
        self.capture_view(); self.last_sub[self.main_selector.currentText()]=sub; self.screen_key=self.main_selector.currentText()+'/'+sub; self.render()
    def navigate(self,main,sub):
        if self.main_selector.currentText()!=main: self.main_selector.setCurrentText(main)
        self.sub_selector.setCurrentText(sub)
    def group(self,name):
        if name not in self.groups:
            item=QTreeWidgetItem(self.tree,[name]); item.setFirstColumnSpanned(True); item.setFlags(Qt.ItemIsEnabled); self.groups[name]=item; item.setExpanded(True)
        return self.groups[name]
    def row(self,group,name,value,action=None,enabled=True,tip=None):
        item=QTreeWidgetItem(self.group(group),[name,str(value)]); item.setToolTip(0,tip or name); item.setToolTip(1,tip or str(value)); item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        if action:
            item.setData(1,ROLE,action if enabled else None)
            item.setForeground(1,QColor('#E2E7EB' if enabled else '#8C99A6'))
            item.setToolTip(1,tip or (str(value) if enabled else '현재 상태 또는 자원 조건에서 사용할 수 없습니다.'))
        return item
    def description(self,group,label,text):
        self.row(group,label,'')
        item=QTreeWidgetItem(self.group(group),[text,'']); item.setFirstColumnSpanned(True); item.setData(0,WRAPPED_ROLE,True)
        item.setToolTip(0,text); item.setToolTip(1,text); item.setFlags(Qt.ItemIsEnabled)
        return item
    def choice(self,group,name,key,options,default=None,on_change=None):
        options=list(options); item=self.row(group,name,''); combo=Selector(); combo.setFixedHeight(24)
        for value,label in options: combo.addItem(str(label),value)
        current=self.selected.get(key,default if default is not None else (options[0][0] if options else None))
        index=combo.findData(current); combo.setCurrentIndex(max(0,index))
        self.selected[key]=combo.currentData(); self.tree.setItemWidget(item,1,combo)
        def change(index):
            self.selected[key]=combo.itemData(index)
            if on_change: on_change(combo.itemData(index))
            QTimer.singleShot(0,self.refresh)
        combo.currentIndexChanged.connect(change); return self.selected[key]
    def search(self,group,key):
        item=self.row(group,'이름 검색',''); field=QLineEdit(str(self.selected.get(key,''))); field.setPlaceholderText('입력 후 Enter'); field.setFixedHeight(24)
        self.tree.setItemWidget(item,1,field)
        def changed():
            self.selected[key]=field.text().strip(); QTimer.singleShot(0,self.refresh)
        field.returnPressed.connect(changed)
        return str(self.selected.get(key,'')).casefold()
    def pending(self,free):
        rows=self.engine.s['pending_loot']; self.row('획득 대기','대기 수',len(rows))
        def label(row):
            if row['kind']=='equipment': return self.engine.item_name(row['equipment'])
            return self.engine.content.by_id.get(row['item_id'],{}).get('name',row['item_id'])+f" ×{row['quantity']}"
        key=self.choice('획득 대기','대기 아이템','pending',[(r['pending_id'],label(r)) for r in rows])
        if key: self.description('획득 대기','선택 내용',label(next(r for r in rows if r['pending_id']==key)))
        self.act('획득 대기','받기','받기','claim_loot',free and bool(key),key=key)
        self.act('획득 대기','버리기','버리기','discard_loot',free and bool(key),key=key)
    def number(self,group,name,key,maximum=999):
        item=self.row(group,name,''); spin=QSpinBox(); spin.setRange(1,max(1,maximum)); spin.setValue(int(self.selected.get(key,1))); spin.setFixedHeight(24); spin.setKeyboardTracking(False); self.tree.setItemWidget(item,1,spin)
        def change(value): self.selected[key]=value; QTimer.singleShot(0,self.refresh)
        spin.valueChanged.connect(change); return spin.value()
    def act(self,group,name,label,command,enabled=True,**kwargs):
        return self.row(group,name,label,('command',command,kwargs),enabled and (not self.engine.s.get('event_result') or command=='continue_event'))
    def link(self,group,name,label,main,sub): self.row(group,name,label,('navigate',main,sub))
    def refresh(self): self.capture_view(); self.render()
    def full_text(self,pos):
        item=self.tree.itemAt(pos)
        if item: QMessageBox.information(self,item.text(0),item.toolTip(1) or item.text(1))
    def clicked(self,item,column):
        if not item.parent(): item.setExpanded(not item.isExpanded()); return
        if column!=1 or self.busy: return
        action=item.data(1,ROLE)
        if not action: return
        kind=action[0]
        if kind=='navigate': self.navigate(action[1],action[2]); return
        if kind=='slot_detail': self.selected['gear_slot']=action[1]; self.selected['gear']=action[2]; self.navigate('장비','장비 상세'); return
        if kind=='save': self.save_action(action[1]); return
        self.run(action[1],**action[2])
    def confirm(self,text): return QMessageBox.question(self,'확인',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)==QMessageBox.Yes
    def run(self,command,**kwargs):
        if command in ('discard','discard_loot') and not self.confirm('선택한 아이템을 버리시겠습니까?'): return
        self.busy=True
        try:
            previous=self.engine.s['mode']; self.engine.execute(command,**kwargs)
            if self.engine.s['settings']['autosave'] and not self.prevent_autosave: self.store.save(self.slot,self.engine.s)
            current=self.engine.s['mode']
            if self.engine.s.get('event_result'):
                self.navigate('던전','이벤트')
            elif current!=previous or command in ('enter','next','continue_event'):
                destination={'base':('거점','휴식'),'explore':('던전','탐험'),'combat':('던전','전투'),'event':('던전','이벤트')}[current]
                self.navigate(*destination)
            self.apply_style(); self.refresh()
            if command=='event': QTimer.singleShot(0,lambda:self.tree.scrollToItem(self.groups['이벤트 결과']) if '이벤트 결과' in self.groups else None)
        except (RuleError,ValueError,KeyError,OSError) as exc: QMessageBox.warning(self,'실행 안내',str(exc))
        finally:
            # Keep the click lock through a double-click sequence.
            QTimer.singleShot(QApplication.doubleClickInterval(),lambda:setattr(self,'busy',False))
    def save_action(self,action):
        target=int(self.selected.get('save_slot',self.slot)); path=self.store.path(target)
        try:
            if action=='save':
                if path.exists() and not self.confirm(f'{target}번 슬롯을 현재 진행으로 덮어쓰시겠습니까?'): return
                self.store.save(target,self.engine.s); self.slot=target; self.prevent_autosave=False
            elif action=='load':
                if not self.confirm('현재 진행을 선택한 슬롯의 저장 상태로 바꾸시겠습니까?'): return
                state=self.store.load(target); self.engine=GameEngine(self.root/'content',state); self.slot=target; self.prevent_autosave=False
                if self.engine.s.get('event_result'): self.navigate('던전','이벤트')
                if self.store.notice: QMessageBox.information(self,'복구 안내',self.store.notice)
            elif action=='new':
                if not self.confirm(f'{target}번 슬롯에서 새 게임을 시작하시겠습니까? 기존 진행은 백업됩니다.'): return
                default=self.engine.s['settings']['default_screen']; self.engine=GameEngine(self.root/'content'); self.slot=target; self.store.save(target,self.engine.s); self.prevent_autosave=False; self.navigate(*default.split('/'))
            elif action=='delete':
                if not self.confirm(f'{target}번 슬롯을 삭제하시겠습니까?'): return
                self.store.delete(target)
                if target==self.slot: self.prevent_autosave=True
            self.settings.setValue('active_slot',self.slot); self.apply_style(); self.refresh()
        except (ValueError,KeyError,OSError) as exc: QMessageBox.warning(self,'저장 오류',str(exc))
    def closeEvent(self,event):
        self.capture_view(); settings=self.settings
        rect=self.normalGeometry() if self.isMinimized() else self.geometry()
        for key,value in {'x':rect.x(),'y':rect.y(),'width':rect.width(),'height':rect.height(),'column_ratio':self.ratio,'main':self.main_selector.currentText(),'active_slot':self.slot}.items(): settings.setValue(key,value)
        for key in ('view_state','last_sub','selected'): settings.setValue(key,json.dumps(getattr(self,key),ensure_ascii=False))
        settings.sync(); self.engine.s['stats']['play_seconds']+=int(time.monotonic()-self.session_time)
        try:
            if not self.prevent_autosave: self.store.save(self.slot,self.engine.s)
        except OSError as exc:
            QMessageBox.warning(self,'저장 실패',str(exc)); event.ignore(); return
        event.accept()
        QApplication.instance().removeEventFilter(self)

    def render(self):
        self.tree.clear(); self.groups={}; e=self.engine; s=e.s; p=e.p; d=e.derived(); main=self.main_selector.currentText(); sub=self.sub_selector.currentText()
        free=s['mode'] not in ('combat','event'); base=s['mode']=='base'; combat=s['mode']=='combat'
        hp=f"{p['hp']} / {d['hp']}"; mp=f"{p['mp']} / {d['mp']}"; xp=f"{p['exp']:,} / {e.need_exp():,}"; gold=f"{p['gold']:,} G"
        location='모험가 거점' if base else f"던전 {s['floor']}층"
        def status(group='캐릭터 상태'): self.row(group,'HP',hp); self.row(group,'MP',mp)
        def gear_options(ids): return [(i,e.item_name(s['inventory'][i])) for i in ids]
        def detail(item):
            self.row('기본 정보','이름',e.item_name(item)); self.row('기본 정보','등급',item['rarity']); self.row('기본 정보','장비 레벨',item['level']); self.row('기본 정보','강화 단계',f"+{item['enhance']}")
            for k,v in item['rolled_stats'].items():
                self.row('능력치','기본 '+STAT_NAMES[k],stat_value(k,v)); self.row('능력치','강화 '+STAT_NAMES[k], '+'+stat_value(k,round(v*.1*item['enhance'],6) if k in PERCENT_STATS or not item.get('catalogue') else math.floor(v*.1*item['enhance'])))
            for i,a in enumerate(item['affixes']): self.row('추가 옵션',f'옵션 {i+1}',f"{a['name']} +{stat_value(a['stat'],a['value'])}")
            if item['base_id'] not in e.content.by_id: self.row('기본 정보','콘텐츠 상태','미확인 · 원형 팩 필요')
        if main=='캐릭터':
            if sub=='정보':
                for n,v in [('이름',p['name']),('직업','전사'),('레벨',p['level']),('경험치',xp),('소지 골드',gold)]: self.row('일반',n,v)
                status('상태'); self.row('상태','현재 위치',location); self.row('상태','상태이상',e.status_label())
                self.row('성장 요약','남은 능력치',f"{p['points']} P"); self.row('성장 요약','남은 스킬 포인트',f"{p['skill_points']} P"); self.link('성장 요약','능력치 분배','상세 보기','캐릭터','성장')
            elif sub=='능력치':
                for k in p['attributes']: self.row('기본 능력치',STAT_NAMES[k],p['attributes'][k])
                for k in ('atk','defense','hp','mp','crit','evasion'): self.row('전투 능력치',STAT_NAMES[k],f'{d[k]:.1%}' if k in ('crit','evasion') else d[k])
                for k in ('atk','defense'): self.row('장비 보너스','추가 '+STAT_NAMES[k],round(sum(e.gear_stats(s['inventory'][i]).get(k,0) for i in s['equipped'].values()),2))
            else:
                for n,v in [('현재 레벨',p['level']),('경험치',xp),('능력치 포인트',p['points'])]: self.row('성장 정보',n,v)
                for k,n in STAT_NAMES.items():
                    if k in p['attributes']: self.act('능력치 투자',n+' +1','투자','invest',free and p['points']>0,key=k)
                self.row('투자 결과','최근 투자',s['last_growth'])
        elif main=='던전':
            if sub=='탐험':
                for n,v in [('던전 층',location),('최고 도달',f"{s['highest']}층"),('진행 상황',f"{s['progress']} / 3"),('현재 상황',{'base':'거점 · 입장 필요','explore':'층 완료' if e.complete() else '탐험 대기','combat':'전투 중','event':'이벤트 진행'}[s['mode']])]: self.row('현재 위치',n,v)
                self.row('현재 위치','환경',e.environment()['name']); self.row('현재 위치','층 유형',e.floor_type_name())
                for name,value in [('레벨',p['level']),('HP',hp),('MP',mp),('경험치',xp),('돈',gold)]: self.row('캐릭터 상태',name,value)
                self.act('탐험 행동','탐험 진행','실행','explore',s['mode']=='explore'); self.act('탐험 행동','다음 층 이동','이동','next',s['mode']=='explore' and e.complete()); self.act('탐험 행동','거점 귀환','귀환','return',s['mode']=='explore')
                if base: self.link('탐험 행동','던전 입장 준비','거점으로 이동','거점','휴식')
                for n,v in [('최근 결과',s['last']),('획득 골드',f"+{s['last_gold']} G"),('획득 경험치',f"+{s['last_exp']}")]: self.row('탐험 기록',n,v)
            elif sub=='전투':
                enemy=s['enemy'] or {}; self.row('전투 상태','진행 상태','전투 중' if combat else '전투 없음'); self.row('전투 상태','턴 수',s['combat_turn']); status('플레이어')
                for n,v in [('이름',enemy.get('name','없음')),('레벨',enemy.get('level','-')),('HP',f"{enemy.get('hp',0)} / {enemy.get('max_hp',0)}"),('상태이상',e.status_label('enemy'))]: self.row('적 정보',n,v)
                if enemy:
                    self.description('적 정보','행동 설명',' → '.join({'attack':'공격','defend':'방어','special':'특수공격'}.get(a,a) for a in enemy.get('pattern',[]))+f" · 다음 순서 {enemy.get('pattern_index',0)%max(1,len(enemy.get('pattern',[])))+1}"+'\n'+str(e.content.by_id.get('catalogue.v3.'+str(enemy.get('effect_id','')),{}).get('effect','특수공격 피해 150%')) )
                for n,label,cmd in [('일반 공격','공격','attack'),('강공격','공격','heavy'),('방어','방어','defend'),('도주','도주','flee')]: self.act('기본 행동',n,label,cmd,combat and not (cmd=='flee' and enemy.get('kind')=='boss'))
                key=self.choice('스킬 행동','선택 스킬','battle_skill',[(r['id'],r['name']) for r in e.content['skills'] if r['kind']=='active'])
                self.act('스킬 행동','스킬 사용','사용','skill',combat and p['mp']>=e.content.by_id[key]['mp'] and not any(st.get('effect_number')==6 for st in s['statuses']),key=key)
                key=self.choice('소비 행동','선택 물약','potion',[(r['id'],r['name']) for r in e.available_items('소비품') if 'combat' in r.get('contexts',['combat'])])
                self.act('소비 행동','물약 사용','사용','use',combat and s['items'].get(key,0)>0,key=key); self.act('자동 행동','현재 전투 자동','실행','auto',combat)
                self.row('전투 기록','최근 피해',s['last_damage']); self.row('전투 기록','최근 반격',s['last_counter']); self.link('전투 기록','전체 기록','기록 보기','기록','전투 통계')
            else:
                result=s.get('event_result'); ev=result or s['event']
                self.row('이벤트 정보','이벤트명',ev['title'] if ev else '없음'); self.description('이벤트 정보','상황 설명',ev['description'] if ev else '진행 중인 이벤트 없음')
                if result:
                    self.description('이벤트 결과','선택한 행동',result['choice'])
                    self.description('이벤트 결과','선택 결과',result['text'])
                    self.act('다음 진행','결과 확인','계속하기','continue_event')
                elif ev:
                    for i,opt in enumerate(ev['options']): self.act('이벤트 선택',f"선택지 {i+1}: {opt['label']}",'선택하기','event',p['gold']>=opt.get('cost',0) and all(e.condition(c) for c in opt.get('conditions',[])),index=i)
                else: self.row('이벤트 결과','결과','진행 중인 이벤트 없음')
        elif main=='장비':
            if sub=='착용 장비':
                for slot in SLOTS:
                    iid=s['equipped'].get(slot); self.row('장착 상태',slot,e.item_name(s['inventory'][iid]) if iid else '없음',('slot_detail',slot,iid))
                for k in ('atk','defense','hp'): self.row('장비 합계','추가 '+STAT_NAMES[k],round(sum(e.gear_stats(s['inventory'][i]).get(k,0) for i in s['equipped'].values()),2))
                self.row('장비 합계','특수 옵션 수',sum(len(s['inventory'][i]['affixes']) for i in s['equipped'].values())); self.link('장비 관리','장비 상세','상세 보기','장비','장비 상세')
            else:
                slot=self.choice('선택','장비 슬롯','gear_slot',[(v,v) for v in SLOTS]); ids=[i for i in s['bag']+list(s['equipped'].values()) if s['inventory'][i]['slot']==slot]; iid=self.choice('선택','보유 장비','gear',gear_options(ids))
                if iid:
                    item=s['inventory'][iid]; detail(item); current=s['equipped'].get(slot); old=e.gear_stats(s['inventory'][current]) if current else {}; new=e.gear_stats(item)
                    self.row('장비 비교','현재 착용 대비',', '.join(f'{STAT_NAMES[k]} {stat_value(k,v-old.get(k,0))}' for k,v in new.items()))
                self.act('장비 관리','장착','장착하기','equip',free and iid in s['bag'],key=iid); self.act('장비 관리','해제','해제하기','unequip',free and slot in s['equipped'] and e.bag_used()<30,key=slot); self.link('장비 관리','강화 화면','이동','거점','강화')
        elif main=='가방':
            if sub=='장비':
                self.row('가방 정보','사용 칸',f'{e.bag_used()} / 30'); self.row('가방 정보','장비 개수',len(s['bag']))
                sort=self.choice('아이템 선택','정렬 기준','sort',[(v,v) for v in ('등급순','레벨순','이름순')]); slot=self.choice('아이템 선택','장비 종류','filter_slot',[(v,v) for v in ['전체']+SLOTS]); ids=[i for i in s['bag'] if slot=='전체' or s['inventory'][i]['slot']==slot]
                query=self.search('아이템 선택','bag_search'); ids=[i for i in ids if query in e.item_name(s['inventory'][i]).casefold()]
                ids.sort(key=lambda i:list(e.content.balance['rarities']).index(s['inventory'][i]['rarity']) if sort=='등급순' else s['inventory'][i]['level'] if sort=='레벨순' else s['inventory'][i]['name'],reverse=sort!='이름순')
                iid=self.choice('아이템 선택','장비 목록','bag_gear',gear_options(ids))
                if iid:
                    item=s['inventory'][iid]
                    for n,v in [('이름',e.item_name(item)),('등급',item['rarity']),('레벨',item['level']),('핵심 능력치',', '.join(f'{STAT_NAMES[k]} +{stat_value(k,v)}' for k,v in e.gear_stats(item).items()))]: self.row('선택 장비',n,v)
                    self.row('관리','판매 가격',f'{e.sell_price(item)} G')
                self.act('관리','장착','장착하기','equip',free and bool(iid),key=iid); self.act('관리','판매','판매하기','sell',base and bool(iid),key=iid); self.act('관리','버리기','버리기','discard',free and bool(iid),key=iid)
            else:
                items=e.available_items(sub); self.row('보유 정보',sub+' 종류',sum(s['items'].get(r['id'],0)>0 for r in items))
                kind=self.choice('아이템 선택','종류 필터','bag_type_'+sub,[(v,v) for v in ['전체']+sorted({r.get('subtype','기존') for r in items})])
                query=self.search('아이템 선택','bag_search_'+sub); items=[r for r in items if (kind=='전체' or r.get('subtype','기존')==kind) and query in r['name'].casefold()]
                key=self.choice('아이템 선택',sub,'bag_'+sub,[(r['id'],r['name']) for r in items])
                if key:
                    item=e.content.by_id[key]; self.row('아이템 정보','보유 수량',f"{s['items'].get(key,0)}개"); self.description('아이템 정보','설명',e.shop_description(key)); self.row('아이템 정보','판매 가격',f"{item['sell_price']} G")
                    if sub=='소비품': self.act('사용','아이템 사용','사용하기','use',s['mode'] in item.get('contexts',['base','explore','combat']) and s['items'].get(key,0)>0,key=key)
                    quantity=self.number('관리','판매 수량','sell_quantity'); has=s['items'].get(key,0)>=quantity
                    self.act('관리','판매','판매하기','sell',base and has,key=key,quantity=quantity); self.act('관리','버리기','버리기','discard',free and has,key=key,quantity=quantity)
                else: self.row('아이템 정보','검색 결과','없음')
            self.pending(free)
        elif main=='스킬':
            active=sub=='액티브'; skills=[r for r in e.content['skills'] if r['kind']==('active' if active else 'passive')]; key=self.choice('스킬 선택','스킬','skill_'+sub,[(r['id'],r['name']) for r in skills]); skill=e.content.by_id[key]; level=s['skills'].get(key,0); effect=skill['effects'][0]
            self.row('스킬 정보','레벨',f'{level} / 5')
            if active:
                self.row('스킬 정보','유형','공격' if effect['type']=='damage' else '회복'); self.row('스킬 정보','소모 MP',skill['mp']); self.row('스킬 정보','피해 배율' if effect['type']=='damage' else '회복 비율',f"{effect['value']+effect.get('growth',0)*(level-1):.0%}"+(' ×2' if effect.get('hits')==2 else '')); self.row('스킬 정보','사용 가능','가능' if combat and p['mp']>=skill['mp'] else '전투 또는 MP 필요')
            else: self.row('패시브 정보','현재 효과',f"{STAT_NAMES[effect['stat']]} +{effect['value']*level:.0%}")
            self.row('스킬 성장','보유 포인트',p['skill_points']); self.row('스킬 성장','다음 레벨 효과','최대 레벨' if level>=5 else f"+{effect.get('growth',effect['value']):.0%}"); self.act('스킬 성장','스킬 강화','강화하기','upgrade_skill',free and p['skill_points']>0 and level<5,key=key)
            if active:
                cfg=s['skill_auto'].get(key,{'enabled':True,'priority':1})
                self.selected['auto_'+key]=cfg['enabled']; self.selected['priority_'+key]=cfg['priority']
                self.choice('전투 설정','자동 사용','auto_'+key,[(True,'켜짐'),(False,'꺼짐')],cfg['enabled'],lambda v:self.change_skill_auto(key,'enabled',v)); self.choice('전투 설정','우선순위','priority_'+key,[(i,str(i)) for i in range(1,4)],cfg['priority'],lambda v:self.change_skill_auto(key,'priority',v))
        elif main=='거점':
            if sub=='휴식':
                self.row('거점 정보','현재 위치',location); self.row('거점 정보','보유 골드',gold); status()
                for k,label in [('hp','HP'),('mp','MP'),('both','HP/MP')]:
                    keys=['hp','mp'] if k=='both' else [k]; needed=[v for v in keys if p[v]<d[v]]; cost=sum(e.content.balance['rest_'+v]*p['level'] for v in needed)
                    self.act('회복',label+' 전체 회복',f'{cost} G','rest',base and bool(needed) and p['gold']>=cost,key=k)
                floor=self.choice('탐험 준비','입장 층수','entry_floor',[(i,f'{i}층') for i in range(1,s['highest']+1)])
                self.act('탐험 준비','던전 입장','입장하기','enter',base,floor=floor)
            elif sub=='상점':
                self.row('상점 정보','보유 골드',gold); kind=self.choice('상품 선택','상품 종류','shop_kind',[(k,k) for k in ('소비품','재료','장비')])
                items=[r for r in e.shop_stock() if ('slot' in r if kind=='장비' else r.get('category')==kind)]
                # Product stays immediately below kind; filters are separate rows.
                query=str(self.selected.get('shop_search','')).casefold(); filter_kind=self.selected.get('shop_filter','전체')
                valid_filters=['전체']+sorted({r.get('slot',r.get('subtype','기존')) for r in items})
                if filter_kind not in valid_filters: filter_kind='전체'; self.selected['shop_filter']='전체'
                items=[r for r in items if query in r['name'].casefold() and (filter_kind=='전체' or r.get('slot',r.get('subtype','기존'))==filter_kind)]
                key=self.choice('상품 선택','상품명','shop_item',[(r['id'],r['name']) for r in items]); self.choice('상품 선택','슬롯 / 종류','shop_filter',[(v,v) for v in valid_filters]); self.search('상품 선택','shop_search')
                if key:
                    item=e.content.by_id[key]; price=e.equipment_price(key) if kind=='장비' else item['price']
                    self.row('상품 정보','단가',f'{price} G'); self.row('상품 정보','보유 수량',sum(i['base_id']==key for i in s['inventory'].values()) if kind=='장비' else s['items'].get(key,0))
                    self.description('상품 정보','상품 설명',e.shop_description(key))
                    quantity=self.number('구매','구매 수량','buy_quantity'); self.row('구매','총 구매금액',f'{quantity*price} G')
                    capacity=e.bag_used()+(quantity if kind=='장비' else int(s['items'].get(key,0)==0))<=30
                    self.act('구매','구매하기','구매','buy',base and p['gold']>=quantity*price and capacity and (kind=='장비' or s['items'].get(key,0)+quantity<=item['stack_limit']),key=key,quantity=quantity)
                else: self.row('상품 정보','검색 결과','없음')
                self.link('판매','판매 화면','가방으로 이동','가방','장비')
            elif sub=='강화':
                iid=self.choice('강화 대상','장비 선택','enhance',gear_options(s['bag']+list(s['equipped'].values())))
                materials=e.upgrade_materials(); material=self.choice('강화 재료','사용 재료','enhance_material',[(k,n) for k,n,u in materials]); units=dict((k,u) for k,n,u in materials).get(material,1); allowed=False
                if iid:
                    item=s['inventory'][iid]; cost,stones,chance=e.enhance_cost(item)
                    for n,v in [('현재 강화',f"+{item['enhance']}"),('강화 후 단계',f"+{min(15,item['enhance']+1)}"),('성공 확률',f'{chance:.0%}'),('현재 능력치',', '.join(f'{STAT_NAMES[k]} {stat_value(k,v)}' for k,v in e.gear_stats(item).items())),('성공 시 증가',', '.join(f'{STAT_NAMES[k]} +{stat_value(k,round(v*.1,6) if k in PERCENT_STATS or not item.get("catalogue") else math.floor(v*.1*(item["enhance"]+1))-math.floor(v*.1*item["enhance"]))}' for k,v in item['rolled_stats'].items()))]: self.row('강화 정보',n,v)
                    for n,v in [('필요 골드',f'{cost} G'),('필요 수량',math.ceil(stones/units)),('보유 수량',s['items'].get(material,0))]: self.row('강화 재료',n,v)
                    allowed=base and p['gold']>=cost and s['items'].get(material,0)>=math.ceil(stones/units) and item['enhance']<15
                self.act('강화 실행','강화하기','실행','enhance',allowed,key=iid,material=material); self.row('강화 결과','최근 결과',s['last_enhance'])
            else:
                cost=e.content.balance['storage_cost']*(1+(s['storage_capacity']-50)//10)
                for n,v in [('사용 공간',f"{len(s['storage'])} / {s['storage_capacity']}"),('가방 공간',f'{e.bag_used()} / 30'),('확장 비용',f'{cost} G')]: self.row('보관 정보',n,v)
                self.act('보관 정보','공간 확장','확장하기','expand',base and p['gold']>=cost); iid=self.choice('보관하기','가방 장비','deposit',gear_options(s['bag'])); self.act('보관하기','보관 실행','맡기기','deposit',base and bool(iid) and len(s['storage'])<s['storage_capacity'],key=iid); iid=self.choice('꺼내기','보관 장비','withdraw',gear_options(s['storage'])); self.act('꺼내기','꺼내기 실행','꺼내기','withdraw',base and bool(iid) and e.bag_used()<30,key=iid)
        elif main=='기록':
            if sub=='전투 통계':
                for group,k,n in [('전투 기록','battles','총 전투'),('전투 기록','wins','승리'),('전투 기록','deaths','패배'),('전투 기록','escapes','도주 성공'),('처치 기록','normal','일반 몬스터'),('처치 기록','elite','정예 몬스터'),('처치 기록','boss','보스'),('피해 기록','damage','누적 피해량'),('피해 기록','max_damage','최대 단일 피해')]: self.row(group,n,s['stats'][k])
                log_kind=self.choice('전투 로그','로그 항목','log_kind',[('combat','최근 전투'),('all','전체 행동')]); logs=s['combat_logs'] if log_kind=='combat' else s['logs']
                for i,line in enumerate(logs[-s['settings']['log_count']:]): self.row('상세 기록',str(i+1),line)
            elif sub=='탐험 기록':
                for n,v in [('현재 층',s['floor']),('최고 층',s['highest']),('총 탐험 횟수',s['stats']['explorations']),('총 귀환 횟수',s['stats']['returns'])]: self.row('탐험 기록',n,v)
                for n,k in [('누적 골드 획득','gold'),('획득 장비','equipment'),('전설 장비','legendary')]: self.row('보상 기록',n,s['stats'][k])
                self.row('기타','플레이 시작일',s['started_at'][:10]); self.row('기타','누적 플레이 시간',f"{int((s['stats']['play_seconds']+time.monotonic()-self.session_time)//60)}분")
            else:
                achievements=e.content['achievements']; self.row('업적 현황','달성 수',f"{sum(e.metric(r['metric'])>=r['target'] for r in achievements)} / {len(achievements)}")
                kind=self.choice('업적 선택','업적 종류','ach_kind',[(v,v) for v in ('전체','탐험','전투','수집')]); filtered=[r for r in achievements if kind=='전체' or (kind=='탐험' and r['metric']=='highest') or (kind=='전투' and r['metric'] in ('wins','deaths')) or (kind=='수집' and r['metric']=='legendary')]; key=self.choice('업적 선택','업적명','achievement',[(r['id'],r['name']) for r in filtered]); ach=e.content.by_id[key]; value=e.metric(ach['metric']); achieved=value>=ach['target']
                for n,v in [('달성 조건',f"{ {'highest':'최고 층','wins':'승리','deaths':'사망','legendary':'전설 장비'}[ach['metric']]} {ach['target']}"),('현재 진행',f"{value} / {ach['target']}"),('달성 여부','수령 완료' if key in s['claimed'] else '완료' if achieved else '진행 중'),('보상',f"{ach['reward'].get('gold',0)} G")]: self.row('업적 정보',n,v)
                self.act('업적 관리','보상 수령','수령하기','claim',free and achieved and key not in s['claimed'],key=key)
        elif main=='설정':
            if sub=='게임 설정':
                specs=[('일반','자동 저장','autosave',[(True,'켜짐'),(False,'꺼짐')]),('일반','게임 로그 수','log_count',[(i,f'{i}개') for i in (5,10,20,50,200)]),('인터페이스','글자 크기','font_size',[(i,f'{i}px') for i in (11,12,13)]),('인터페이스','기본 화면','default_screen',[(v,v) for v in ('던전/탐험','거점/휴식','캐릭터/정보')]),('인터페이스','카테고리 기억','remember_categories',[(True,'켜짐'),(False,'꺼짐')]),('자동 전투','HP 위험 기준','danger',[(v,f'{v:.0%}') for v in (.2,.3,.4,.5)]),('자동 전투','위험 시 중단','stop_danger',[(True,'켜짐'),(False,'꺼짐')]),('자동 전투','자동 물약','auto_potion',[(True,'켜짐'),(False,'꺼짐')]),('자동 전투','물약 사용 기준','potion_threshold',[(v,f'HP {v:.0%}') for v in (.3,.5,.7)]),('자동 전투','자동 스킬','auto_skill',[(True,'켜짐'),(False,'꺼짐')])]
                for group,name,key,options in specs:
                    self.selected['setting_'+key]=s['settings'][key]
                    self.choice(group,name,'setting_'+key,options,s['settings'][key],lambda v,k=key:self.change_setting(k,v))
                self.row('시스템','게임 버전','1.1.0'); self.row('시스템','콘텐츠 팩',', '.join(r['id'] for r in e.content.packs))
            else:
                target=self.choice('저장 정보','저장 슬롯','save_slot',[(i,str(i)) for i in (1,2,3)],self.slot); summary=None
                if self.store.path(target).exists():
                    try: summary=self.store.load(target)
                    except (ValueError,KeyError,OSError): pass
                for n,v in [('캐릭터',summary['player']['name'] if summary else '빈 슬롯 / 읽기 불가'),('캐릭터 레벨',summary['player']['level'] if summary else '-'),('최고 도달',summary['highest'] if summary else '-'),('저장 시각',summary['saved_at'] if summary else '-'),('현재 진행 슬롯',self.slot)]: self.row('저장 정보',n,v)
                for n,label,action in [('수동 저장','저장하기','save'),('불러오기','불러오기','load'),('새 게임','새로 시작','new'),('슬롯 삭제','삭제하기','delete')]: self.row('저장 행동',n,label,('save',action),action not in ('load','delete') or self.store.path(target).exists())
        if s.get('event_result') and (main,sub)!=('던전','이벤트'): self.link('진행 안내','선택 결과 확인','결과 보기','던전','이벤트')
        view=self.view_state.get(self.screen_key,{})
        if s['settings']['remember_categories']:
            for name,item in self.groups.items(): item.setExpanded(name not in view.get('collapsed',[]))
        self.columns(); self.tree.verticalScrollBar().setValue(view.get('scroll',0))
        QTimer.singleShot(0,self.columns)

    def change_setting(self,key,value):
        self.engine.execute('setting',key=key,value=value); self.apply_style()
        if not self.prevent_autosave: self.store.save(self.slot,self.engine.s)

    def change_skill_auto(self,key,field,value):
        self.engine.execute('skill_auto',key=key,field=field,value=value)
        if not self.prevent_autosave: self.store.save(self.slot,self.engine.s)
