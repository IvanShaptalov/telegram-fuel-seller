import json

from icecream import ic

from utils import db_util


def save_parameter(chat_id, **kwargs):
    db_util.write_obj_to_table(table_class=db_util.ClientSignJson,
                               identifier=db_util.ClientSignJson.user_chat_id,
                               value=chat_id,
                               user_chat_id=chat_id)
    obj = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ClientSignJson,
                                                    identifier=db_util.ClientSignJson.user_chat_id,
                                                    value=chat_id)
    assert isinstance(obj, db_util.ClientSignJson)
    json_info = obj.all_info_json
    info = json.loads(json_info)
    assert isinstance(info, dict)
    if kwargs:
        for key, value in kwargs.items():
            info['{}'.format(key)] = value
    json_info = json.dumps(info)
    db_util.write_obj_to_table(table_class=db_util.ClientSignJson,
                               identifier=db_util.ClientSignJson.user_chat_id,
                               value=chat_id,
                               user_chat_id=chat_id,
                               all_info_json=json_info)
    ic('info saved!')