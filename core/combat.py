"""Shared player/enemy effect processing and phase-one patterned combat."""
import copy
import math
from .catalogue import cid, OPTION_STATS
from .legacy_engine import GameEngine as LegacyEngine

BUFF_STATS={7:{'atk':-.2},8:{'defense':-.2},9:{'atk':-.1,'defense':-.1},10:{'atk':.2},11:{'defense':.2}}

class CombatMixin:
    def actor(self,side): return self.p if side=='player' else self.s['enemy']
    def actor_statuses(self,side): return self.s['statuses'] if side=='player' else self.s['enemy'].get('statuses',[])
    def status_label(self,side='player'):
        if side=='enemy' and not self.s['enemy']: return '없음'
        return ', '.join(f"{st.get('name',st.get('stat','효과'))} {st['turns']}턴"+(f" ×{st['stacks']}" if st.get('stacks',1)>1 else '') for st in self.actor_statuses(side)) or '없음'

    def apply_modifiers(self,d,statuses):
        for st in statuses:
            number=st.get('effect_number')
            for stat,value in BUFF_STATS.get(number,{}).items(): d[stat]*=1+value
            if number==12: d['evasion']+=.08
            if number==13: d['leech']=d.get('leech',0)+.05
            if number==14: d['hp_regen']=d.get('hp_regen',0)+.04
            if number==15: d['reflect']=d.get('reflect',0)+.1
            if st.get('stat') in d and number is None:
                stat=st['stat']
                if st.get('additive'): d[stat]+=st['value']
                else: d[stat]*=1+st['value']
        for stat,cap in {'crit':.75,'evasion':.45,'counter':.4,'reduction':.7,'leech':.25,'status_resist':.75,'gold_bonus':2,'exp_bonus':2,'penetration':1,'crit_resist':.75}.items(): d[stat]=max(0,min(cap,d.get(stat,0)))
        for stat in ('atk','defense','hp','mp'): d[stat]=max(1,math.floor(d.get(stat,1)))
        return d

    def derived(self):
        if getattr(self,'_legacy_running',False): return LegacyEngine.derived(self)
        attributes=dict(self.p['attributes']); gear={k:0 for k in OPTION_STATS}
        for iid in self.s['equipped'].values():
            item=self.s['inventory'][iid]
            if item['base_id'] in self.content.by_id:
                for key,value in self.gear_stats(item).items(): gear[key]=gear.get(key,0)+value
        for key in attributes: attributes[key]+=gear.get(key,0)
        attributes['luk']*=1+gear['luk_pct']
        d=dict(gear); d.update(attributes)
        d.update(atk=15+2*(attributes['str']-10)+gear['atk'],defense=5+.5*(attributes['vit']-10)+gear['defense'],hp=100+10*(attributes['vit']-10)+gear['hp'],mp=30+5*(attributes['int']-5)+gear['mp'],crit=.002*attributes['luk']+gear['crit'],evasion=.002*attributes['dex']+gear['evasion'])
        for skill in self.content['skills']:
            if skill['kind']=='passive':
                for effect in skill['effects']: d[effect['stat']]*=1+effect['value']*self.s['skills'].get(skill['id'],0)
        return self.apply_modifiers(d,self.s['statuses'])

    def enemy_stats(self):
        enemy=self.s['enemy']; d={k:0 for k in OPTION_STATS}
        d.update(atk=enemy['atk'],defense=enemy['defense'],hp=enemy['max_hp'],mp=30,crit=enemy.get('crit',.05),evasion=enemy['evasion'],leech=enemy.get('leech',0))
        if enemy.get('phase2'):
            d['atk']*=enemy.get('phase2_multiplier',1.25)
        return self.apply_modifiers(d,enemy.get('statuses',[]))

    def stats_for(self,side): return self.derived() if side=='player' else self.enemy_stats()

    def apply_status(self,number,target,source='enemy',chance=None):
        definition=self.content.by_id[cid(f'EF{number:03}')]; actor=self.actor(target)
        if actor is None or actor['hp']<=0: return False
        if number in (4,5) and actor.get('cc_until',-1)>=self.s['turn']: return False
        chance=definition['base_chance_pct']/100 if chance is None else chance
        if number<10: chance=max(0,chance-self.stats_for(target)['status_resist'])
        if self.rng.random()>=chance: return False
        statuses=self.actor_statuses(target); current=next((st for st in statuses if st.get('effect_number')==number),None)
        limit={1:3,2:2,3:3}.get(number,1)
        if current:
            current['stacks']=min(limit,current.get('stacks',1)+1); current['turns']=max(current['turns'],definition['duration_turns']); current['applied_at']=self.s['turn']
        else:
            statuses.append(dict(effect_number=number,effect_id=definition['id'],name=definition['name'],stat='effect',value=0,turns=definition['duration_turns'],stacks=1,applied_at=self.s['turn']-(1 if target=='enemy' and source=='player' and number<10 else 0),source_atk=self.stats_for(source)['atk']))
        self.log(('플레이어' if target=='player' else '적')+' · '+definition['name']); return True

    def tick_start(self,side):
        actor=self.actor(side); stats=self.stats_for(side)
        # A freshly applied regeneration starts on the recipient's next turn.
        fresh=sum(.04 for st in self.actor_statuses(side) if st.get('effect_number')==14 and st['applied_at']>=self.s['turn'])
        for resource in ('hp','mp'):
            if resource not in actor: continue
            rate=max(0,stats.get(resource+'_regen',0)-(fresh if resource=='hp' else 0))
            amount=math.floor(stats[resource]*rate)
            if amount: actor[resource]=min(stats[resource],actor[resource]+amount); self.log(f"{side} {resource.upper()} 재생 +{amount}")

    def tick_end(self,side):
        actor=self.actor(side)
        if not actor: return
        statuses=self.actor_statuses(side)
        for st in list(statuses):
            if st.get('applied_at',-1)>=self.s['turn']: continue
            n=st.get('effect_number'); amount=0
            if n in (1,3): amount=max(1,math.floor(self.stats_for(side)['hp']*(.03 if n==1 else .02)*st.get('stacks',1)))
            elif n==2: amount=max(1,math.floor(st['source_atk']*.08*st.get('stacks',1)))
            elif st.get('stat')=='poison': amount=st['value']
            if amount: actor['hp']=max(0,actor['hp']-amount); self.log(f'{side} 지속 피해 {amount}')
            st['turns']-=1
            if st['turns']<=0:
                statuses.remove(st)
                if n in (4,5):
                    actor['cc_until']=self.s['turn']+2
                    if n==5: statuses.append(dict(stat='evasion',value=-.05,additive=True,name='빙결 후 둔화',turns=1,applied_at=self.s['turn']))
            if actor['hp']<=0: break

    def tick_status(self):
        if self.s.get('legacy_pending') or getattr(self,'_legacy_running',False): return LegacyEngine.tick_status(self)
        self.tick_start('player'); self.tick_end('player')

    def resolve_deaths(self):
        if self.p['hp']<=0: self.death(); return True
        if self.s['enemy'] and self.s['enemy']['hp']<=0: self.victory(); return True
        return False

    def direct_hit(self,source,mult=1,accuracy=.95,action='attack',secondary=False):
        target='enemy' if source=='player' else 'player'; attacker=self.actor(source); defender=self.actor(target)
        if not attacker or not defender or attacker['hp']<=0 or defender['hp']<=0: return 0
        a=self.stats_for(source); b=self.stats_for(target)
        if self.rng.random()>=max(.05,accuracy-b['evasion']):
            message='공격 빗나감' if source=='player' else '적 공격 회피'; self.log(message); self.s['last_damage' if source=='player' else 'last_counter']=message; return 0
        bonus=a.get('heavy_damage' if action=='heavy' else 'normal_damage',0) if action in ('attack','heavy') else 0
        amount=max(1,math.floor(a['atk']*mult*(1+bonus)*self.rng.uniform(.9,1.1)-.6*b['defense']*(1-a.get('penetration',0))))
        critical=self.rng.random()<max(0,a['crit']-b.get('crit_resist',0))
        amount=math.floor(amount*(1.5+a.get('crit_damage',0) if critical else 1)*(1+a.get('extra_damage',0))*(1-b.get('reduction',0)))
        if defender.get('guard'): amount=math.floor(amount*.5)
        if target=='player' and self.s['exploration_bonuses'].get('protection'):
            amount=math.floor(amount*.7); self.s['exploration_bonuses'].pop('protection')
        amount=max(1,amount); shield=defender.get('shield',0); absorbed=min(shield,amount); defender['shield']=shield-absorbed; amount-=absorbed
        actual=min(defender['hp'],amount); defender['hp']-=actual
        if source=='player':
            self.s['stats']['damage']+=actual; self.s['stats']['max_damage']=max(self.s['stats']['max_damage'],actual); self.s['last_damage']=f'적에게 {actual} 피해'
        else: self.s['last_counter']=f'HP -{actual}'
        self.log(self.s['last_damage' if source=='player' else 'last_counter'])
        if not secondary: attacker['hp']=min(a['hp'],attacker['hp']+math.floor(actual*a.get('leech',0)))
        # Secondary damage never reflects, counters, or leeches again.
        if not secondary and actual:
            reflected=math.floor(actual*b.get('reflect',0))
            if reflected: attacker['hp']=max(0,attacker['hp']-reflected); self.log(f'피해 반사 {reflected}')
            if attacker['hp']>0 and defender['hp']>0 and self.rng.random()<b.get('counter',0): self.direct_hit(target,secondary=True)
        return actual

    def hit(self,mult=1,accuracy=.95):
        if getattr(self,'_legacy_running',False): return LegacyEngine.hit(self,mult,accuracy)
        return self.direct_hit('player',mult,accuracy,getattr(self,'_attack_kind','skill'))

    def start_combat(self,kind='normal'):
        f=self.s['floor']; zone=(f-1)%100+1; environment=self.environment(); boss=None
        if kind=='boss':
            boss=self.content['bosses'][(f//10-1)%10]; base=self.content.by_id[boss['monster_id']]
        else:
            rows=[r for r in self.content['monsters'] if r['min_floor']<=zone<=r['max_floor']]
            base=self.rng.choices(rows,weights=[r['weight']*(3 if r['category']==environment['primary_family'] else 1) for r in rows])[0]
        enemy=copy.deepcopy(base); enemy.update(level=f,kind=kind,exp_multiplier=1,gold_multiplier=1,statuses=[],pattern_index=0,guard=False,shield=0,crit=self.content.catalogue['defaults']['monster_critical_chance'],prefix_ids=[])
        for key,rate in [('hp',.12),('atk',.08),('defense',.06)]: enemy[key]=math.floor(base[key]*(1+rate*(f-1)))
        risk=1+environment['risk_modifier_pct']/100
        if self.s['floor_type']=='FLR004': risk*=1.2
        enemy['hp']=math.floor(enemy['hp']*risk); enemy['atk']=math.floor(enemy['atk']*risk)
        if kind=='elite': enemy['hp']*=2; enemy['atk']=math.floor(enemy['atk']*1.4)
        if boss:
            enemy['hp']=math.floor(enemy['hp']*boss['hp_multiplier']); enemy['atk']=math.floor(enemy['atk']*boss['atk_multiplier']); enemy['defense']=math.floor(enemy['defense']*boss['def_multiplier'])
            enemy.update(name=boss['name'],boss_id=boss['id'],effect_id=boss['effect_id'],pattern=boss['pattern'],phase2=False,phase2_hp_pct=boss['phase2_hp_pct'],phase2_multiplier=boss['phase2_multiplier'])
        elif kind=='elite' or self.rng.random()<.18:
            count=self.rng.randint(1,2) if kind=='elite' else 1; candidates=list(self.content['prefixes'])
            for _ in range(count):
                prefix=self.weighted(candidates); candidates=[p for p in candidates if p['category']!=prefix['category']]; n=int(prefix['source_id'][3:]); enemy['prefix_ids'].append(prefix['id']); enemy['name']=prefix['name']+' '+enemy['name']
                if n<=12:
                    stat='atk' if n<=4 else 'defense' if n<=8 else 'hp'; percentages=([15,20,25,30] if n<=8 else [15,25,35,45]); enemy[stat]=math.floor(enemy[stat]*(1+percentages[(n-1)%4]/100))
                elif n in (13,14,16): enemy.setdefault('on_hit_effects',[]).append({13:1,14:2,16:9}[n])
                elif n==15: enemy['leech']=.05
                else: enemy['gold_multiplier']*=1+(.2+.1*(n-17)); enemy['exp_multiplier']*=1+(.2+.1*(n-17))
        enemy['max_hp']=enemy['hp']; self.s.update(enemy=enemy,mode='combat',combat_turn=0,combat_logs=[],legacy_pending=False)
        self.p['shield']=math.floor(self.derived()['hp']*self.derived().get('shield',0)); self.p['guard']=False
        self.s['stats']['battles']+=1; self.log(enemy['name']+' 등장')

    def counter(self,defend=False):
        if getattr(self,'_legacy_running',False): return LegacyEngine.counter(self,defend)
        enemy=self.s['enemy']; self.tick_start('enemy')
        enemy['guard']=False
        if enemy.get('phase2_hp_pct') and not enemy['phase2'] and enemy['hp']/enemy['max_hp']<=enemy['phase2_hp_pct']/100:
            enemy['phase2']=True; self.log('보스 2단계 · 공격력 증가')
        blocked=any(st.get('effect_number') in (4,5) for st in enemy['statuses'])
        action=enemy['pattern'][enemy['pattern_index']%len(enemy['pattern'])]
        if blocked: self.log('적 행동 불가')
        else:
            enemy['pattern_index']+=1
            if action=='special' and any(st.get('effect_number')==6 for st in enemy['statuses']):
                action='attack'; self.log('적 침묵 · 특수공격 대신 일반 공격')
            if action=='defend': enemy['guard']=True; self.log('적 방어 · 다음 피격 피해 50% 감소')
            else:
                damage=self.direct_hit('enemy',self.content.catalogue['defaults']['special_damage'] if action=='special' else 1,enemy['accuracy'],action='skill' if action=='special' else 'attack')
                if self.resolve_deaths(): return
                if damage:
                    for number in enemy.get('on_hit_effects',[]): self.apply_status(number,'player',chance=.15)
                if enemy.get('effect_id') and (action=='special' or 'special' not in enemy['pattern']):
                    number=int(enemy['effect_id'][2:]); target='enemy' if number>=10 else 'player'
                    if target=='enemy' or damage: self.apply_status(number,target)
        if not self.resolve_deaths(): self.tick_end('enemy'); self.resolve_deaths()

    def battle(self,action,key=None):
        if self.s.get('legacy_pending'):
            self._legacy_running=True
            try: return LegacyEngine.battle(self,action,key)
            finally: self._legacy_running=False
        self.require(self.s['mode']=='combat','전투 중에만 사용할 수 있습니다.')
        if action=='flee': self.require(self.s['enemy']['kind']!='boss','보스전에서는 도주할 수 없습니다.')
        if action=='skill':
            skill=self.content.by_id.get(key,{})
            self.require(skill.get('kind')=='active' and self.s['skills'].get(key,0)>0,'사용할 수 없는 스킬입니다.')
            self.require(not any(st.get('effect_number')==6 for st in self.s['statuses']),'침묵 중에는 스킬을 사용할 수 없습니다.')
            self.require(self.p['mp']>=skill['mp'],'MP가 부족합니다.')
        if action=='potion': self.validate_consumable(key)
        self.s['turn']+=1; self.s['combat_turn']+=1; self.tick_start('player')
        blocked=any(st.get('effect_number') in (4,5) for st in self.s['statuses'])
        self.p['guard']=action=='defend' and not blocked
        if blocked: self.log('행동 불가 · 자원은 소모하지 않습니다.')
        elif action in ('attack','heavy'):
            self._attack_kind=action
            try: self.hit(1.5 if action=='heavy' else 1,.8 if action=='heavy' else .95)
            finally: self._attack_kind='skill'
        elif action=='skill': self.p['mp']-=skill['mp']; self.effects(skill['effects'],self.s['skills'][key])
        elif action=='potion': self.consume(key)
        elif action=='defend': self.log('방어')
        elif action=='flee':
            if self.rng.random()<.6:
                self.s.update(mode='explore',enemy=None); self.s['stats']['escapes']+=1; self.tick_end('player'); self.log('도주 성공')
                if self.p['hp']<=0: self.death()
                return
            self.log('도주 실패')
        if self.resolve_deaths(): return
        self.tick_end('player')
        if not self.resolve_deaths(): self.counter(action=='defend')

    def validate_consumable(self,key):
        item=self.content.by_id.get(key,{})
        self.require(item.get('category')=='소비품' and self.s['items'].get(key,0)>0,'사용할 소비품이 없습니다.')
        self.require(self.s['mode'] in item.get('contexts',['base','explore','combat']),'현재 위치에서는 사용할 수 없습니다.')
        return item

    def consume(self,key):
        item=self.validate_consumable(key)
        if not item.get('catalogue'): return LegacyEngine.consume(self,key)
        self.s['items'][key]-=1; number=item['use_number']; self.log(item['name']+' 사용')
        if number<=8: self.effects(item['effects'])
        elif number in (9,10,12): self.apply_status({9:10,10:11,12:12}[number],'player','player',1)
        elif number==11:
            self.s['statuses']=[st for st in self.s['statuses'] if st.get('name')!='치명타 물약']
            self.s['statuses'].append(dict(stat='crit',value=.1,additive=True,name='치명타 물약',turns=3,applied_at=self.s['turn']))
        elif number in (13,14,15,16):
            remove={13:{1},14:{2},15:{9},16:set(range(1,10))}[number]
            self.s['statuses']=[st for st in self.s['statuses'] if st.get('effect_number') not in remove and not (number in (13,16) and st.get('stat')=='poison') and not (number==16 and st.get('value',0)<0)]
        elif number==17: self.return_to_base()
        elif number==18: self.s['exploration_bonuses']['treasure_pp']=10
        elif number==19: self.s['exploration_bonuses']['rarity_pp']=self.content.catalogue['defaults']['lucky_charm_pp']
        elif number==20: self.s['exploration_bonuses']['protection']=True

    def effects(self,effects,level=1):
        if getattr(self,'_legacy_running',False): return LegacyEngine.effects(self,effects,level)
        for effect in effects:
            if effect['type']=='damage':
                for _ in range(effect.get('hits',1)):
                    if not self.s['enemy'] or self.s['enemy']['hp']<=0 or self.p['hp']<=0: break
                    self.hit(effect['value']+effect.get('growth',0)*(level-1))
            else: LegacyEngine.effects(self,[effect],level)

    def victory(self):
        if getattr(self,'_legacy_running',False): return LegacyEngine.victory(self)
        enemy=self.s['enemy']; kind=enemy['kind']; floor=self.s['floor']; d=self.derived(); environment=self.environment()
        self.s['stats']['wins']+=1; self.s['stats'][kind]+=1
        reward=1+environment['reward_modifier_pct']/100
        gold=math.floor((10+3*floor)*{'normal':1,'elite':3,'boss':10}[kind]*enemy['gold_multiplier']*reward*(1+d['gold_bonus'])*(1.3 if self.s['floor_type']=='FLR004' else 1))
        xp=math.floor((25+8*floor)*{'normal':1,'elite':2,'boss':5}[kind]*enemy['exp_multiplier']*reward*(1+d['exp_bonus'])*(.2 if self.p['level']-enemy['level']>=10 else 1))
        self.gain_gold(gold); self.gain_exp(xp)
        chance=min(1,{'normal':.15,'elite':.5,'boss':1}[kind]+d['drop_bonus'])
        dropped=(kind=='elite' and self.s['elite_misses']>=10) or self.rng.random()<chance
        if dropped: self.award_equipment()
        if kind=='elite': self.s['elite_misses']=0 if dropped else self.s['elite_misses']+1
        if self.rng.random()<.2 and enemy.get('material_id'): self.grant_item(cid(enemy['material_id']),1)
        if self.rng.random()<.05:
            tier=min(4,((floor-1)%100)//20); pool=[r for r in self.content['materials'] if (int(r['source_id'][3:])-1)%5<=tier]; self.grant_item(self.rng.choice(pool)['id'],1)
        if kind=='boss':
            self.s['boss_done']=True; self.grant_item(cid('MAT018'),1)
            if floor not in self.s['boss_first']: self.grant_item(cid('MAT016'),3); self.s['boss_first'].append(floor)
        elif kind=='elite' and self.rng.random()<.2: self.grant_item(cid('MAT016'),1)
        for resource in ('hp','mp'): self.p[resource]=min(self.derived()[resource],self.p[resource]+math.floor(self.derived()[resource]*d.get('kill_'+resource,0)))
        self.log(f'승리 · 골드 +{gold} / 경험치 +{xp}')
        self.s.update(mode='explore',enemy=None); self.s['progress']+=1; self.p['guard']=False; self.p['shield']=0
