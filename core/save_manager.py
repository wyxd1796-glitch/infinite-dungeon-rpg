import json
import os
import shutil
import hashlib
import math
from pathlib import Path
from datetime import datetime
from .phase3_effects import EFFECTS, validate_status

class SaveManager:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True,exist_ok=True)
        self.notice = ''

    def path(self, slot):
        if slot not in (1,2,3): raise ValueError('저장 슬롯은 1~3입니다')
        return self.directory/f'slot_{slot}.json'

    @staticmethod
    def validate(state):
        if type(state.get('battle_rules_version',1)) is not int or state.get('battle_rules_version',1) not in (1,2,3): raise ValueError('미지원 전투 규칙 버전')
        if state.get('battle_rules_version')==3:
            flags=state.get('effect_combat_state')
            if not isinstance(flags,dict) or set(flags)!={'player','enemy'} or any(not isinstance(v,dict) or type(v.get('survive_used')) is not bool for v in flags.values()): raise ValueError('전투 생존 기록 오류')
        if state.get('save_schema_version') not in (1,2,3): raise ValueError('지원하지 않는 저장 버전')
        for key in ('player','inventory','equipped','bag','storage','items','stats','settings','skills','mode','floor','highest','progress'):
            if key not in state: raise ValueError(f'저장 필드 누락: {key}')
        if state['mode'] not in ('base','explore','combat','event'): raise ValueError('잘못된 진행 상태')
        if state['mode']=='combat' and not state.get('enemy'): raise ValueError('전투 데이터 누락')
        if state['mode']=='event' and not state.get('event'): raise ValueError('이벤트 데이터 누락')
        player=state['player']
        for key in ('hp','mp','gold','exp','points','skill_points','level'):
            if not isinstance(player.get(key),int) or player[key]<0 or (key=='level' and player[key]<1): raise ValueError(f'잘못된 캐릭터 수치: {key}')
        if not isinstance(player.get('name'),str) or not isinstance(player.get('attributes'),dict): raise ValueError('캐릭터 정보 누락')
        if any(not isinstance(player['attributes'].get(k),int) or player['attributes'][k]<0 for k in ('str','dex','vit','int','luk')): raise ValueError('능력치 정보 누락')
        for key in ('inventory','equipped','items','stats','settings','skills'):
            if not isinstance(state[key],dict): raise ValueError(f'잘못된 저장 형식: {key}')
        for key in ('bag','storage'):
            if not isinstance(state[key],list): raise ValueError(f'잘못된 저장 형식: {key}')
        for key in ('floor','highest','progress'):
            if not isinstance(state[key],int) or state[key]<(0 if key=='progress' else 1): raise ValueError('잘못된 층 정보')
        for item in state['inventory'].values():
            if not {'instance_id','base_id','name','slot','level','rarity','enhance','rolled_stats','affixes'}.issubset(item): raise ValueError('장비 데이터 누락')
        if any(not isinstance(n,int) or n<0 for n in state['items'].values()): raise ValueError('잘못된 아이템 수량')
        if state['player']['hp'] < 0 or state['player']['gold'] < 0: raise ValueError('잘못된 자원')
        ids=list(state['equipped'].values())+state['bag']+state['storage']
        if len(ids)!=len(set(ids)) or any(i not in state['inventory'] for i in ids): raise ValueError('장비 참조 오류')
        if state['save_schema_version']>=2:
            result=state.get('event_result')
            if result is not None and (not isinstance(result,dict) or any(not isinstance(result.get(k),str) for k in ('title','description','choice','text'))): raise ValueError('이벤트 결과 데이터 오류')
            pending=state.get('pending_loot')
            if not isinstance(pending,list): raise ValueError('획득 대기 목록 누락')
            pending_ids=[]
            for row in pending:
                pending_ids.append(row['pending_id'])
                if row['kind']=='item':
                    if not isinstance(row['quantity'],int) or row['quantity']<=0: raise ValueError('획득 대기 수량 오류')
                elif row['kind']=='equipment':
                    if not {'instance_id','base_id','name','slot','level','rarity','enhance','rolled_stats','affixes'}.issubset(row['equipment']): raise ValueError('획득 대기 장비 데이터 누락')
                    iid=row['equipment']['instance_id']
                    if iid in ids: raise ValueError('획득 대기 장비 중복')
                    ids.append(iid)
                else: raise ValueError('획득 대기 종류 오류')
            if len(pending_ids)!=len(set(pending_ids)): raise ValueError('획득 대기 ID 중복')
            if not isinstance(state.get('elite_misses'),int) or state['elite_misses']<0: raise ValueError('드롭 보장 횟수 오류')
            if not isinstance(state.get('exploration_bonuses'),dict): raise ValueError('탐험 보너스 형식 오류')
            statuses=list(state.get('statuses',[])); enemy=state.get('enemy')
            if enemy and enemy.get('catalogue'):
                from .prefixes import validate_ids
                validate_ids(enemy)
                if 'prefix_runtime' in enemy:
                    if state.get('battle_rules_version')!=3: raise ValueError('접두어 효과 전투 버전 오류')
                    from .prefixes import validate_saved
                    validate_saved(enemy['prefix_runtime'])
                if not isinstance(enemy.get('pattern_index'),int) or enemy['pattern_index']<0: raise ValueError('전투 패턴 진행 오류')
                allowed={'attack','defend','special'}
                if enemy.get('depth_rules_version') is not None:
                    from .high_floors import MECHANICS
                    if type(enemy['depth_rules_version']) is not int or enemy['depth_rules_version']!=1: raise ValueError('미지원 고층 전투 버전')
                    allowed|={'heavy','heal','debuff'}
                    env=enemy.get('environment_snapshot')
                    if not isinstance(env,dict) or not isinstance(env.get('name'),str) or not isinstance(env.get('id'),str): raise ValueError('환경 스냅샷 누락')
                    if env['id'] not in {f'catalogue.v3.ENV{i:03}' for i in range(1,31)} or not isinstance(env.get('primary_family'),str): raise ValueError('환경 스냅샷 참조 오류')
                    for key in ('risk_modifier_pct','reward_modifier_pct'):
                        if type(env.get(key)) not in (int,float) or not math.isfinite(env[key]) or env[key]<0: raise ValueError('환경 스냅샷 수치 오류')
                    if type(enemy.get('reward_factor')) not in (int,float) or not math.isfinite(enemy['reward_factor']) or enemy['reward_factor']<=0: raise ValueError('보상 배율 오류')
                    if enemy.get('mechanic'):
                        if enemy['mechanic'] not in MECHANICS: raise ValueError('미지원 저장 보스 기믹')
                        for key in ('summon_turns','healing_suppression'):
                            if type(enemy.get(key)) is not int or not 0<=enemy[key]<=2: raise ValueError('보스 기믹 기간 오류')
                        if type(enemy.get('suppression_at')) is not int or not 0<=enemy['suppression_at']<=state.get('turn',0): raise ValueError('보스 기믹 시점 오류')
                if not enemy.get('pattern') or set(enemy['pattern'])-allowed: raise ValueError('미지원 저장 전투 패턴')
                statuses+=enemy.get('statuses',[])
            for status in statuses:
                if not isinstance(status.get('turns'),int) or status['turns']<1: raise ValueError('상태 지속시간 오류')
                if status.get('effect_number') is not None and status['effect_number'] not in range(1,41): raise ValueError('미지원 저장 상태효과')
                if status.get('effect_number') in EFFECTS: validate_status(status,state)
            for item in list(state['inventory'].values())+[r['equipment'] for r in pending if r['kind']=='equipment']:
                if 'generation_rules_version' in item and (type(item['generation_rules_version']) is not int or item['generation_rules_version']!=1): raise ValueError('미지원 장비 생성 버전')
                if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in item['rolled_stats'].values()): raise ValueError('장비 수치 오류')
        if state['save_schema_version']==3:
            settings=state['settings']
            if settings.get('recovery_policy','potion_first') not in ('potion_first','skill_first','efficient'): raise ValueError('자동 회복 정책 오류')
            reserve=settings.get('mp_reserve',0)
            if type(reserve) is not int or not 0<=reserve<=999: raise ValueError('MP 예약량 오류')
            for key in ('skill_cooldowns','skill_buffs','skill_usage'):
                if not isinstance(state.get(key),dict): raise ValueError('스킬 상태 누락: '+key)
            if any(type(v) is not int or v<0 for v in state['skill_cooldowns'].values()): raise ValueError('스킬 대기시간 오류')
            if any(k not in state['skills'] for k in state['skill_cooldowns']): raise ValueError('스킬 대기시간 참조 오류')
            if any(type(v) is not int or v<0 for v in state['skill_usage'].values()): raise ValueError('스킬 사용 기록 오류')
            if any(type(v) is not int or not 0<=v<=5 for v in state['skills'].values()): raise ValueError('스킬 레벨 오류')
            if type(state.get('phase2_legacy_combat')) is not bool: raise ValueError('이전 전투 상태 오류')
            for key,buff in state['skill_buffs'].items():
                if key not in state['skills']: raise ValueError('스킬 효과 참조 오류')
                if not isinstance(buff,dict) or buff.get('kind') not in ('attack','reduction') or type(buff.get('remaining')) is not int or buff['remaining']<1: raise ValueError('스킬 지속시간 오류')
                if type(buff.get('applied_at')) is not int or not isinstance(buff.get('name'),str) or not isinstance(buff.get('value'),(int,float)) or not math.isfinite(buff['value']) or not 0<=buff['value']<1: raise ValueError('스킬 효과 오류')
            if not isinstance(state.get('skill_auto'),dict): raise ValueError('자동 스킬 설정 누락')
            for config in state['skill_auto'].values():
                if not isinstance(config,dict) or type(config.get('enabled')) is not bool or type(config.get('priority')) is not int or not 1<=config['priority']<=9: raise ValueError('자동 스킬 설정 오류')
            if state.get('event_result') is not None and 'resolved' in state['event_result'] and state['event_result']['resolved'] is not True: raise ValueError('미확정 이벤트 결과')

    def save(self, slot, state):
        self.validate(state)
        path=self.path(slot)
        state['saved_at']=datetime.now().astimezone().isoformat(timespec='seconds')
        temp=path.with_suffix('.tmp')
        with temp.open('w',encoding='utf-8') as f:
            json.dump(state,f,ensure_ascii=False,indent=2); f.flush(); os.fsync(f.fileno())
        self.validate(json.loads(temp.read_text(encoding='utf-8')))
        if path.exists():
            try:
                self.validate(json.loads(path.read_text(encoding='utf-8')))
                shutil.copy2(path,path.with_suffix('.json.bak'))
            except (ValueError,KeyError,TypeError):
                shutil.copy2(path,path.with_suffix('.json.corrupt'))
        os.replace(temp,path)

    def load(self,slot):
        path=self.path(slot)
        self.notice=''
        try:
            state=json.loads(path.read_text(encoding='utf-8')); self.validate(state)
            return self.prepare_migration(state,path)
        except (ValueError,KeyError,TypeError,OSError) as original:
            backup=path.with_suffix('.json.bak')
            if not backup.exists(): raise ValueError(f'저장을 읽을 수 없습니다: {original}') from original
            state=json.loads(backup.read_text(encoding='utf-8')); self.validate(state)
            if path.exists(): shutil.copy2(path,path.with_suffix('.json.corrupt'))
            self.notice='손상된 원본을 보존하고 백업을 불러왔습니다.'
            return self.prepare_migration(state,backup)

    def prepare_migration(self,state,path):
        if state['save_schema_version']==1:
            from .migrations import migrate_v1_to_v2
            backup=path.with_suffix(path.suffix+'.pre-v2.bak')
            if backup.exists() and backup.read_bytes()!=path.read_bytes():
                digest=hashlib.sha256(path.read_bytes()).hexdigest()[:12]
                backup=path.with_suffix(path.suffix+f'.pre-v2-{digest}.bak')
            if not backup.exists(): shutil.copy2(path,backup)
            migrated=migrate_v1_to_v2(state); self.validate(migrated)
            self.notice+=' 저장 버전 1을 2로 이전했습니다. 변경 전 백업을 보존했습니다.'
            state=migrated
        if state['save_schema_version']==2:
            from .migrations import migrate_v2_to_v3
            backup=path.with_suffix(path.suffix+'.pre-v3.bak')
            if backup.exists() and backup.read_bytes()!=path.read_bytes():
                digest=hashlib.sha256(path.read_bytes()).hexdigest()[:12]
                backup=path.with_suffix(path.suffix+f'.pre-v3-{digest}.bak')
            if not backup.exists(): shutil.copy2(path,backup)
            state=migrate_v2_to_v3(state); self.validate(state)
            self.notice+=' 저장 버전을 3으로 이전했습니다. 변경 전 백업을 보존했습니다.'
        return state

    def delete(self,slot):
        path=self.path(slot)
        for item in (path,path.with_suffix('.json.bak')):
            if item.exists(): os.replace(item,item.with_suffix(item.suffix+'.deleted'))
