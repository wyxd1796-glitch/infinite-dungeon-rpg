import json
from pathlib import Path
from .phase2_content import PHASE2_EFFECTS, validate_phase2, has_phase2_effect

EFFECTS = {'damage','heal_hp','heal_mp','modify_stat','grant_item','grant_gold','grant_exp','equipment','hurt','add_status','start_combat','nothing'}
EFFECTS |= PHASE2_EFFECTS
CONDITIONS = {'min_floor','max_floor','gold_at_least','hp_percent','has_item','boss_defeated','has_tag'}
REQUIRED = {
    'monsters': {'id','name','hp','atk','defense','evasion','accuracy','weight','abilities'},
    'equipment': {'id','name','slot','stats'}, 'items': {'id','name','category','price','sell_price','effects'},
    'skills': {'id','name','kind','mp','max_level','effects'}, 'events': {'id','title','description','weight','options'},
    'achievements': {'id','name','metric','target','reward'}, 'affixes': {'id','name','stat','base','per_level'},
    'prefixes': {'id','name','stats','exp'}, 'bosses': {'id','name','monster_id','ability'},
}

class Content:
    def __init__(self, root):
        self.root = Path(root)
        self.tables = {}
        self.by_id = {}
        self.errors = []
        self.packs = []
        self.balance = json.loads((self.root/'base/balance.json').read_text(encoding='utf-8'))
        self._load(self.root/'base')
        pending = list((self.root/'packs').glob('*/manifest.json'))
        while pending:
            progress = False
            for path in pending[:]:
                try:
                    manifest = json.loads(path.read_text(encoding='utf-8'))
                    if not manifest.get('enabled', True):
                        pending.remove(path); progress = True; continue
                    if all(d in [p['id'] for p in self.packs] for d in manifest.get('dependencies', [])):
                        self._load(path.parent)
                        pending.remove(path); progress = True
                except (ValueError, KeyError, OSError, TypeError) as exc:
                    self.errors.append(f'{path.parent.name}: {exc}')
                    pending.remove(path); progress = True
            if not progress:
                self.errors.extend(f'{p.parent.name}: 의존성 누락 또는 순환' for p in pending)
                break

    def _load(self, folder):
        manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        if manifest['schema_version'] != 1:
            raise ValueError('지원하지 않는 콘텐츠 버전')
        if manifest['pack_id'] in [p['id'] for p in self.packs]: raise ValueError('중복 팩 ID')
        candidate = {}
        ids = dict(self.by_id)
        for name in manifest['content_files']:
            if Path(name).name != name or not name.endswith('.json'):
                raise ValueError('잘못된 콘텐츠 경로')
            rows = json.loads((folder/name).read_text(encoding='utf-8'))
            kind=Path(name).stem
            if kind not in REQUIRED: raise ValueError(f'미지원 콘텐츠 종류: {kind}')
            if not isinstance(rows, list): raise ValueError('콘텐츠는 목록이어야 합니다')
            for row in rows:
                if not isinstance(row,dict) or not REQUIRED[kind].issubset(row): raise ValueError(f'{kind}: 필수 필드 누락')
                key = row['id']
                if not isinstance(key,str) or len(key.split('.'))<3: raise ValueError('ID는 pack.type.name 형식입니다')
                if key in ids: raise ValueError(f'중복 ID: {key}')
                if kind=='monsters' and (row['hp']<=0 or not 0<=row['evasion']<=1 or not 0<=row['accuracy']<=1): raise ValueError('잘못된 몬스터 능력치')
                if kind=='equipment' and row['slot'] not in ('무기','투구','갑옷','장갑','신발','반지','목걸이'): raise ValueError('미지원 장비 슬롯')
                if kind=='skills' and row['kind'] not in ('active','passive'): raise ValueError('미지원 스킬 종류')
                if has_phase2_effect(row) and not row.get('phase2'): raise ValueError('2차 효과는 검증된 2차 정의에서만 사용할 수 있습니다.')
                if row.get('phase2'):
                    if kind not in ('skills','events'): raise ValueError('2차 콘텐츠 종류 오류')
                    if not hasattr(self,'_phase2_source'):
                        self._phase2_source=json.loads((self.root/'source/catalogue_v4.json').read_text(encoding='utf-8'))['base_catalogue_v3']['content']
                        self._phase2_selection=json.loads((self.root/'catalogue/selection.json').read_text(encoding='utf-8'))
                    validate_phase2(row,kind,self._phase2_source,self._phase2_selection)
                ids[key] = row
            candidate[Path(name).stem] = rows
        for rows in candidate.values():
            if rows and all('weight' in r for r in rows) and sum(r['weight'] for r in rows) <= 0:
                raise ValueError('가중치 합이 0입니다')
            for row in rows:
                self._validate(row, ids)
        def references(obj):
            if isinstance(obj,dict):
                for k,v in obj.items():
                    if k in ('item_id','monster_id','effect_id') and v is not None: yield v
                    else: yield from references(v)
            elif isinstance(obj,list):
                for v in obj: yield from references(v)
        visited=set(); visiting=set()
        def visit(key):
            if key in visiting: raise ValueError(f'콘텐츠 순환 참조: {key}')
            if key in visited: return
            visiting.add(key)
            for ref in references(ids[key]): visit(ref)
            visiting.remove(key); visited.add(key)
        for key in ids: visit(key)
        self.by_id = ids
        for name, rows in candidate.items(): self.tables.setdefault(name, []).extend(rows)
        self.packs.append({'id':manifest['pack_id'],'version':manifest['version']})

    def _validate(self, obj, ids):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in ('item_id','monster_id','effect_id') and value is not None and value not in ids: raise ValueError(f'없는 참조: {value}')
                if key in ('weight','price','cost','hp','atk','defense','min_floor','mp','max_level') and (not isinstance(value,(int,float,list)) or (isinstance(value,(int,float)) and value < 0) or (isinstance(value,list) and any(not isinstance(v,(int,float)) or v<0 for v in value))):
                    raise ValueError(f'잘못된 수치: {key}')
                if key == 'effects' and any(e.get('type') not in EFFECTS for e in value): raise ValueError('미지원 효과')
                if key == 'conditions' and any(c.get('type') not in CONDITIONS for c in value): raise ValueError('미지원 조건')
                if key == 'outcomes' and (not value or sum(o['weight'] for o in value)<=0): raise ValueError('결과 가중치 합이 0입니다')
                if key == 'options' and not 1 <= len(value) <= 3: raise ValueError('선택지는 1~3개')
                self._validate(value, ids)
        elif isinstance(obj,list):
            for value in obj: self._validate(value, ids)

    def __getitem__(self, name): return self.tables[name]
