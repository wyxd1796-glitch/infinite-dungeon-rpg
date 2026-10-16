"""Save schema versions are independent of catalogue source versions."""
import copy
import uuid

def migrate_v1_to_v2(original):
    state=copy.deepcopy(original)
    if state['save_schema_version']!=1: return state
    state['save_schema_version']=2; state['game_version']='1.1.0'
    state['legacy_pending']=state['mode'] in ('combat','event')
    state.setdefault('pending_loot',[])
    state.setdefault('elite_misses',0); state.setdefault('floor_type','FLR005' if state['floor']%10==0 else 'FLR001')
    state.setdefault('exploration_bonuses',{}); state.setdefault('shop_stock',[])
    # Preserve excess quantities as claimable data, never truncate or silently sell.
    slots=len(state['bag'])
    for key,quantity in list(state['items'].items()):
        cap=999 if key=='base.item.stone' or '.MAT' in key else 99
        keep=min(quantity,cap) if slots<30 else 0
        if keep: slots+=1
        state['items'][key]=keep
        if quantity>keep: state['pending_loot'].append(dict(pending_id=str(uuid.uuid4()),kind='item',item_id=key,quantity=quantity-keep))
    return state
