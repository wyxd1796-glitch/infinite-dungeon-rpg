"""Rebuild the editable initial content set. Not required to run the game."""
import json
from pathlib import Path
p=Path(__file__).parent/'content/base'
def put(name,obj):
    (p/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
put('balance',dict(initial={'hp':100,'mp':30,'atk':15,'defense':5,'gold':200},stats={'str':10,'dex':5,'vit':10,'int':5,'luk':5},encounters={'normal':60,'event':20,'chest':10,'rest':5,'elite':5},rarities={'일반':60,'고급':25,'희귀':10,'영웅':4,'전설':1},luck_weight=.01,enhance_gold=20,rest_hp=5,rest_mp=3,storage_cost=1000,death_hp_fraction=.3,initial_potions=3,boss_stones=3))
mon=[]
for i,n,h,a,d,e,abilities in [('slime','슬라임',50,8,2,0,[]),('goblin','고블린',40,9,2,.08,[]),('skeleton','해골 병사',45,9,6,0,[]),('wolf','늑대',42,12,2,.03,[]),('bat','박쥐',30,7,1,.15,[]),('orc','오크',70,10,3,0,[]),('ghost','망령',40,9,2,.05,[{'type':'drain_mp','chance':.2,'value':4}]),('golem','골렘',65,8,9,0,[])]:
    mon.append(dict(id='base.monster.'+i,name=n,hp=h,atk=a,defense=d,evasion=e,accuracy=.95,min_floor=1,weight=1,abilities=abilities))
put('monsters',mon)
put('prefixes',[dict(id='base.prefix.'+i,name=n,stats=s,exp=x) for i,n,s,x in [('feral','흉포한',{'atk':1.2},1),('solid','견고한',{'defense':1.3},1),('giant','거대한',{'hp':1.4},1),('agile','민첩한',{'evasion':.1},1),('blessed','축복받은',{},1.3),('cursed','저주받은',{'atk':1.25,'defense':.8},1)]])
put('bosses',[dict(id='base.boss.'+str(i),name=n,monster_id=mon[i]['id'],ability={'type':t,'chance':1,'value':v,'interval':3}) for i,(n,t,v) in enumerate([('슬라임 군주','heal',.08),('고블린 왕','heavy',1.5),('해골 장군','poison',3),('핏빛 늑대','heavy',1.6),('밤의 날개','drain_mp',6),('오크 족장','heavy',1.5),('심연의 망령','drain_mp',8),('고대 수호자','heal',.1)])])
put('equipment',[dict(id='base.equipment.'+str(i),name=n,slot=s,stats=b) for i,(s,n,b) in enumerate([('무기','장검',{'atk':[3,1.5]}),('투구','투구',{'hp':[5,2],'defense':[1,.5]}),('갑옷','갑옷',{'defense':[2,1]}),('장갑','장갑',{'atk':[1,.5],'crit':[.005,.001]}),('신발','장화',{'evasion':[.01,.001]}),('반지','반지',{'luk':[1,.2],'crit':[.005,.001]}),('목걸이','목걸이',{'hp':[5,3],'mp':[2,1]})])])
put('affixes',[dict(id='base.affix.'+s,stat=s,name=n,base=b,per_level=v) for s,n,b,v in [('str','힘',1,.2),('dex','민첩',1,.2),('vit','체력',1,.2),('int','지능',1,.2),('luk','행운',1,.2),('crit','치명타율',.005,.001),('evasion','회피율',.005,.001)]])
put('items',[dict(id='base.item.'+i,name=n,category=c,price=price,sell_price=price//2,effects=e) for i,n,c,price,e in [('hp','HP 물약','소비품',30,[{'type':'heal_hp','value':50}]),('mp','MP 물약','소비품',40,[{'type':'heal_mp','value':30}]),('stone','강화석','재료',40,[])]])
put('skills',[dict(id='base.skill.'+i,name=n,kind=k,mp=m,max_level=5,effects=e) for i,n,k,m,e in [('strike','강타','active',8,[{'type':'damage','value':1.8,'growth':.1,'hits':1}]),('heal','회복','active',12,[{'type':'heal_hp','value':.25,'growth':.05,'fraction':True}]),('slash','연속 베기','active',15,[{'type':'damage','value':.8,'growth':.05,'hits':2}]),('weapon','무기 숙련','passive',0,[{'type':'modify_stat','stat':'atk','value':.03}]),('wall','철벽','passive',0,[{'type':'modify_stat','stat':'defense','value':.03}])]])
def fx(t,v=0,**kw): return dict(type=t,value=v,**kw)
def opt(label,effects,fail=None,cost=0):
    return dict(label=label,cost=cost,outcomes=[dict(weight=70 if fail else 100,effects=effects)]+([dict(weight=30,effects=fail)] if fail else []))
events=[
('chest','버려진 상자','먼지 속에서 오래된 상자를 발견했다.',[opt('상자를 연다',[fx('grant_gold',35)],[fx('hurt',12)]),opt('지나간다',[])]),
('altar','수상한 제단','희미한 빛이 제물을 요구한다.',[opt('기도한다',[fx('hurt',10),fx('add_status',.2,stat='atk',turns=5)],[fx('hurt',15)]),opt('떠난다',[])]),
('merchant','길 잃은 상인','상인이 물약과 장비를 내민다.',[opt('HP 물약 구매',[fx('grant_item',1,item_id='base.item.hp')],cost=25),opt('장비 구매',[fx('equipment')],cost=70),opt('떠난다',[])]),
('well','오래된 우물','수상한 물이 흐른다.',[opt('물을 마신다',[fx('heal_hp',35)],[fx('add_status',3,stat='poison',turns=3)]),opt('우물을 조사한다',[fx('grant_item',1,item_id='base.item.hp')]),opt('지나간다',[])]),
('passage','붕괴한 통로','돌무더기가 길을 막고 있다.',[opt('우회한다',[]),opt('돌파한다',[fx('grant_exp',35)],[fx('hurt',15)])]),
('treasure','숨겨진 보물','바위 틈에 보물이 빛난다.',[opt('골드를 챙긴다',[fx('grant_gold',50)]),opt('장비를 챙긴다',[fx('equipment')])]),
('stone','고대 비석','고대의 지식이 새겨져 있다.',[opt('해독한다',[fx('grant_exp',45)]),opt('명상한다',[fx('heal_mp',20)])]),
('door','수상한 문','문 너머에서 소리가 들린다.',[opt('문을 연다',[fx('grant_gold',50)],[fx('start_combat')]),opt('떠난다',[])]),
('adventurer','부상당한 모험가','모험가가 치료비를 부탁한다.',[opt('돕는다',[fx('equipment')],[fx('grant_exp',20)],cost=20),opt('떠난다',[])]),
('statue','저주받은 조각상','낯선 힘이 감돌고 있다.',[opt('손을 댄다',[fx('add_status',.25,stat='atk',turns=5)],[fx('add_status',-.2,stat='atk',turns=5)]),opt('떠난다',[])])]
put('events',[dict(id='base.event.'+i,title=n,description=d,min_floor=1,weight=1,options=o) for i,n,d,o in events])
put('achievements',[dict(id='base.achievement.'+str(i),name=n,metric=m,target=t,reward={'gold':g}) for i,(n,m,t,g) in enumerate([('첫걸음','highest',10,500),('숙련 탐험가','highest',50,2000),('심연의 도전자','highest',100,5000),('학살자','wins',1000,5000),('수집가','legendary',10,3000),('불굴의 의지','deaths',100,1000),('전설의 모험가','highest',500,20000)])])
put('manifest',dict(pack_id='base',version='1.0.0',schema_version=1,dependencies=[],enabled=True,content_files=[x.name for x in p.glob('*.json') if x.stem not in ('manifest','balance')]))
balance=json.loads((p/'balance.json').read_text(encoding='utf-8'))
balance.update(initial_mp_potions=1,critical_cap=.75,evasion_cap=.75,chest_equipment_chance=.5,chest_gold_base=20,chest_gold_per_floor=5,shop_equipment_base=70,shop_equipment_per_floor=10,equipment_sell_per_level=10,equipment_sell_per_enhance=5,enhance_stone_group=3,auto_turn_limit=500,full_bag_equipment='sell',active_start_level=1,passive_start_level=1)
put('balance',balance)
