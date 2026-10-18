"""Shared player/enemy effect processing and phase-one patterned combat."""
import copy
import math
from .catalogue import cid, OPTION_STATS
from .legacy_engine import GameEngine as LegacyEngine
from .effect_timing import DamageKind, SHIELDED_DAMAGE
from .phase3_effects import EFFECTS, DESCRIPTIONS, BATTLE_RULES_VERSION, required_version

BUFF_STATS={7:{'atk':-.2},8:{'defense':-.2},9:{'atk':-.1,'defense':-.1},10:{'atk':.2},11:{'defense':.2}}

class CombatMixin:
    def healing_amount(self,side,amount):
        enemy=self.s.get('enemy')
        return math.floor(amount*.5) if side=='player' and self.s['mode']=='combat' and enemy and enemy.get('healing_suppression',0)>0 else amount
    def actor(self,side): return self.p if side=='player' else self.s['enemy']
    def actor_statuses(self,side): return self.s['statuses'] if side=='player' else self.s['enemy'].get('statuses',[])

    def action_blocked(self,side,roll=False):
        statuses=self.actor_statuses(side)
        if any(st.get('effect_number') in (4,5) for st in statuses): return True
        return roll and any(st.get('effect_number')==22 for st in statuses) and self.rng.random()<.25

    def skill_mp_cost(self,skill):
        if isinstance(skill,str): skill=self.content.by_id[skill]
        return math.ceil(skill['mp']*1.3) if any(st.get('effect_number')==26 for st in self.s['statuses']) else skill['mp']

    def actor_phase(self,side,phase):
        """Shared recipient timing; callers own death settlement between phases."""
        if side not in ('player','enemy'): raise ValueError('알 수 없는 효과 대상')
        if phase=='turn_start': return self.tick_start(side)
        if phase=='turn_end': return self.tick_end(side)
        raise ValueError('알 수 없는 효과 시점')

    def damage_hp(self,target,amount,kind):
        """Commit mitigated integer damage, returning actual HP lost.

        No RNG, rewards, reflection, or death settlement happens here.
        One-shot barriers precede shields; survival precedes HP loss.
        """
        kind=DamageKind(kind)
        if target not in ('player','enemy') or type(amount) is not int or amount<0:
            raise ValueError('잘못된 피해 대상 또는 수치')
        actor=self.actor(target)
        if not actor or actor['hp']<=0: return 0
        if kind in SHIELDED_DAMAGE:
            barrier=next((st for st in self.actor_statuses(target) if st.get('effect_number')==37 and not st['triggered']),None)
            if barrier and amount:
                actor['shield']=max(actor.get('shield',0),math.floor(self.stats_for(target)['hp']*.15))
                barrier['triggered']=True
            absorbed=min(actor.get('shield',0),amount)
            actor['shield']=actor.get('shield',0)-absorbed; amount-=absorbed
        status_survive=any(st.get('effect_number')==39 for st in self.actor_statuses(target))
        prefix_survive=actor.get('prefix_runtime',{}).get('survive',0)==1
        if amount>=actor['hp'] and (status_survive or prefix_survive):
            flags=self.s['effect_combat_state'][target]
            if not flags['survive_used']:
                flags['survive_used']=True
                kept=min(actor['hp'],max(1,math.floor(self.stats_for(target)['hp']*.01)) if status_survive else 1)
                amount=actor['hp']-kept
        actual=min(actor['hp'],amount); actor['hp']-=actual
        return actual
    def status_label(self,side='player'):
        if side=='enemy' and not self.s['enemy']: return '없음'
        def label(st):
            number=st.get('effect_number')
            text=f"{st.get('name',st.get('stat','효과'))} {st['turns']}턴"+(f" ×{st['stacks']}" if st.get('stacks',1)>1 else '')
            if number in DESCRIPTIONS: text+=f' ({DESCRIPTIONS[number]})'
            if number==37 and st.get('triggered'): text+=' [발동 완료]'
            if number==39 and self.s.get('effect_combat_state',{}).get(side,{}).get('survive_used'): text+=' [사용 완료]'
            return text
        return ', '.join(label(st) for st in self.actor_statuses(side)) or '없음'

    def apply_modifiers(self,d,statuses):
        for st in statuses:
            number=st.get('effect_number')
            for stat,value in BUFF_STATS.get(number,{}).items(): d[stat]*=1+value
            if number==12: d['evasion']+=.08
            if number==13: d['leech']=d.get('leech',0)+.05
            if number==14: d['hp_regen']=d.get('hp_regen',0)+.04
            if number==15: d['reflect']=d.get('reflect',0)+.1
            if number in (23,25): d['evasion']-=EFFECTS[number][2]/100
            if number==20: d['accuracy_down']=d.get('accuracy_down',0)+.15
            if number==21: d['basic_damage_multiplier']=.7
            if number==24: d['damage_taken_multiplier']=1.15
            if number==27: d['mp']*=.85
            if number in (28,32): d['skill_damage_multiplier']=d.get('skill_damage_multiplier',1)*(.8 if number==28 else 1.2)
            if number==29: d['crit']+=.1
            if number==30: d['reduction']=d.get('reduction',0)+.12
            if number in (31,40): d['effect_gold_bonus']=max(d.get('effect_gold_bonus',0),EFFECTS[number][2]/100)
            if number==33: d['defense']*=1.25
            if number==35: d['mp_leech']=.05
            if number==36: d['crit_damage']=d.get('crit_damage',0)+.25
            if number==38: d['counter']=d.get('counter',0)+.15
            if st.get('stat') in d and number is None:
                stat=st['stat']
                if st.get('additive'): d[stat]+=st['value']
                else: d[stat]*=1+st['value']
        from .balance_profile import PROFILE
        for stat,cap in PROFILE['combat']['caps'].items(): d[stat]=max(0,min(cap,d.get(stat,0)))
        for stat in ('atk','defense','hp','mp'): d[stat]=max(1,math.floor(d.get(stat,1)))
        return d

    def derived(self):
        if getattr(self,'_legacy_running',False) or (self.s.get('legacy_pending') and self.s['mode']=='combat'): return LegacyEngine.derived(self)
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
                for effect in skill['effects']:
                    level=self.s['skills'].get(skill['id'],0)
                    bonus=(effect['value']+effect.get('growth',0)*(level-1) if level else 0) if skill.get('phase2') else effect['value']*level
                    d[effect['stat']]*=1+bonus
        return self.apply_modifiers(d,self.s['statuses'])

    def enemy_stats(self):
        enemy=self.s['enemy']; d={k:0 for k in OPTION_STATS}
        d.update(atk=enemy['atk'],defense=enemy['defense'],hp=enemy['max_hp'],mp=30,crit=enemy.get('crit',.05),evasion=enemy['evasion'],leech=enemy.get('leech',0))
        for key,value in enemy.get('prefix_runtime',{}).get('stats',{}).items(): d[key]=d.get(key,0)+value
        if enemy.get('phase2'):
            d['atk']*=enemy.get('phase2_multiplier',1.25)
        return self.apply_modifiers(d,enemy.get('statuses',[]))

    def stats_for(self,side): return self.derived() if side=='player' else self.enemy_stats()

    def apply_status(self,number,target,source='enemy',chance=None):
        if number in EFFECTS:
            if self.s['mode']!='combat' or self.s.get('battle_rules_version',1)<required_version(number): return False
            definition=self.content.by_id[cid(f'EF{number:03}')]; actor=self.actor(target)
            if not actor or actor['hp']<=0: return False
            probability=definition['base_chance_pct']/100 if chance is None else chance
            if self.rng.random()>=max(0,probability-(self.stats_for(target)['status_resist'] if number<=28 else 0)): return False
            statuses=self.actor_statuses(target)
            current=next((s for s in statuses if s.get('effect_number')==number),None)
            if current:
                current.update(stacks=min(EFFECTS[number][4],current['stacks']+1),turns=max(current['turns'],EFFECTS[number][3]),source_atk=self.stats_for(source)['atk'],source_side=source)
            else:
                statuses.append(dict(effect_number=number,effect_id=definition['id'],name=definition['name'],stat='effect',value=0,
                    turns=EFFECTS[number][3],stacks=1,applied_at=self.s['turn'],
                    eligible_turn=self.s['turn']+(0 if target=='enemy' and source=='player' else 1),
                    source_atk=self.stats_for(source)['atk'],source_side=source,runtime_version=required_version(number),
                    **({'triggered':False} if number==37 else {})))
            if target=='player' and number==27: self.clamp()
            self.log(('플레이어' if target=='player' else '적')+' · '+definition['name']); return True
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
            if resource=='hp': amount=self.healing_amount(side,amount)
            if amount: actor[resource]=min(stats[resource],actor[resource]+amount); self.log(f"{side} {resource.upper()} 재생 +{amount}")
        if actor['hp']>0 and any(st.get('effect_number')==34 and st['eligible_turn']<=self.s['turn'] for st in self.actor_statuses(side)):
            amount=self.healing_amount(side,math.floor(stats['hp']*.06)); actor['hp']=min(stats['hp'],actor['hp']+amount); self.log(f'{side} 급속 치유 +{amount}')

    def tick_end(self,side):
        actor=self.actor(side)
        if not actor: return
        statuses=self.actor_statuses(side)
        for st in list(statuses):
            if st.get('effect_number') in EFFECTS:
                if st['eligible_turn']>self.s['turn']: continue
                n=st['effect_number']; operator,_,value,_,_=EFFECTS[n]
                if operator in ('dot_atk_pct','dot_maxhp_pct'):
                    base=st['source_atk'] if operator=='dot_atk_pct' else self.stats_for(side)['hp']
                    amount=max(1,math.floor(base*value/100*st['stacks']))
                    self.damage_hp(side,amount,DamageKind.PERIODIC); self.log(f'{side} {st["name"]} 지속 피해 {amount}')
                st['turns']-=1
                if st['turns']<=0: statuses.remove(st)
                if actor['hp']<=0: break
                continue
            if st.get('applied_at',-1)>=self.s['turn']: continue
            n=st.get('effect_number'); amount=0
            if n in (1,3): amount=max(1,math.floor(self.stats_for(side)['hp']*(.03 if n==1 else .02)*st.get('stacks',1)))
            elif n==2: amount=max(1,math.floor(st['source_atk']*.08*st.get('stacks',1)))
            elif st.get('stat')=='poison': amount=st['value']
            if amount: self.damage_hp(side,amount,DamageKind.PERIODIC); self.log(f'{side} 지속 피해 {amount}')
            st['turns']-=1
            if st['turns']<=0:
                statuses.remove(st)
                if n in (4,5):
                    actor['cc_until']=self.s['turn']+2
                    if n==5: statuses.append(dict(stat='evasion',value=-.05,additive=True,name='빙결 후 둔화',turns=1,applied_at=self.s['turn']))
            if actor['hp']<=0: break

    def tick_status(self):
        if self.s.get('legacy_pending') or getattr(self,'_legacy_running',False): return LegacyEngine.tick_status(self)
        self.actor_phase('player','turn_start'); self.actor_phase('player','turn_end')

    def resolve_deaths(self):
        if self.p['hp']<=0: self.death(); return True
        if self.s['enemy'] and self.s['enemy']['hp']<=0: self.victory(); return True
        return False

    def direct_hit(self,source,mult=1,accuracy=.95,action='attack',secondary=False,penetration=0):
        target='enemy' if source=='player' else 'player'; attacker=self.actor(source); defender=self.actor(target)
        if not attacker or not defender or attacker['hp']<=0 or defender['hp']<=0: return 0
        a=self.stats_for(source); b=self.stats_for(target)
        if attacker.get('prefix_runtime',{}).get('execute') and defender['hp']/b['hp']<=.3:
            mult*=1+attacker['prefix_runtime']['execute']
        if self.rng.random()>=max(.05,accuracy-a.get('accuracy_down',0)-b['evasion']):
            message='공격 빗나감' if source=='player' else '적 공격 회피'; self.log(message); self.s['last_damage' if source=='player' else 'last_counter']=message; return 0
        bonus=a.get('heavy_damage' if action=='heavy' else 'normal_damage',0) if action in ('attack','heavy') else 0
        if action in ('attack','heavy'): mult*=a.get('basic_damage_multiplier',1)
        elif action=='skill': mult*=a.get('skill_damage_multiplier',1)
        amount=max(1,math.floor(a['atk']*mult*(1+bonus)*self.rng.uniform(.9,1.1)-.6*b['defense']*(1-min(1,a.get('penetration',0)+penetration))))
        critical=self.rng.random()<max(0,a['crit']-b.get('crit_resist',0))
        amount=math.floor(amount*(1.5+a.get('crit_damage',0) if critical else 1)*(1+a.get('extra_damage',0))*b.get('damage_taken_multiplier',1)*(1-b.get('reduction',0)))
        amount=math.floor(amount*(1-b.get('skill_reduction',0)))
        if defender.get('guard'): amount=math.floor(amount*.5)
        if target=='player' and self.s['exploration_bonuses'].get('protection'):
            amount=math.floor(amount*.7); self.s['exploration_bonuses'].pop('protection')
        actual=self.damage_hp(target,max(1,amount),DamageKind.COUNTER if secondary else DamageKind.DIRECT)
        if source=='player':
            self.s['stats']['damage']+=actual; self.s['stats']['max_damage']=max(self.s['stats']['max_damage'],actual); self.s['last_damage']=f'적에게 {actual} 피해'
        else: self.s['last_counter']=f'HP -{actual}'
        self.log(self.s['last_damage' if source=='player' else 'last_counter'])
        if not secondary: attacker['hp']=min(a['hp'],attacker['hp']+self.healing_amount(source,math.floor(actual*a.get('leech',0))))
        if not secondary and 'mp' in attacker and a.get('mp_leech'):
            attacker['mp']=min(a['mp'],attacker['mp']+math.floor(actual*a['mp_leech']))
        # Secondary damage never reflects, counters, or leeches again.
        if not secondary and actual:
            reflected=math.floor(actual*b.get('reflect',0))
            if reflected: self.damage_hp(source,reflected,DamageKind.REFLECTED); self.log(f'피해 반사 {reflected}')
            if attacker['hp']>0 and defender['hp']>0 and self.rng.random()<b.get('counter',0): self.direct_hit(target,secondary=True)
        if actual and defender['hp']==0 and attacker['hp']>0 and attacker.get('prefix_runtime',{}).get('kill_heal'):
            amount=math.floor(a['hp']*attacker['prefix_runtime']['kill_heal'])
            attacker['hp']=min(a['hp'],attacker['hp']+amount); self.log(f'접두어 처치 회복 +{amount}')
        return actual

    def hit(self,mult=1,accuracy=.95):
        if getattr(self,'_legacy_running',False): return LegacyEngine.hit(self,mult,accuracy)
        return self.direct_hit('player',mult,accuracy,getattr(self,'_attack_kind','skill'))

    def start_combat(self,kind='normal'):
        self.s['battle_rules_version']=BATTLE_RULES_VERSION
        self.s['effect_combat_state']={side:{'survive_used':False} for side in ('player','enemy')}
        f=self.s['floor']; environment=self.content.by_id[cid(self.content.regions.at(f)['environment_id'])]; boss=None
        if kind=='boss':
            boss=self.content.by_id[cid(self.content.regions.boss_id(f))]; base=self.content.by_id[boss['monster_id']]
        else:
            rows=self.content.regions.monsters(self.content,f)
            base=self.rng.choices(rows,weights=self.content.high_floors.weights(rows,environment,f))[0]
        enemy=copy.deepcopy(base); enemy.update(level=f,kind=kind,exp_multiplier=1,gold_multiplier=1,statuses=[],pattern_index=0,guard=False,shield=0,crit=self.content.catalogue['defaults']['monster_critical_chance'],prefix_ids=[])
        for key,rate in [('hp',.12),('atk',.08),('defense',.06)]: enemy[key]=math.floor(base[key]*(1+rate*(f-1)))
        risk=1+environment['risk_modifier_pct']/100
        if self.s['floor_type']=='FLR004': risk*=1.2
        enemy['hp']=math.floor(enemy['hp']*risk); enemy['atk']=math.floor(enemy['atk']*risk)
        if f>100:
            enemy.update(self.content.high_floors.stats(base,f,environment,boss is not None))
            if self.s['floor_type']=='FLR004':
                for stat in ('hp','atk'): enemy[stat]=math.floor(enemy[stat]*1.2)
            enemy.update(depth_rules_version=1,environment_snapshot=copy.deepcopy(environment),reward_factor=1.27)
        if kind=='elite': enemy['hp']*=2; enemy['atk']=math.floor(enemy['atk']*1.4)
        if boss:
            if f<=100:
                enemy['hp']=math.floor(enemy['hp']*boss['hp_multiplier']); enemy['atk']=math.floor(enemy['atk']*boss['atk_multiplier']); enemy['defense']=math.floor(enemy['defense']*boss['def_multiplier'])
            enemy.update(name=boss['name'],boss_id=boss['id'],effect_id=boss['effect_id'],pattern=boss['pattern'],phase2=False,phase2_hp_pct=boss['phase2_hp_pct'],phase2_multiplier=boss['phase2_multiplier'])
            if boss.get('mechanic'): enemy.update(mechanic=boss['mechanic'],summon_turns=0,healing_suppression=0,suppression_at=0)
        elif kind=='elite' or self.rng.random()<.18:
            count=self.rng.randint(1,2) if kind=='elite' else 1; candidates=[p for p in self.content['prefixes'] if p.get('min_floor',1)<=f]
            for _ in range(count):
                prefix=self.weighted(candidates); candidates=[p for p in candidates if p['category']!=prefix['category']]; enemy['prefix_ids'].append(prefix['id']); enemy['name']=prefix['name']+' '+enemy['name']
                from .prefixes import apply as apply_prefix
                apply_prefix(enemy,prefix,self.content.prefixes)
        enemy['max_hp']=enemy['hp']; self.s.update(enemy=enemy,mode='combat',combat_turn=0,combat_logs=[],legacy_pending=False)
        self.p['shield']=math.floor(self.derived()['hp']*self.derived().get('shield',0)); self.p['guard']=False
        self.s['stats']['battles']+=1; self.log(enemy['name']+' 등장')
        if f>100 and environment.get('floor_effect_id'):
            n=int(environment['floor_effect_id'][2:]); self.apply_status(n,'enemy' if n>=29 else 'player','enemy',.1)

    def counter(self,defend=False):
        if getattr(self,'_legacy_running',False): return LegacyEngine.counter(self,defend)
        enemy=self.s['enemy']; self.actor_phase('enemy','turn_start')
        enemy['guard']=False
        if enemy.get('phase2_hp_pct') and not enemy['phase2'] and enemy['hp']/enemy['max_hp']<=enemy['phase2_hp_pct']/100:
            enemy['phase2']=True; self.log('보스 2단계 · 공격력 증가')
        blocked=self.action_blocked('enemy',roll=True)
        action=enemy['pattern'][enemy['pattern_index']%len(enemy['pattern'])]
        if blocked: self.log('적 행동 불가')
        else:
            enemy['pattern_index']+=1
            if action in ('special','heal','debuff') and any(st.get('effect_number')==6 for st in enemy['statuses']):
                action='attack'; self.log('적 침묵 · 특수공격 대신 일반 공격')
            if action=='defend': enemy['guard']=True; self.log('적 방어 · 다음 피격 피해 50% 감소')
            elif action=='heal':
                amount=math.floor(enemy['max_hp']*.04); enemy['hp']=min(enemy['max_hp'],enemy['hp']+amount); self.log(f'보스 회복 +{amount}')
            elif action=='debuff':
                number=int(enemy['effect_id'][2:]); target='enemy' if 10<=number<=15 or 29<=number<=40 else 'player'
                self.apply_status(number,target,'enemy',.6); self.log('보스 강화 시도' if target=='enemy' else '보스 약화 시도')
            else:
                mechanic=enemy.get('mechanic') if action=='special' or (action=='heavy' and 'special' not in enemy['pattern']) else None
                if mechanic=='보호막 파괴': self.p['shield']=0; self.log('보스 · 보호막 파괴')
                mult=2 if mechanic=='단일 강타' else self.content.catalogue['defaults']['special_damage'] if action=='special' else 1.5 if action=='heavy' else 1
                damage=self.direct_hit('enemy',mult,enemy['accuracy']*(.85 if action=='heavy' else 1),action='skill' if action=='special' else action)
                if self.resolve_deaths(): return
                if mechanic=='연속 공격':
                    self.direct_hit('enemy',.7,enemy['accuracy'],action='skill',secondary=True)
                    if self.resolve_deaths(): return
                elif mechanic=='특수 소환':
                    enemy['summon_turns']=2; enemy['shield']=max(enemy['shield'],math.floor(enemy['max_hp']*.08)); self.log('방패 소환체 · 보호막과 2회 보조 공격')
                elif mechanic=='회복 억제':
                    enemy.update(healing_suppression=2,suppression_at=self.s['turn']); self.log('회복 억제 · 이후 2행동 HP 회복 50% 감소')
                elif mechanic=='추가 상태이상': self.apply_status(24,'player','enemy',.3)
                if damage:
                    for number in enemy.get('on_hit_effects',[]): self.apply_status(number,'player',chance=.15)
                    for hit in enemy.get('prefix_runtime',{}).get('hits',[]): self.apply_status(hit['effect'],'player',chance=hit['chance'])
                if enemy.get('effect_id') and (action=='special' or 'special' not in enemy['pattern']):
                    number=int(enemy['effect_id'][2:]); target='enemy' if 10<=number<=15 or 29<=number<=40 else 'player'
                    from .monster_roles import effect_chance
                    if target=='enemy' or damage: self.apply_status(number,target,chance=effect_chance(enemy))
            if not blocked and enemy.get('summon_turns',0)>0:
                enemy['summon_turns']-=1; self.direct_hit('enemy',.25,enemy['accuracy'],action='skill',secondary=True)
                if self.resolve_deaths(): return
        if not self.resolve_deaths(): self.actor_phase('enemy','turn_end'); self.resolve_deaths()

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
            self.require(self.p['mp']>=self.skill_mp_cost(skill),'MP가 부족합니다.')
        if action=='potion': self.validate_consumable(key)
        self.s['turn']+=1; self.s['combat_turn']+=1; self.actor_phase('player','turn_start')
        blocked=self.action_blocked('player',roll=True)
        self.p['guard']=action=='defend' and not blocked
        if blocked: self.log('행동 불가 · 자원은 소모하지 않습니다.')
        elif action in ('attack','heavy'):
            self._attack_kind=action
            try: self.hit(1.5 if action=='heavy' else 1,.8 if action=='heavy' else .95)
            finally: self._attack_kind='skill'
        elif action=='skill': self.p['mp']-=self.skill_mp_cost(skill); self.effects(skill['effects'],self.s['skills'][key])
        elif action=='potion': self.consume(key)
        elif action=='defend': self.log('방어')
        elif action=='flee':
            if self.rng.random()<.6:
                self.s.update(mode='explore',enemy=None); self.s['stats']['escapes']+=1; self.actor_phase('player','turn_end'); self.log('도주 성공')
                if self.p['hp']<=0: self.death()
                return not blocked
            self.log('도주 실패')
        if self.resolve_deaths(): return not blocked
        self.actor_phase('player','turn_end')
        if self.s.get('enemy') and self.s['enemy'].get('healing_suppression',0)>0 and self.s['enemy']['suppression_at']<self.s['turn']: self.s['enemy']['healing_suppression']-=1
        if not self.resolve_deaths(): self.counter(action=='defend')
        return not blocked

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
        elif 21<=number<=25: self.effects(item['effects'])
        elif 36<=number<=40:
            targets=set(item['dispel_targets']); self.s['statuses']=[st for st in self.s['statuses'] if st.get('effect_id') not in {cid(key) for key in targets}]
        elif number in (9,10,12): self.apply_status({9:10,10:11,12:12}[number],'player','player',1)
        elif number==11:
            self.s['statuses']=[st for st in self.s['statuses'] if st.get('name')!='치명타 물약']
            self.s['statuses'].append(dict(stat='crit',value=.1,additive=True,name='치명타 물약',turns=3,applied_at=self.s['turn']))
        elif number in (13,14,15,16):
            version=self.s.get('battle_rules_version',1)
            remove={13:{1,19} if version>=2 else {1},14:{2},15:{9},16:set(range(1,10))|({n for n in EFFECTS if n<=28 and required_version(n)<=version})}[number]
            self.s['statuses']=[st for st in self.s['statuses'] if st.get('effect_number') not in remove and not (number in (13,16) and st.get('stat')=='poison') and not (number==16 and st.get('value',0)<0)]
        elif number==17: self.return_to_base()
        elif number==18: self.s['exploration_bonuses']['treasure_pp']=10
        elif number==19: self.s['exploration_bonuses']['rarity_pp']=self.content.catalogue['defaults']['lucky_charm_pp']
        elif number==20: self.s['exploration_bonuses']['protection']=True

    def effects(self,effects,level=1):
        if getattr(self,'_legacy_running',False): return LegacyEngine.effects(self,effects,level)
        for effect in effects:
            if effect['type']=='heal_hp' and self.s.get('enemy',{} ) and self.s['enemy'].get('healing_suppression',0):
                value=effect['value']+effect.get('growth',0)*(level-1)
                amount=math.floor(value*self.derived()['hp']) if effect.get('fraction') else int(value)
                amount=self.healing_amount('player',amount); self.p['hp']+=amount; self.clamp(); self.log(f'HP +{amount}')
            elif effect['type']=='damage':
                for _ in range(effect.get('hits',1)):
                    if not self.s['enemy'] or self.s['enemy']['hp']<=0 or self.p['hp']<=0: break
                    self.hit(effect['value']+effect.get('growth',0)*(level-1))
            else: LegacyEngine.effects(self,[effect],level)

    def victory(self):
        if getattr(self,'_legacy_running',False): return LegacyEngine.victory(self)
        enemy=self.s['enemy']; kind=enemy['kind']; floor=self.s['floor']; d=self.derived(); environment=self.environment()
        self.s['stats']['wins']+=1; self.s['stats'][kind]+=1
        reward=enemy.get('reward_factor',1+environment['reward_modifier_pct']/100)
        from .balance_profile import PROFILE
        effect_gold=max(d.get('effect_gold_bonus',0),self.enemy_stats().get('effect_gold_bonus',0))
        gold_bonus=min(PROFILE['combat']['caps']['gold_bonus'],d['gold_bonus']+effect_gold)
        gold=math.floor((10+3*floor)*{'normal':1,'elite':3,'boss':10}[kind]*enemy['gold_multiplier']*reward*(1+gold_bonus)*(1.3 if self.s['floor_type']=='FLR004' else 1))
        xp=math.floor((25+8*floor)*{'normal':1,'elite':2,'boss':5}[kind]*enemy['exp_multiplier']*reward*(1+d['exp_bonus'])*(.2 if self.p['level']-enemy['level']>=10 else 1))
        self.gain_gold(gold); self.gain_exp(xp)
        from .balance_profile import PROFILE
        prefix=enemy.get('prefix_runtime',{})
        chance=min(1,(PROFILE['drops']['equipment_chance'][kind]+d['drop_bonus'])*(1+prefix.get('equipment_drop',0)))
        dropped=(kind=='elite' and self.s['elite_misses']>=10) or self.rng.random()<chance
        if dropped: self.award_equipment(rarity_bonus=prefix.get('rarity_pp',0))
        if kind=='elite': self.s['elite_misses']=0 if dropped else self.s['elite_misses']+1
        material_chance=min(1,(enemy.get('drop_material_pct',20)/100 if enemy.get('depth_rules_version') else .2)*(1+prefix.get('material_drop',0)))
        if self.rng.random()<material_chance and enemy.get('material_id'): self.grant_item(cid(enemy['material_id']),1)
        if self.rng.random()<.05:
            tier=min(4,((floor-1)%100)//20); pool=[r for r in self.content['materials'] if (int(r['source_id'][3:])-1)%5<=tier and (enemy.get('depth_rules_version') or int(r['source_id'][3:])<=20)]; self.grant_item(self.rng.choice(pool)['id'],1)
        if kind=='boss':
            self.s['boss_done']=True; self.grant_item(cid('MAT018'),1)
            if enemy.get('depth_rules_version') and enemy.get('material_id'): self.grant_item(cid(enemy['material_id']),2)
            if floor not in self.s['boss_first']: self.grant_item(cid('MAT016'),3); self.s['boss_first'].append(floor)
        elif kind=='elite' and self.rng.random()<.2: self.grant_item(cid('MAT016'),1)
        for resource in ('hp','mp'): self.p[resource]=min(self.derived()[resource],self.p[resource]+math.floor(self.derived()[resource]*d.get('kill_'+resource,0)))
        self.log(f'승리 · 골드 +{gold} / 경험치 +{xp}')
        self.s.update(mode='explore',enemy=None); self.s['progress']+=1; self.p['guard']=False; self.p['shield']=0
