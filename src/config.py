import random

import yaml

with open('conf/battle.yaml', 'r', encoding='utf-8') as f:
    battle_conf = yaml.load(f, Loader=yaml.FullLoader)


def conf_battle() -> dict:
    return battle_conf


def conf_battle_stage() -> list:
    return conf_battle()['stages']


def battle_stage_count() -> int:
    return len(conf_battle_stage())


def in_which_stage(round: int) -> dict:
    for i in conf_battle_stage():
        if i['start'] <= round and (round <= i['end'] or i['end'] == -1):
            return i


with open('conf/system.yaml', 'r', encoding='utf-8') as f:
    system_conf = yaml.load(f, Loader=yaml.FullLoader)


def conf_system() -> dict:
    return system_conf


def conf_system_db() -> dict:
    return conf_system()['db']


def db_path() -> str:
    return conf_system_db()['path']


def conf_system_mode() -> str:
    return conf_system()['mode']


if 'op_key' in conf_system():
    op_key = conf_system()['op_key']
else:
    op_key = ''.join([random.choice('0123456789abcdef') for x in range(16)])
    print(f'op_key: {op_key}')


def get_op_key() -> str:
    return op_key
