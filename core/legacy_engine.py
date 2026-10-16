"""Turn-based engine. Every public mutation passes through execute()."""
import copy
import math
import random
import uuid
from datetime import datetime
from .content import Content

SLOTS=['무기','투구','갑옷','장갑','신발','반지','목걸이']
STAT_NAMES={'str':'힘','dex':'민첩','vit':'체력','int':'지능','luk':'행운','atk':'공격력','defense':'방어력','hp':'HP','mp':'MP','crit':'치명타율','evasion':'회피율'}

class RuleError(ValueError): pass

class GameEngine:
    def __init__(self, root, state=None, seed=None):
        self.content=Content(root)
        self.rng=random.Random(seed)
        self.s=state or self.new_state()
        # Additive defaults preserve older version-1 saves and removed-pack instances.
        def defaults(target, template):
            for key,value in template.items():
                if key not in target: target[key]=copy.deepcopy(value)
                elif key not in ('items','inventory','equipped','event_seen') and isinstance(value,dict) and isinstance(target[key],dict): defaults(target[key],value)
        defaults(self.s,self.new_state())
        if self.s.get('rng_state'):
            def tup(v): return tuple(tup(x) for x in v) if isinstance(v,list) else v
            self.rng.setstate(tup(self.s['rng_state']))

    def new_state(self):
        b=self.content.balance
        return dict(save_schema_version=1,game_version='1.0.0',active_content_packs=self.content.packs,saved_at='',
            player=dict(name='무명의 전사',level=1,exp=0,hp=b['initial']['hp'],mp=b['initial']['mp'],gold=b['initial']['gold'],points=0,skill_points=0,attributes=dict(b['stats'])),
            mode='base',floor=1,highest=1,progress=0,boss_done=False,boss_first=[],enemy=None,event=None,turn=0,combat_turn=0,
            inventory={},bag=[],equipped={},storage=[],storage_capacity=50,items={'base.item.hp':b['initial_potions'],'base.item.mp':b['initial_mp_potions'],'base.item.stone':0},
            skills={r['id']:r.get('initial_level',b['active_start_level' if r['kind']=='active' else 'passive_start_level']) for r in self.content['skills']},skill_auto={r['id']:{'enabled':r.get('auto_enabled',True),'priority':min(3,i+1)} for i,r in enumerate(self.content['skills']) if r['kind']=='active'},
            stats={k:0 for k in ('battles','wins','deaths','escapes','normal','elite','boss','damage','max_damage','explorations','returns','gold','equipment','legendary','play_seconds')},
            claimed=[],statuses=[],event_seen={},logs=['거점에서 준비한 뒤 던전에 입장하세요.'],combat_logs=[],last='모험 준비',last_damage='없음',last_counter='없음',last_gold=0,last_exp=0,last_item='없음',last_growth='없음',last_enhance='없음',
            started_at=datetime.now().astimezone().isoformat(timespec='seconds'),
            settings=dict(autosave=True,log_count=5,font_size=12,default_screen='던전/탐험',remember_categories=True,danger=.3,auto_potion=True,potion_threshold=.5,auto_skill=True,stop_danger=True))

    @property
    def p(self): return self.s['player']
    def need_exp(self): return math.floor(100*self.p['level']**1.5)
    def log(self,text):
        self.s['last']=text; self.s['logs'].append(text); self.s['logs']=self.s['logs'][-200:]
        if self.s['mode']=='combat':
            self.s['combat_logs'].append(text); self.s['combat_logs']=self.s['combat_logs'][-200:]
    def require(self,condition,message):
        if not condition: raise RuleError(message)
    def weighted(self,rows,key='weight'): return self.rng.choices(rows,weights=[r[key] for r in rows],k=1)[0]
    def eligible(self,row):
        if not (row.get('min_floor',1)<=self.s['floor'] and (row.get('max_floor') is None or self.s['floor']<=row['max_floor'])): return False
        seen=self.s.get('event_seen',{}).get(row.get('id'))
        if seen is not None and (row.get('once_per_run') or self.s['stats']['explorations']-seen<=row.get('cooldown_encounters',0)): return False
        return all(self.condition(c) for c in row.get('conditions',[]))

    def condition(self,c):
        kind=c['type']; value=c.get('value')
        if kind=='min_floor': return self.s['floor']>=value
        if kind=='max_floor': return self.s['floor']<=value
        if kind=='gold_at_least': return self.p['gold']>=value
        if kind=='hp_percent': return c.get('min',0)<=self.p['hp']/self.derived()['hp']<=c.get('max',1)
        if kind=='has_item': return self.s['items'].get(c['item_id'],0)>=c.get('count',1)
        if kind=='boss_defeated': return value in self.s['boss_first']
        if kind=='has_tag': return value in self.s.get('tags',[])
        return False
    def gear_stats(self,item):
        result={k:v*(1+.1*item['enhance']) for k,v in item['rolled_stats'].items()}
        for a in item['affixes']: result[a['stat']]=result.get(a['stat'],0)+a['value']
        return result
    def derived(self):
        a=dict(self.p['attributes']); gear={}
        for iid in self.s['equipped'].values():
            item=self.s['inventory'][iid]
            if item['base_id'] not in self.content.by_id: continue
            for k,v in self.gear_stats(item).items(): gear[k]=gear.get(k,0)+v
        for k in a: a[k]+=gear.get(k,0)
        d=dict(atk=15+2*(a['str']-10)+gear.get('atk',0),defense=5+.5*(a['vit']-10)+gear.get('defense',0),hp=100+10*(a['vit']-10)+gear.get('hp',0),mp=30+5*(a['int']-5)+gear.get('mp',0),crit=.002*a['luk']+gear.get('crit',0),evasion=.002*a['dex']+gear.get('evasion',0),**a)
        for skill in self.content['skills']:
            if skill['kind']=='passive':
                for e in skill['effects']: d[e['stat']]*=1+e['value']*self.s['skills'].get(skill['id'],0)
        for status in self.s['statuses']:
            if status['stat'] in d: d[status['stat']]*=1+status['value']
        for k in ('atk','defense','hp','mp'): d[k]=max(1,math.floor(d[k]))
        d['crit']=min(self.content.balance['critical_cap'],d['crit']); d['evasion']=min(self.content.balance['evasion_cap'],d['evasion'])
        return d
    def clamp(self):
        d=self.derived(); self.p['hp']=max(0,min(self.p['hp'],d['hp'])); self.p['mp']=max(0,min(self.p['mp'],d['mp']))
    def bag_used(self): return len(self.s['bag'])+sum(n>0 for n in self.s['items'].values())
    def complete(self): return self.s['progress']>=3 and (self.s['floor']%10!=0 or self.s['boss_done'])
    def gain_exp(self,amount):
        self.p['exp']+=amount; self.s['last_exp']=amount
        while self.p['exp']>=self.need_exp():
            self.p['exp']-=self.need_exp(); self.p['level']+=1; self.p['points']+=3
            if self.p['level']%5==0: self.p['skill_points']+=1
            d=self.derived(); self.p['hp']=d['hp']; self.p['mp']=d['mp']; self.log(f"레벨 {self.p['level']} 달성 · 능력치 +3")
    def gain_gold(self,amount):
        self.p['gold']+=amount; self.s['stats']['gold']+=amount; self.s['last_gold']=amount
    def grant_item(self,key,n):
        if self.s['items'].get(key,0)==0 and self.bag_used()>=30:
            self.log('가방이 가득 차 아이템을 받지 못했습니다.'); return False
        self.s['items'][key]=self.s['items'].get(key,0)+n
        self.s['last_item']=self.content.by_id[key]['name']; return True
    @staticmethod
    def equipment_base_stats(base,level):
        return {k:round(v[0]+v[1]*level,4) if k in ('crit','evasion') else math.floor(v[0]+v[1]*level) for k,v in base['stats'].items()}

    def shop_description(self,key):
        """Read-only preview; buying random gear still rolls only on purchase."""
        item=self.content.by_id[key]; lines=[]
        if item.get('description'): lines.append(item['description'])
        if 'slot' in item:
            low=max(1,self.s['floor']-2); high=max(1,self.s['floor']+2)
            minimum=self.equipment_base_stats(item,low); maximum=self.equipment_base_stats(item,high)
            lines.extend([f"착용 부위: {item['slot']}",f'장비 레벨: {low}~{high}', '기본 능력치 (강화 +0):'])
            for stat,value in minimum.items():
                def number(v): return f'{v*100:g}%p' if stat in ('crit','evasion') else f'{v:g}'
                span=number(value) if value==maximum[stat] else f'{number(value)}~{number(maximum[stat])}'
                lines.append(f'{STAT_NAMES[stat]} +{span}')
            lines.append('구매 시 레벨·등급·추가 옵션이 무작위로 결정됩니다. 위 수치는 기본 능력치 범위이며 추가 옵션은 별도입니다.')
        elif item.get('category')=='소비품':
            for effect in item['effects']:
                if effect['type'] in ('heal_hp','heal_mp'):
                    resource=effect['type'][5:].upper(); amount=f"최대치의 {effect['value']:.0%}" if effect.get('fraction') else f"{effect['value']:g}"
                    lines.append(f'{resource} {amount} 회복 (최대치까지).')
            lines.append('사용 시 1개 소모. 전투 중에는 1턴을 사용하며 적이 살아 있으면 반격합니다.')
        elif item.get('category')=='재료':
            lines.append('거점 → 강화에서 장비 강화에 사용합니다. 필요 수량은 강화 단계에 따라 달라집니다. 강화 실패 시에도 재료가 소모됩니다.')
        return '\n'.join(lines) or '추가 설명 없음'

    def generate_equipment(self,base_id=None):
        base=self.content.by_id[base_id] if base_id else self.rng.choice(self.content['equipment'])
        level=max(1,self.s['floor']+self.rng.randint(-2,2)); rarities=self.content.balance['rarities']
        weights=[v*(1+max(0,self.derived()['luk']-5)*self.content.balance['luck_weight'] if i>=2 else 1) for i,v in enumerate(rarities.values())]
        rarity=self.rng.choices(list(rarities),weights=weights)[0]; count=list(rarities).index(rarity)
        affixes=[dict(id=a['id'],stat=a['stat'],name=a['name'],value=(round(a['base']+level*a['per_level'],4) if a['stat'] in ('crit','evasion') else math.floor(a['base']+level*a['per_level']))) for a in self.rng.sample(self.content['affixes'],min(count,len(self.content['affixes'])))]
        return dict(instance_id=str(uuid.UUID(int=self.rng.getrandbits(128))),base_id=base['id'],name=base['name'],slot=base['slot'],level=level,rarity=rarity,enhance=0,rolled_stats=self.equipment_base_stats(base,level),affixes=affixes,origin_floor=self.s['floor'])
    def award_equipment(self):
        item=self.generate_equipment()
        if self.bag_used()>=30:
            self.gain_gold(self.sell_price(item)); self.log('가방 가득 참 · 획득 장비를 자동 환전했습니다.'); return
        self.s['inventory'][item['instance_id']]=item; self.s['bag'].append(item['instance_id']); self.s['stats']['equipment']+=1
        self.s['stats']['legendary']+=int(item['rarity']=='전설'); self.s['last_item']=self.item_name(item)
        self.log(f"획득: {self.item_name(item)}")
    def item_name(self,item): return f"{item['rarity']} {item['name']} +{item['enhance']}"
    def sell_price(self,item):
        b=self.content.balance
        return max(1,item['level']*b['equipment_sell_per_level']*(list(b['rarities']).index(item['rarity'])+1)+item['enhance']*b['equipment_sell_per_enhance'])
    def equipment_price(self): return self.content.balance['shop_equipment_base']+self.content.balance['shop_equipment_per_floor']*self.s['highest']
    def start_combat(self,kind='normal'):
        f=self.s['floor']; boss=None
        if kind=='boss':
            bosses=[b for b in self.content['bosses'] if self.eligible(b)]
            boss=bosses[(f//10-1)%len(bosses)]; base=self.content.by_id[boss['monster_id']]
        else: base=self.weighted([m for m in self.content['monsters'] if self.eligible(m)])
        e=copy.deepcopy(base); e.update(level=f,kind=kind,exp_multiplier=1)
        e['hp']=math.floor(base['hp']*(1+.12*(f-1))); e['atk']=math.floor(base['atk']*(1+.08*(f-1))); e['defense']=math.floor(base['defense']*(1+.06*(f-1)))
        if kind=='elite':
            e['hp']*=2; e['atk']=math.floor(e['atk']*1.4); prefix=self.rng.choice(self.content['prefixes']); e['name']=prefix['name']+' '+e['name']; e['exp_multiplier']=prefix['exp']
            for k,v in prefix['stats'].items(): e[k]=e.get(k,0)+v if k=='evasion' else math.floor(e[k]*v)
        if boss:
            e['hp']*=5; e['atk']=math.floor(e['atk']*1.8); e['name']=boss['name']; e['abilities'].append(boss['ability'])
        e['max_hp']=e['hp']; self.s['enemy']=e; self.s['mode']='combat'; self.s['combat_turn']=0; self.s['stats']['battles']+=1; self.s['combat_logs']=[]
        self.log(e['name']+' 등장')
    def damage(self,atk,mult,defense,crit=0):
        value=max(1,math.floor(atk*mult*self.rng.uniform(.9,1.1)-.6*defense))
        return max(1,math.floor(value*(1.5 if self.rng.random()<crit else 1)))
    def hit(self,mult=1,accuracy=.95):
        e=self.s['enemy']; d=self.derived()
        if self.rng.random()>=max(.05,accuracy-e['evasion']): self.s['last_damage']='공격 빗나감'; self.log('공격 빗나감'); return
        amount=self.damage(d['atk'],mult,e['defense'],d['crit']); e['hp']=max(0,e['hp']-amount)
        self.s['stats']['damage']+=amount; self.s['stats']['max_damage']=max(self.s['stats']['max_damage'],amount)
        self.s['last_damage']=f'적에게 {amount} 피해'; self.log(self.s['last_damage'])
    def victory(self):
        e=self.s['enemy']; kind=e['kind']; f=self.s['floor']; self.s['stats']['wins']+=1; self.s['stats'][kind]+=1
        self.gain_gold(math.floor((10+3*f)*{'normal':1,'elite':3,'boss':10}[kind]))
        xp=math.floor((25+8*f)*{'normal':1,'elite':2,'boss':5}[kind]*e['exp_multiplier']*(.2 if self.p['level']-e['level']>=10 else 1)); self.gain_exp(xp)
        if self.rng.random()<{'normal':.15,'elite':.5,'boss':1}[kind]: self.award_equipment()
        if kind=='boss':
            self.s['boss_done']=True
            if f not in self.s['boss_first']: self.grant_item('base.item.stone',self.content.balance['boss_stones']); self.s['boss_first'].append(f)
        self.log(f"승리 · 골드 +{self.s['last_gold']} / 경험치 +{xp}")
        self.s['mode']='explore'; self.s['enemy']=None; self.s['progress']+=1
    def death(self):
        loss=self.p['gold']//10; self.p['gold']-=loss; self.s['stats']['deaths']+=1
        self.s.update(mode='base',enemy=None,event=None,progress=0,boss_done=False,statuses=[])
        self.p['hp']=max(1,math.floor(self.derived()['hp']*self.content.balance['death_hp_fraction']))
        self.log(f'패배 · 거점 귀환 · 골드 {loss} 손실')
    def tick_status(self):
        for st in self.s['statuses']:
            if st['stat']=='poison': self.p['hp']=max(0,self.p['hp']-st['value']); self.log(f"독 피해 {st['value']}")
            st['turns']-=1
        self.s['statuses']=[st for st in self.s['statuses'] if st['turns']>0]
    def counter(self,defend=False):
        e=self.s['enemy']; d=self.derived(); mult=1
        for a in e.get('abilities',[]):
            if self.s['combat_turn']%a.get('interval',1)==0 and self.rng.random()<a.get('chance',1):
                if a['type']=='heavy': mult=a['value']
                elif a['type']=='drain_mp': self.p['mp']=max(0,self.p['mp']-a['value'])
                elif a['type']=='heal': e['hp']=min(e['max_hp'],e['hp']+math.floor(e['max_hp']*a['value']))
                elif a['type']=='poison': self.s['statuses'].append(dict(stat='poison',value=a['value'],turns=3))
        if self.rng.random()<max(.05,e['accuracy']-d['evasion']):
            amount=max(1,math.floor(self.damage(e['atk'],mult,d['defense'])*(.5 if defend else 1)))
            self.p['hp']=max(0,self.p['hp']-amount); self.s['last_counter']=f'HP -{amount}'
        else: self.s['last_counter']='적 공격 회피'
        self.log(self.s['last_counter']); self.tick_status()
        if self.p['hp']<=0: self.death()
    def effects(self,effects,level=1):
        for e in effects:
            t=e['type']; v=e.get('value',0)+e.get('growth',0)*(level-1)
            if t=='damage':
                for _ in range(e.get('hits',1)):
                    if self.s['enemy']['hp']>0: self.hit(v)
            elif t in ('heal_hp','heal_mp'):
                k=t[5:]; amount=math.floor(v*self.derived()[k]) if e.get('fraction') else int(v)
                self.p[k]+=amount; self.clamp(); self.log(f'{k.upper()} +{amount}')
            elif t=='grant_gold': self.gain_gold(int(v)); self.log(f'골드 +{int(v)}')
            elif t=='grant_exp': self.gain_exp(int(v)); self.log(f'경험치 +{int(v)}')
            elif t=='grant_item': self.grant_item(e['item_id'],int(v))
            elif t=='equipment': self.award_equipment()
            elif t=='hurt': self.p['hp']=max(0,self.p['hp']-int(v)); self.log(f'HP -{int(v)}')
            elif t=='add_status': self.s['statuses'].append(dict(stat=e['stat'],value=v,turns=e['turns'])); self.log('일시 효과 적용')
            elif t=='start_combat': self.start_combat()
    def battle(self,action,key=None):
        self.require(self.s['mode']=='combat','전투 중에만 사용할 수 있습니다.')
        self.s['turn']+=1; self.s['combat_turn']+=1
        if action=='attack': self.hit()
        elif action=='heavy': self.hit(1.5,.8)
        elif action=='defend': self.log('방어 · 이번 반격 피해 50% 감소')
        elif action=='flee':
            self.require(self.s['enemy']['kind']!='boss','보스전에서는 도주할 수 없습니다.')
            if self.rng.random()<.6:
                self.s.update(mode='explore',enemy=None); self.s['stats']['escapes']+=1; self.log('도주 성공'); self.tick_status()
                if self.p['hp']<=0: self.death()
                return
            self.log('도주 실패')
        elif action=='skill':
            skill=self.content.by_id.get(key,{})
            self.require(skill.get('kind')=='active' and self.s['skills'].get(key,0)>0,'사용할 수 없는 스킬입니다.')
            self.require(self.p['mp']>=skill['mp'],'MP가 부족합니다.'); self.p['mp']-=skill['mp']; self.effects(skill['effects'],self.s['skills'][key])
        elif action=='potion': self.consume(key)
        if self.s['enemy']['hp']<=0: self.victory()
        else: self.counter(action=='defend')
    def consume(self,key):
        item=self.content.by_id.get(key,{})
        self.require(item.get('category')=='소비품' and self.s['items'].get(key,0)>0,'사용할 소비품이 없습니다.')
        self.s['items'][key]-=1; self.effects(item['effects'])
    def enhance_cost(self,item):
        n=item['enhance']+1
        return self.content.balance['enhance_gold']*item['level']*n,1+(n-1)//self.content.balance['enhance_stone_group'],1 if n<=3 else .8 if n<=6 else .6 if n<=9 else .4 if n<=12 else .2
    def metric(self,key): return self.s['highest'] if key=='highest' else self.s['stats'].get(key,0)

    def execute(self,action,**args):
        """Transactional: rejected actions never spend a turn, resource, or RNG state."""
        old=copy.deepcopy(self.s); rng=self.rng.getstate()
        try:
            self._execute(action,**args); self.clamp()
            self.s['rng_state']=self.rng.getstate()
        except Exception:
            self.s=old; self.rng.setstate(rng); raise

    def _execute(self,action,**a):
        s=self.s; p=self.p; key=a.get('key'); quantity=a.get('quantity',1)
        self.require(isinstance(quantity,int) and 1<=quantity<=999,'수량은 1~999입니다.')
        if action in ('attack','heavy','defend','flee','skill'): return self.battle(action,key)
        if action=='auto':
            self.require(s['mode']=='combat','현재 전투가 없습니다.')
            for _ in range(self.content.balance['auto_turn_limit']):
                if s['mode']!='combat': break
                setting=s['settings']; fraction=p['hp']/self.derived()['hp']
                if setting['stop_danger'] and fraction<=setting['danger']: self.log('위험 HP · 자동 전투 중단'); break
                if setting['auto_potion'] and fraction<=setting['potion_threshold'] and s['items'].get('base.item.hp',0)>0: self.battle('potion','base.item.hp'); continue
                skills=sorted((r for r in self.content['skills'] if r['kind']=='active'),key=lambda r:s['skill_auto'].get(r['id'],{}).get('priority',99))
                usable=[r for r in skills if s['skills'].get(r['id'],0)>0 and p['mp']>=r['mp'] and s['skill_auto'].get(r['id'],{}).get('enabled',False) and not (r['effects'][0]['type']=='heal_hp' and fraction>.7)]
                if setting['auto_skill'] and usable: self.battle('skill',usable[0]['id'])
                else: self.battle('attack')
            else: self.log('500턴 안전 한도 · 자동 전투 중단')
            return
        if action=='use':
            self.require(s['mode']!='event','이벤트를 먼저 해결하세요.')
            return self.battle('potion',key) if s['mode']=='combat' else self.consume(key)
        if action=='event':
            self.require(s['mode']=='event','진행 중인 이벤트가 없습니다.')
            options=s['event']['options']; index=a.get('index',0)
            self.require(0<=index<len(options),'잘못된 선택지입니다.'); option=options[index]
            self.require(all(self.condition(c) for c in option.get('conditions',[])),'선택지 조건을 충족하지 못했습니다.')
            self.require(p['gold']>=option.get('cost',0),'골드가 부족합니다.')
            p['gold']-=option.get('cost',0); s['turn']+=1; s['mode']='explore'; s['event']=None
            self.log(option['label']); self.effects(self.weighted(option['outcomes'])['effects'])
            if s['mode']!='combat': s['progress']+=1
            if p['hp']<=0: self.death()
            return
        if action=='setting':
            self.require(key in s['settings'],'알 수 없는 설정')
            value=a['value']; valid={'log_count':(5,10,20,50,200),'font_size':(11,12,13),'danger':(.2,.3,.4,.5),'potion_threshold':(.3,.5,.7),'default_screen':('던전/탐험','거점/휴식','캐릭터/정보')}
            self.require(value in valid[key] if key in valid else isinstance(value,bool),'설정값이 유효하지 않습니다.'); s['settings'][key]=value; return
        if action=='skill_auto':
            self.require(key in s['skill_auto'],'잘못된 스킬 설정')
            field=a['field']; value=a['value']; self.require((field=='enabled' and isinstance(value,bool)) or (field=='priority' and value in (1,2,3)),'잘못된 자동 스킬 값'); s['skill_auto'][key][field]=value; return
        self.require(s['mode'] not in ('combat','event'),'현재 전투 또는 이벤트를 먼저 해결하세요.')
        if action=='enter':
            self.require(s['mode']=='base','거점에서 입장하세요.'); floor=a.get('floor',1)
            self.require(isinstance(floor,int) and 1<=floor<=s['highest'],'아직 개방되지 않은 층입니다.')
            s.update(mode='explore',floor=floor,progress=0,boss_done=False,event_seen={}); self.log(f'{floor}층 입장')
        elif action=='explore':
            self.require(s['mode']=='explore','거점에서 던전에 입장하세요.'); s['turn']+=1; s['stats']['explorations']+=1; s['last_gold']=0; s['last_exp']=0; s['last_item']='없음'
            self.tick_status()
            if p['hp']<=0: self.death(); return
            if s['floor']%10==0 and s['progress']>=2 and not s['boss_done']: self.start_combat('boss'); return
            table=self.content.balance['encounters']; kind=self.rng.choices(list(table),weights=list(table.values()))[0]
            if kind in ('normal','elite'): self.start_combat(kind)
            elif kind=='event':
                events=[e for e in self.content['events'] if self.eligible(e)]
                if events:
                    s['event']=copy.deepcopy(self.weighted(events)); s['event_seen'][s['event']['id']]=s['stats']['explorations']; s['mode']='event'; self.log(s['event']['title'])
                else: s['progress']+=1; self.log('조용한 통로를 지나갔습니다.')
            else:
                s['progress']+=1
                if kind=='chest':
                    if self.rng.random()<self.content.balance['chest_equipment_chance']: self.award_equipment()
                    else: self.gain_gold(self.content.balance['chest_gold_base']+self.content.balance['chest_gold_per_floor']*s['floor']); self.log(f"보물 · 골드 +{s['last_gold']}")
                else: self.effects([{'type':'heal_hp','value':.25,'fraction':True}]); self.log('휴식 장소 · HP 회복')
        elif action=='next':
            self.require(s['mode']=='explore' and self.complete(),'현재 층 목표를 먼저 완료하세요.')
            s['floor']+=1; s['highest']=max(s['highest'],s['floor']); s['progress']=0; s['boss_done']=False; self.log(f"{s['floor']}층 도달")
        elif action=='return':
            self.require(s['mode']=='explore','던전에서만 귀환할 수 있습니다.'); s.update(mode='base',progress=0,boss_done=False,statuses=[]); s['stats']['returns']+=1; self.log('거점 귀환')
        elif action=='invest':
            self.require(key in p['attributes'] and p['points']>0,'남은 능력치 포인트가 없습니다.')
            p['points']-=1; p['attributes'][key]+=1; s['last_growth']=STAT_NAMES[key]+' +1'; self.log(s['last_growth'])
        elif action=='upgrade_skill':
            self.require(key in self.content.by_id and key in s['skills'],'알 수 없는 스킬')
            self.require(p['skill_points']>0 and s['skills'][key]<self.content.by_id[key]['max_level'],'스킬 포인트 부족 또는 최대 레벨입니다.')
            p['skill_points']-=1; s['skills'][key]+=1; self.log('스킬 강화 완료')
        elif action=='equip':
            self.require(key in s['bag'],'가방의 장비를 선택하세요.'); item=s['inventory'][key]
            self.require(item['base_id'] in self.content.by_id,'미확인 장비는 장착할 수 없습니다.')
            prev=s['equipped'].get(item['slot']); s['bag'].remove(key)
            if prev: s['bag'].append(prev)
            s['equipped'][item['slot']]=key; self.log(self.item_name(item)+' 장착')
        elif action=='unequip':
            self.require(key in s['equipped'] and self.bag_used()<30,'해제할 장비가 없거나 가방이 가득 찼습니다.')
            s['bag'].append(s['equipped'].pop(key)); self.log('장비 해제')
        elif action in ('sell','discard'):
            if action=='sell': self.require(s['mode']=='base','판매는 거점에서만 가능합니다.')
            if key in s['inventory']:
                self.require(key in s['bag'],'착용 또는 보관 중인 장비는 처분할 수 없습니다.')
                if action=='sell': p['gold']+=self.sell_price(s['inventory'][key])
                s['bag'].remove(key); del s['inventory'][key]
            else:
                self.require(key in self.content.by_id and s['items'].get(key,0)>=quantity,'보유 수량이 부족합니다.')
                s['items'][key]-=quantity
                if action=='sell': p['gold']+=self.content.by_id[key]['sell_price']*quantity
            self.log('판매 완료' if action=='sell' else '버리기 완료')
        elif action=='claim':
            ach=self.content.by_id.get(key,{})
            self.require('metric' in ach and self.metric(ach['metric'])>=ach['target'] and key not in s['claimed'],'미달성 또는 이미 수령한 업적입니다.')
            p['gold']+=ach['reward'].get('gold',0); s['claimed'].append(key); self.log('업적 보상 수령')
        elif action in ('rest','buy','enhance','deposit','withdraw','expand'):
            self.require(s['mode']=='base','거점에서만 이용할 수 있습니다.')
            if action=='rest':
                keys=['hp','mp'] if key=='both' else [key]; self.require(all(k in ('hp','mp') for k in keys),'회복 종류 오류')
                keys=[k for k in keys if p[k]<self.derived()[k]]; self.require(bool(keys),'이미 모두 회복되어 있습니다.')
                cost=sum(self.content.balance['rest_'+k]*p['level'] for k in keys); self.require(p['gold']>=cost,'골드가 부족합니다.')
                p['gold']-=cost
                for k in keys: p[k]=self.derived()[k]
                self.log('휴식 · 회복 완료')
            elif action=='buy':
                self.require(key in self.content.by_id,'알 수 없는 상품')
                item=self.content.by_id[key]; equipment=key.startswith('base.equipment.') or 'slot' in item
                cost=(self.equipment_price() if equipment else item['price'])*quantity
                slots=quantity if equipment else int(s['items'].get(key,0)==0)
                self.require(self.bag_used()+slots<=30,'가방이 가득 찼습니다.'); self.require(p['gold']>=cost,'골드가 부족합니다.'); p['gold']-=cost
                if equipment:
                    for _ in range(quantity):
                        gear=self.generate_equipment(key); s['inventory'][gear['instance_id']]=gear; s['bag'].append(gear['instance_id'])
                else: self.grant_item(key,quantity)
                self.log('구매 완료')
            elif action=='enhance':
                self.require(key in s['bag']+list(s['equipped'].values()),'강화할 장비를 선택하세요.'); item=s['inventory'][key]
                self.require(item['base_id'] in self.content.by_id and item['enhance']<15,'미확인 장비 또는 최대 강화입니다.')
                gold,stones,chance=self.enhance_cost(item); self.require(p['gold']>=gold and s['items'].get('base.item.stone',0)>=stones,'골드 또는 강화석이 부족합니다.')
                p['gold']-=gold; s['items']['base.item.stone']-=stones; success=self.rng.random()<chance
                item['enhance']+=int(success); s['last_enhance']='강화 성공' if success else '강화 실패 · 단계 유지'; self.log(s['last_enhance'])
            elif action=='deposit':
                self.require(key in s['bag'] and len(s['storage'])<s['storage_capacity'],'보관할 수 없습니다.')
                s['bag'].remove(key); s['storage'].append(key); self.log('보관 완료')
            elif action=='withdraw':
                self.require(key in s['storage'] and self.bag_used()<30,'꺼낼 수 없습니다.')
                s['storage'].remove(key); s['bag'].append(key); self.log('꺼내기 완료')
            else:
                cost=self.content.balance['storage_cost']*(1+(s['storage_capacity']-50)//10)
                self.require(p['gold']>=cost,'골드가 부족합니다.'); p['gold']-=cost; s['storage_capacity']+=10; self.log('보관함 +10칸')
        else: raise RuleError('알 수 없는 명령: '+action)
