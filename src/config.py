import yaml

battle_conf = yaml.load(open('conf/battle.yaml'), Loader=yaml.FullLoader)


def conf_battle_stage() -> list:
    return battle_conf['stages']


def battle_stage_count() -> int:
    return len(conf_battle_stage())


def in_which_stage(round: int) -> dict:
    for i in conf_battle_stage():
        if i['start'] <= round and (round <= i['end'] or i['end'] == -1):
            return i


system_conf = yaml.load(open('conf/system.yaml'), Loader=yaml.FullLoader)


def conf_system_db() -> dict:
    return system_conf['db']


def db_path() -> str:
    return conf_system_db()['path']
