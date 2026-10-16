"""Phase-two skills and choice events; all mutations use the engine transaction."""
import copy
import math


class Phase2Mixin:
    def skill_reason(self,key,learning=False):
        skill=self.content.by_id.get(key,{})
        if key not in self.s['skills'] or 'kind' not in skill: return '알 수 없는 스킬'
        if learning:
            if self.s.get('event_result') or self.s['mode'] in ('combat','event'): return '전투·이벤트를 먼저 완료하세요'
            if self.p['level']<skill.get('unlock_level',1): return f"레벨 {skill['unlock_level']}에 해금"
            if self.s['skills'][key]>=skill['max_level']: return '최대 레벨'
            if self.p['skill_points']<1: return '스킬 포인트 부족'
            return ''
        if self.s.get('event_result'): return '이벤트 결과를 먼저 확인하세요'
        if self.s['mode']!='combat': return '전투 중 사용 가능'
        if skill['kind']!='active': return '패시브 스킬'
        if self.p['level']<skill.get('unlock_level',1): return f"레벨 {skill['unlock_level']}에 해금"
        if self.s['skills'].get(key,0)<1: return '미학습'
        if skill.get('phase2') and (self.s.get('phase2_legacy_combat') or self.s.get('legacy_pending')): return '이전 버전 전투 종료 후 사용 가능'
        if any(st.get('effect_number')==6 for st in self.s['statuses']): return '침묵 상태'
        cooldown=self.s.get('skill_cooldowns',{}).get(key,0)
        if cooldown: return f'재사용 대기 {cooldown}행동'
        if self.p['mp']<skill['mp']: return 'MP 부족'
        return ''

    def skill_label(self,skill):
        level=self.s['skills'].get(skill['id'],0)
        state=f"잠금 Lv.{skill['unlock_level']}" if self.p['level']<skill.get('unlock_level',1) else '미학습' if not level else f'Lv.{level}'
        return f"{skill['name']} · {state}"

    def skill_description(self,key):
        skill=self.content.by_id[key]; level=self.s['skills'].get(key,0)
        if skill.get('description'): return skill['description']
        effect=skill['effects'][0]
        if skill['kind']=='passive': return f"{effect['stat']} +{effect['value']*level:.0%}"
        value=effect['value']+effect.get('growth',0)*(max(1,level)-1)
        return ('공격력 ' if effect['type']=='damage' else '최대 HP ')+f"{value:.0%}"+(f" ×{effect['hits']}" if effect.get('hits',1)>1 else '')

    def auto_skill_allowed(self,skill):
        if self.skill_reason(skill['id']): return False
        rule=skill.get('auto_condition','heal70' if skill['effects'][0]['type']=='heal_hp' else 'always')
        if rule=='heal70': return self.p['hp']/self.derived()['hp']<=.7
        if rule=='emergency': return self.p['hp']/self.derived()['hp']<=.5 or self.has_treatable_status()
        if rule=='execute': return self.s['enemy']['hp']/self.s['enemy']['max_hp']<=.3
        if rule=='unbuffed': return skill['id'] not in self.s['skill_buffs']
        if rule=='unshielded': return self.p.get('shield',0)<=0
        return True

    def has_treatable_status(self):
        return any(st.get('effect_number') in (1,2,3) or st.get('stat')=='poison' for st in self.s['statuses'])

    def derived(self):
        d=super().derived()
        for buff in self.s.get('skill_buffs',{}).values():
            if buff['kind']=='attack': d['atk']=max(1,math.floor(d['atk']*(1+buff['value'])))
            elif buff['kind']=='reduction': d['skill_reduction']=buff['value']
        return d

    def status_label(self,side='player'):
        label=super().status_label(side)
        extra=[f"{b['name']} {b['remaining']}행동" for b in self.s.get('skill_buffs',{}).values()] if side=='player' else []
        return ', '.join(([label] if label!='없음' else [])+extra) or '없음'

    def clear_skill_combat(self):
        self.s.update(skill_cooldowns={},skill_buffs={},phase2_legacy_combat=False)
        self.p['shield']=0

    def start_combat(self,kind='normal'):
        self.clear_skill_combat()
        return super().start_combat(kind)

    def victory(self):
        result=super().victory(); self.clear_skill_combat(); return result

    def death(self):
        result=super().death(); self.clear_skill_combat(); return result

    def battle(self,action,key=None):
        if action=='skill':
            reason=self.skill_reason(key); self.require(not reason,reason)
        before=self.s['turn']; cooldowns=dict(self.s['skill_cooldowns'])
        blocked=any(st.get('effect_number') in (4,5) for st in self.s['statuses'])
        result=super().battle(action,key)
        if self.s['mode']!='combat': self.clear_skill_combat()
        elif self.s['turn']>before:
            self.s['skill_cooldowns']={k:v-1 for k,v in cooldowns.items() if v>1}
            if action=='skill' and not blocked:
                wait=self.content.by_id[key].get('cooldown_turns',0)
                if wait: self.s['skill_cooldowns'][key]=wait
            for k,b in list(self.s['skill_buffs'].items()):
                if b['kind']=='attack' and b['applied_at']<self.s['turn']:
                    b['remaining']-=1
                    if not b['remaining']: del self.s['skill_buffs'][k]
        if action=='skill' and not blocked and self.s['turn']>before:
            usage=self.s.setdefault('skill_usage',{}); usage[key]=usage.get(key,0)+1
        return result

    def counter(self,defend=False):
        result=super().counter(defend)
        for k,b in list(self.s.get('skill_buffs',{}).items()):
            if b['kind']=='reduction':
                b['remaining']-=1
                if not b['remaining']: del self.s['skill_buffs'][k]
        return result

    def effects(self,effects,level=1):
        for raw in effects:
            e=copy.deepcopy(raw); value=e.get('value',0)+e.get('growth',0)*(level-1); kind=e['type']
            if e.get('floor_scaled'): value=math.floor(value*self.s['floor']); e.update(value=value,growth=0)
            if kind=='tactical_damage':
                if e.get('execute_threshold') and self.s['enemy']['hp']/self.s['enemy']['max_hp']<=e['execute_threshold']: value*=e['execute_multiplier']
                self.direct_hit('player',value,action='skill',penetration=e.get('penetration',0))
            elif kind=='skill_buff':
                self.s['skill_buffs'][e['skill_id']]=dict(kind=e['buff'],value=value,remaining=e['duration'],applied_at=self.s['turn'],name=self.content.by_id[e['skill_id']]['name'])
                self.log(self.content.by_id[e['skill_id']]['name']+' 적용')
            elif kind=='skill_shield':
                amount=math.floor(self.derived()['hp']*value); self.p['shield']=max(self.p.get('shield',0),amount); self.log(f'보호막 {amount}')
            elif kind=='cleanse':
                self.s['statuses']=[s for s in self.s['statuses'] if s.get('effect_number') not in (1,2,3) and s.get('stat')!='poison']; self.log('중독·화상·출혈 제거')
            elif kind=='exploration_bonus':
                self.s['exploration_bonuses'][e['bonus']]=value; self.log('다음 탐험 보물 확률 +10%p' if e['bonus']=='treasure_pp' else '다음 장비 희귀 등급 확률 +5%p')
            elif kind=='catalogue_item':
                self.grant_item('catalogue.v3.'+e['catalogue_item'],int(value)); self.log(self.content.by_id['catalogue.v3.'+e['catalogue_item']]['name']+f' {int(value)}개 획득')
            elif kind=='phase2_combat': self.start_combat(e['encounter'])
            elif kind=='hurt' and e.get('fraction'):
                amount=math.floor(self.derived()['hp']*value); self.p['hp']=max(0,self.p['hp']-amount); self.log(f'HP -{amount}')
            else: super().effects([e],level)
            if self.p['hp']<=0: break

    def event_option(self,option):
        """Pure preview shared by UI, validation and event resolution."""
        opt=copy.deepcopy(option); opt['cost']=math.floor(opt.get('cost',0)+opt.get('gold_per_floor',0)*self.s['floor'])
        opt['hp_cost_amount']=math.floor(opt.get('hp_cost',0)*self.derived()['hp'])
        if opt.get('shop_potion'):
            candidates=[r for r in self.content['consumables'] if r['id'] in self.s['shop_stock'] and any(e['type']=='heal_'+opt['shop_potion'] for e in r['effects'])]
            if candidates:
                item=max(candidates,key=lambda r:r['effects'][0]['value']); opt['cost']=math.floor(item['price']*.8)
                opt['outcomes']=[dict(weight=100,effects=[dict(type='catalogue_item',catalogue_item=item['source_id'],value=1)])]
                opt['description']=f"{item['name']} 1개 / 비용 {opt['cost']} G / 성공 100%"
            else: opt['unavailable']='해금된 물약이 없습니다'
        return opt

    def event_option_reason(self,option):
        opt=self.event_option(option)
        if opt.get('unavailable'): return opt['unavailable']
        if self.p['gold']<opt['cost']: return '골드 부족'
        if opt['hp_cost_amount'] and self.p['hp']<=opt['hp_cost_amount']: return 'HP 비용을 지불하면 사망합니다'
        if opt.get('cost_item') and self.s['items'].get('catalogue.v3.'+opt['cost_item'],0)<1: return '필요한 아이템 부족'
        if not all(self.condition(c) for c in opt.get('conditions',[])): return '선택 조건 미충족'
        return ''

    def event_option_description(self,option):
        opt=self.event_option(option); text=opt.get('description','')
        if opt['cost']: text+=f"\n지불 골드: {opt['cost']} G"
        if opt['hp_cost_amount']: text+=f"\n지불 HP: {opt['hp_cost_amount']}"
        if opt.get('cost_item'): text+='\n필요 아이템: '+self.content.by_id['catalogue.v3.'+opt['cost_item']]['name']+' 1개'
        return text or '비용 없음'

    def resolve_event(self,**args):
        if not (self.s.get('event') or {}).get('phase2'): return super().resolve_event(**args)
        self.require(self.s['mode']=='event','진행 중인 이벤트가 없습니다.')
        event=copy.deepcopy(self.s['event']); index=args.get('index',0)
        self.require(type(index) is int and 0<=index<len(event['options']),'잘못된 선택지입니다.')
        opt=self.event_option(event['options'][index]); reason=self.event_option_reason(event['options'][index]); self.require(not reason,reason)
        self.p['gold']-=opt['cost']; self.p['hp']-=opt['hp_cost_amount']
        if opt.get('cost_item'): self.s['items']['catalogue.v3.'+opt['cost_item']]-=1
        self.s.update(mode='explore',event=None); self.s['turn']+=1; self._event_messages=[]
        try:
            if opt['cost']: self.log(f"골드 -{opt['cost']}")
            if opt['hp_cost_amount']: self.log(f"HP -{opt['hp_cost_amount']}")
            if opt.get('cost_item'): self.log(self.content.by_id['catalogue.v3.'+opt['cost_item']]['name']+' 1개 소비')
            outcome=self.weighted(opt['outcomes']); self.effects(outcome['effects'])
            if self.p['hp']<=0: self.death()
            elif self.s['mode']!='combat': self.s['progress']+=1
            self.s['event_result']=dict(title=event['title'],description=event['description'],choice=opt['label'],text='\n'.join(self._event_messages) or '보상·피해 없이 지나갔습니다.',resolved=True)
        finally: self._event_messages=None

    def _execute(self,action,**args):
        if action in ('upgrade_skill','reset_skills'):
            self.require(not self.s.get('event_result'),'이벤트 결과를 먼저 확인하세요.')
            if action=='upgrade_skill':
                key=args.get('key'); reason=self.skill_reason(key,learning=True); self.require(not reason,reason)
                self.p['skill_points']-=1; self.s['skills'][key]+=1; self.log('스킬 학습·강화 완료')
            else:
                self.require(self.s['mode']=='base','거점에서만 재분배할 수 있습니다.')
                refund=0
                for skill in self.content['skills']:
                    key=skill['id']; initial=skill.get('initial_level',1); level=self.s['skills'].get(key,initial)
                    refund+=max(0,level-initial); self.s['skills'][key]=min(level,initial)
                self.p['skill_points']+=refund; self.log(f'스킬 재분배 · {refund} P 환급')
            self.clamp(); return
        if action=='skill_auto':
            key=args.get('key'); field=args.get('field'); value=args.get('value')
            self.require(key in self.s['skill_auto'],'잘못된 스킬 설정')
            self.require((field=='enabled' and type(value) is bool) or (field=='priority' and type(value) is int and 1<=value<=9),'잘못된 자동 스킬 값')
            self.s['skill_auto'][key][field]=value; return
        return super()._execute(action,**args)
