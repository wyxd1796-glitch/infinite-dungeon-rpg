import copy
import math
from .legacy_engine import GameEngine as LegacyEngine, RuleError, SLOTS, STAT_NAMES
from .catalogue import activate, cid, OPTION_NAMES
from .combat import CombatMixin
from .loot import LootMixin
from .migrations import migrate_v1_to_v2

STAT_NAMES.update(OPTION_NAMES)

class GameEngine(LootMixin,CombatMixin,LegacyEngine):
    def __init__(self,root,state=None,seed=None):
        loaded=migrate_v1_to_v2(state) if state and state.get('save_schema_version')==1 else copy.deepcopy(state)
        super().__init__(root,loaded,seed)
        activate(self.content)
        self.s.update(save_schema_version=2,game_version='1.1.0',active_content_packs=copy.deepcopy(self.content.packs),catalogue_version=self.content.catalogue['version'])
        for key,value in dict(pending_loot=[],elite_misses=0,exploration_bonuses={},shop_stock=[],legacy_pending=False,floor_type='FLR005' if self.s['floor']%10==0 else 'FLR001').items(): self.s.setdefault(key,value)
        if state is None: self.s['items']={cid('CON001'):3,cid('CON005'):1,cid('MAT016'):0}
        if not self.s['shop_stock']: self.refresh_shop()
        self.s.setdefault('event_result',None)

    def log(self,text):
        super().log(text)
        if getattr(self,'_event_messages',None) is not None: self._event_messages.append(text)

    def resolve_event(self,**args):
        event=copy.deepcopy(self.s['event']); self._event_messages=[]
        try:
            LegacyEngine._execute(self,'event',**args)
            index=args.get('index',0); option=event['options'][index]
            messages=self._event_messages[1:]
            sentences=[]
            for message in messages:
                if message.startswith('골드 +'): message=message[4:]+' G를 얻었습니다.'
                elif message.startswith('경험치 +'): message='경험치 '+message[5:]+'를 얻었습니다.'
                elif message.startswith('HP -'): message=message[4:]+'의 피해를 입었습니다.'
                elif message.startswith(('HP +','MP +')): message=message[:2]+'가 '+message[4:]+' 회복되었습니다.'
                sentences.append(message)
            if not sentences: sentences=['별다른 일 없이 그곳을 지나갔습니다.']
            if option.get('cost'): sentences.insert(0,f"비용으로 {option['cost']} G를 지불했습니다.")
            self.s['event_result']=dict(title=event['title'],description=event['description'],choice=option['label'],text='\n'.join(sentences))
        finally: self._event_messages=None

    def environment(self):
        enemy=self.s.get('enemy')
        if self.s['mode']=='combat' and enemy:
            if enemy.get('environment_snapshot'): return enemy['environment_snapshot']
            return self.content.by_id[cid(f"ENV{((self.s['floor']-1)%100)//10+1:03}")]
        return self.content.by_id[cid(self.content.regions.at(self.s['floor'])['environment_id'])]
    def floor_type_name(self): return self.content.by_id[cid(self.s['floor_type'])]['name']
    def roll_floor(self):
        self.s['floor_type']='FLR005' if self.s['floor']%10==0 else self.rng.choices(['FLR001','FLR002','FLR003','FLR004'],weights=[75,10,10,5])[0]

    def return_to_base(self):
        self.require(self.s['mode']=='explore','전투 밖 던전에서만 귀환할 수 있습니다.')
        self.s.update(mode='base',progress=0,boss_done=False,statuses=[]); self.p['guard']=False; self.p['shield']=0; self.s['stats']['returns']+=1; self.refresh_shop(); self.log('거점 귀환')

    def death(self):
        LegacyEngine.death(self); self.p['guard']=False; self.p['shield']=0; self.refresh_shop()

    def explore(self):
        self.require(self.s['mode']=='explore','거점에서 던전에 입장하세요.')
        self.s['turn']+=1; self.s['stats']['explorations']+=1; self.s.update(last_gold=0,last_exp=0,last_item='없음')
        self.tick_status()
        if self.p['hp']<=0: self.death(); return
        if self.s['floor']%10==0 and self.s['progress']>=2 and not self.s['boss_done']: self.start_combat('boss'); return
        table=dict(self.content.balance['encounters'])
        if self.s['floor_type']=='FLR002': table['elite']+=15; table['normal']-=15
        if self.s['floor_type']=='FLR003': table['chest']+=20; table['normal']-=20
        bonus=self.s['exploration_bonuses'].pop('treasure_pp',0); table['chest']+=bonus; table['normal']-=bonus
        kind=self.rng.choices(list(table),weights=list(table.values()))[0]
        if kind in ('normal','elite'): self.start_combat(kind)
        elif kind=='event':
            candidates=[r for r in self.content['events'] if self.eligible(r)]
            if candidates:
                event=copy.deepcopy(self.weighted(candidates)); self.s['event']=event; self.s['mode']='event'; self.s['event_seen'][event['id']]=self.s['stats']['explorations']; self.log(event['title'])
            else: self.s['progress']+=1; self.log('조용한 통로')
        else:
            self.s['progress']+=1
            if kind=='chest':
                if self.rng.random()<.5: self.award_equipment()
                else: self.gain_gold(20+5*self.s['floor']); self.log(f"보물 · 골드 +{self.s['last_gold']}")
            else: self.effects([dict(type='heal_hp',value=.25,fraction=True)])

    def auto_skill_allowed(self,skill):
        silenced=any(st.get('effect_number')==6 for st in self.s['statuses'])
        return not silenced and self.s['skills'].get(skill['id'],0)>0 and self.p['mp']>=skill['mp'] and not (skill['effects'][0]['type']=='heal_hp' and self.p['hp']/self.derived()['hp']>.7)

    def auto_battle(self):
        self.require(self.s['mode']=='combat','현재 전투가 없습니다.')
        for _ in range(self.content.balance['auto_turn_limit']):
            if self.s['mode']!='combat': break
            settings=self.s['settings']; fraction=self.p['hp']/self.derived()['hp']
            if settings['stop_danger'] and fraction<=settings['danger']: self.log('위험 HP · 자동 전투 중단'); break
            potion=self.automatic_potion()
            if settings['auto_potion'] and fraction<=settings['potion_threshold'] and potion: self.battle('potion',potion); continue
            skills=sorted([r for r in self.content['skills'] if r['kind']=='active'],key=lambda r:(self.s['skill_auto'][r['id']]['priority'],r['id']))
            usable=[r for r in skills if self.s['skill_auto'][r['id']]['enabled'] and self.auto_skill_allowed(r)]
            if settings['auto_skill'] and usable: self.battle('skill',usable[0]['id'])
            else: self.battle('attack')
        else: self.log('500턴 안전 한도 · 자동 전투 중단')

    def _execute(self,action,**args):
        if action=='continue_event':
            self.require(bool(self.s.get('event_result')),'확인할 이벤트 결과가 없습니다.')
            self.s['event_result']=None
            return
        self.require(not self.s.get('event_result') or action in ('setting','skill_auto'),'이벤트 결과를 확인한 뒤 계속하기를 눌러 주세요.')
        if action=='event': return self.resolve_event(**args)
        quantity=args.get('quantity',1)
        self.require(isinstance(quantity,int) and 1<=quantity<=999,'수량은 1~999입니다.')
        if action=='use' and self.s['mode']=='explore':
            item=self.validate_consumable(args.get('key'))
            if item.get('consumes_turn',False):
                self.s['turn']+=1; self.actor_phase('player','turn_start'); self.consume(args.get('key')); self.actor_phase('player','turn_end')
                if self.p['hp']<=0: self.death()
            else: self.consume(args.get('key'))
            return
        if action=='auto': return self.auto_battle()
        if action=='explore': return self.explore()
        if action=='return': return self.return_to_base()
        if action=='buy': return self.buy(args.get('key'),quantity)
        if action=='enhance': return self.enhance(args.get('key'),args.get('material',cid('MAT016')))
        if action in ('claim_loot','discard_loot'): return self.pending_action(args.get('key'),action=='discard_loot')
        result=LegacyEngine._execute(self,action,**args)
        if action in ('enter','next'): self.roll_floor()
        return result

    def execute(self,action,**args):
        super().execute(action,**args)
        if self.s.get('legacy_pending') and self.s['mode'] not in ('combat','event'): self.s['legacy_pending']=False
