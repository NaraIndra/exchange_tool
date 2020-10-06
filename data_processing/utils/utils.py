from typing import List
from db.db_model import Currency_pair

def find_minvalue_from_list(pairs: List[Currency_pair]) -> int:
    if not isinstance(pairs, List):
        raise ValueError(f'{type(pairs)=} должен быть списком')
    # if not len(pairs):
        raise ValueError(f'{len(pairs)=} должен быть положительным числом')
    min_v = pairs[0].cur_give_num
    min_saler_num = pairs[0].saler_num
    for index, x in enumerate(pairs):
        if x.cur_give_num < min_v:
            min_index = x.saler_num
    return min_saler_num
