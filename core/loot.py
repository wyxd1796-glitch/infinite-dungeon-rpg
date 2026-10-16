"""Catalogue equipment, currency, stacks and persistent pending rewards."""
import copy
import math
import uuid
from .catalogue import cid, PERCENT_STATS, OPTION_NAMES
from .legacy_engine import GameEngine as LegacyEngine, STAT_NAMES

class LootMixin:
    def equipment_base_stats(self,base,level):
        if not base.get('catalogue'): return LegacyEngine.equipment_base_stats(base,level)
        stat=base['stat']; value=base['base_bonus']
        if stat=='atk': value+=math.floor(3+1.5*level)
        if stat in PERCENT_STATS: value/=100
        return {stat:value}

    def gear_stats(self,item):
        if not item.get('catalogue'): return LegacyEngine.gear_stats(self,item)
        result={}
        for key,value in item['rolled_stats'].items():
            bonus=value*.1*item['enhance']
            result[key]=value+(round(bonus,6) if key in PERCENT_STATS else math.floor(bonus))
        for affix in item['affixes']: result[affix['stat']]=result.get(affix['stat'],0)+affix['value']
        return result

    def rarity_weights(self,luck=None,bonus=None):
        d=self.derived(); luck=d['luk'] if luck is None else luck
        extra=min(8,max(0,luck)*.04)+(d.get('rarity_bonus',0)*100 if bonus is None else bonus)
        extra=min(85,max(0,extra)); weights=[60.,25.,10.,4.,1.]
        for i in (0,1): weights[i]-=extra*weights[i]/85
        for i in (2,3,4): weights[i]+=extra*weights[i]/15
        return weights

    def generate_equipment(self,base_id=None):
        if base_id and not self.content.by_id[base_id].get('catalogue'):
            # Compatibility purchases are not offered, but old developer fixtures remain usable.
            base=self.content.by_id[base_id]
        else:
            candidates=[r for r in self.content['equipment'] if r.get('min_floor',1)<=self.s['floor']]
            self.require(bool(candidates),'출현 가능한 장비가 없습니다.')
            base=self.content.by_id[base_id] if base_id else self.rng.choice(candidates)
        level=max(1,self.s['floor']+self.rng.randint(-2,2))
        weights=self.rarity_weights(bonus=self.derived().get('rarity_bonus',0)*100+self.s['exploration_bonuses'].get('rarity_pp',0))
        self.s['exploration_bonuses'].pop('rarity_pp',None)
        rarities=list(self.content.balance['rarities']); rarity=self.rng.choices(rarities,weights=weights)[0]
        candidates=[o for o in self.content['affixes'] if base['slot'] in o['slots'] and o['category'] in base.get('option_pool',[])]; affixes=[]
        for _ in range(min(rarities.index(rarity),len(candidates))):
            option=self.weighted(candidates); candidates.remove(option)
            scale=(level//10)*option['per_10_levels']; lo=option['min_value']+scale; hi=option['max_value']+scale
            value=self.rng.randint(math.ceil(lo),math.floor(hi)) if option['unit']=='점' else round(self.rng.uniform(lo,hi)/100,4)
            affixes.append(dict(id=option['id'],stat=option['stat'],name=option['name'],value=value))
        return dict(instance_id=str(uuid.UUID(int=self.rng.getrandbits(128))),base_id=base['id'],name=base['name'],slot=base['slot'],level=level,rarity=rarity,enhance=0,rolled_stats=self.equipment_base_stats(base,level),affixes=affixes,origin_floor=self.s['floor'],catalogue=bool(base.get('catalogue')),sell_base=base.get('sell_price',1))

    def queue_reward(self,reward):
        reward=copy.deepcopy(reward); reward['pending_id']=str(uuid.UUID(int=self.rng.getrandbits(128)))
        self.s['pending_loot'].append(reward); self.log('가방 또는 중첩 한도 초과 · 가방의 획득 대기에서 받으세요.')

    def grant_item(self,key,n):
        self.require(isinstance(n,int) and n>0,'획득 수량 오류')
        definition=self.content.by_id[key]; current=self.s['items'].get(key,0); cap=definition.get('stack_limit',999)
        room=max(0,cap-current) if current>0 or self.bag_used()<30 else 0; received=min(n,room)
        if received: self.s['items'][key]=current+received
        if n>received: self.queue_reward({'kind':'item','item_id':key,'quantity':n-received})
        self.s['last_item']=definition['name']; return received==n

    def award_equipment(self):
        item=self.generate_equipment(); self.s['stats']['equipment']+=1; self.s['stats']['legendary']+=int(item['rarity']=='전설')
        if self.bag_used()>=30: self.queue_reward({'kind':'equipment','equipment':item})
        else: self.s['inventory'][item['instance_id']]=item; self.s['bag'].append(item['instance_id'])
        self.s['last_item']=self.item_name(item); self.log('획득: '+self.item_name(item))

    def pending_action(self,key,discard=False):
        self.require(self.s['mode'] not in ('combat','event'),'전투 또는 이벤트를 먼저 해결하세요.')
        row=next((r for r in self.s['pending_loot'] if r['pending_id']==key),None); self.require(row is not None,'획득 대기 항목이 없습니다.')
        if discard: self.s['pending_loot'].remove(row); self.log('획득 대기 아이템 버리기'); return
        if row['kind']=='equipment':
            self.require(self.bag_used()<30,'가방이 가득 찼습니다.'); item=row['equipment']; self.s['inventory'][item['instance_id']]=item; self.s['bag'].append(item['instance_id']); self.s['pending_loot'].remove(row)
        else:
            item_key=row['item_id']; definition=self.content.by_id.get(item_key); self.require(definition is not None,'원형 팩을 먼저 복원하세요.')
            current=self.s['items'].get(item_key,0); amount=min(row['quantity'],definition.get('stack_limit',999)-current)
            self.require(amount>0 and (current>0 or self.bag_used()<30),'가방 또는 중첩 한도가 부족합니다.')
            self.s['items'][item_key]=current+amount; row['quantity']-=amount
            if row['quantity']==0: self.s['pending_loot'].remove(row)
        self.log('획득 대기 수령 완료')

    def sell_price(self,item):
        if not item.get('catalogue'): return LegacyEngine.sell_price(self,item)
        return math.floor(item['sell_base']*(1+.1*item['enhance']+.05*len(item['affixes'])))

    def equipment_price(self,key=None):
        return self.content.by_id[key]['price'] if key else LegacyEngine.equipment_price(self)

    def shop_stock(self):
        return [self.content.by_id[k] for k in self.s['shop_stock'] if k in self.content.by_id]

    def refresh_shop(self):
        # Stable list for a visit, refreshed only at a genuine return/initial migration.
        self.s['shop_stock']=[r['id'] for r in self.content['items'] if r.get('catalogue') and (r['category']=='소비품' or r.get('source_id')=='MAT016')]
        self.s['shop_stock'] += [r['id'] for r in self.content['equipment'] if r['min_floor']<=self.s['highest']]

    def buy(self,key,quantity):
        self.require(self.s['mode']=='base','거점에서만 구매할 수 있습니다.')
        self.require(key in self.s['shop_stock'],'해금되지 않았거나 판매하지 않는 상품입니다.')
        item=self.content.by_id[key]; equipment='slot' in item; cost=item['price']*quantity
        self.require(self.p['gold']>=cost,'골드가 부족합니다.')
        slots=quantity if equipment else int(self.s['items'].get(key,0)==0)
        self.require(self.bag_used()+slots<=30,'가방이 가득 찼습니다.')
        if not equipment: self.require(self.s['items'].get(key,0)+quantity<=item['stack_limit'],'중첩 한도를 초과합니다.')
        self.p['gold']-=cost
        if equipment:
            # Shop gear uses unlocked depth rather than a lower previously visited floor.
            floor=self.s['floor']; self.s['floor']=self.s['highest']
            try:
                for _ in range(quantity):
                    gear=self.generate_equipment(key); self.s['inventory'][gear['instance_id']]=gear; self.s['bag'].append(gear['instance_id'])
            finally: self.s['floor']=floor
        else: self.grant_item(key,quantity)
        self.log('구매 완료')

    def enhance_cost(self,item):
        n=item['enhance']+1
        return round(100+20*item['level']+75*n**1.4),max(1,math.ceil(n/3)),1 if n<=3 else .8 if n<=6 else .6 if n<=9 else .4 if n<=12 else .2

    def upgrade_materials(self):
        return [(r['id'],r['name'],r.get('upgrade_units',1)) for r in self.content['items'] if r.get('upgrade_units',0)>0 or r['id']=='base.item.stone']

    def enhance(self,key,material):
        self.require(self.s['mode']=='base','거점에서만 강화할 수 있습니다.')
        self.require(key in self.s['bag']+list(self.s['equipped'].values()),'강화할 장비를 선택하세요.')
        item=self.s['inventory'][key]; self.require(item['base_id'] in self.content.by_id and item['enhance']<15,'미확인 장비 또는 최대 강화입니다.')
        values={k:units for k,_,units in self.upgrade_materials()}; self.require(material in values,'강화 재료를 선택하세요.')
        cost,stones,chance=self.enhance_cost(item); count=math.ceil(stones/values[material])
        self.require(self.p['gold']>=cost and self.s['items'].get(material,0)>=count,'골드 또는 강화 재료가 부족합니다.')
        self.p['gold']-=cost; self.s['items'][material]-=count; success=self.rng.random()<chance; item['enhance']+=int(success)
        self.s['last_enhance']='강화 성공' if success else '강화 실패 · 단계 유지'; self.log(self.s['last_enhance'])

    def shop_description(self,key):
        item=self.content.by_id[key]
        if not item.get('catalogue'): return LegacyEngine.shop_description(self,key)
        if 'slot' in item:
            low=max(1,self.s['highest']-2); high=self.s['highest']+2; lo=self.equipment_base_stats(item,low); hi=self.equipment_base_stats(item,high)
            lines=[f"착용 부위: {item['slot']} / {item['subtype']}",f"해금: {item['min_floor']}층 · 장비 레벨 {low}~{high}"]
            for stat,value in lo.items():
                def fmt(v): return f'{v*100:g}%p' if stat in PERCENT_STATS else f'{v:g}'
                lines.append(f'{STAT_NAMES[stat]} +{fmt(value)}'+(f'~{fmt(hi[stat])}' if hi[stat]!=value else ''))
            lines+=['추가 옵션: '+', '.join(item['option_pool']),'구매 시 레벨·등급·옵션이 무작위 결정됩니다. 같은 옵션은 한 장비에 중복되지 않습니다.']
            return '\n'.join(lines)
        if item['category']=='소비품':
            timing='전투 중 1턴 및 생존한 적 반격. 탐험 중 1턴, 진행도 불변.' if item['consumes_turn'] else '턴과 탐험 진행도를 소모하지 않습니다.'
            return f"{item['description']}\n사용: {' / '.join(item['use_context'])}\n{timing} 최대 {item['stack_limit']}개 중첩."
        return f"{item['description']}\n획득: {item['source']}\n최대 {item['stack_limit']}개 중첩."+(f"\n강화석 {item['upgrade_units']}개분 대체." if item['upgrade_units'] else '\n이번 버전에서는 보관·판매에 사용합니다.')

    def available_items(self,category):
        return [r for r in self.content['items'] if r['category']==category and (r.get('catalogue') or self.s['items'].get(r['id'],0)>0)]

    def automatic_potion(self):
        candidates=[]
        for item in self.available_items('소비품'):
            if self.s['items'].get(item['id'],0)<=0 or 'combat' not in item.get('contexts',['combat']): continue
            heals=[x['value'] for x in item['effects'] if x['type']=='heal_hp']
            if heals: candidates.append((min(heals),item['id']))
        return min(candidates)[1] if candidates else None
