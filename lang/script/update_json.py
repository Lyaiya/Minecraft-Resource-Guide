import os
import shutil

import orjson
import regex

current_encoding = "utf-8"


# 工作路径切换到脚本所在路径
def SwitchWorkPath():
    # 当前工作路径
    cwd_path = os.getcwd()
    # 脚本所在路径
    script_path = os.path.split(os.path.realpath(__file__))[0]

    # 判断当前工作路径是否为脚本所在路径
    if cwd_path != script_path:
        os.chdir(script_path)


# 判断文件是否存在
def isPathExists(path: str) -> bool:
    return os.path.exists(path)


# 复制 JSON
def CopyJson(origin_json_name: str, new_json_name: str) -> bool:
    # 判断是否存在 new_json_name 文件
    if isPathExists(new_json_name):
        return False
    else:
        # 不存在则进行复制
        shutil.copy(origin_json_name, new_json_name)
        return True


# 获取 JSON 字典
def GetJsonDict(json_name: str) -> dict:
    json_dict = dict()

    if isPathExists(json_name):
        with open(json_name, "rb") as load_f:
            json_dict = orjson.loads(load_f.read())

    return json_dict


# 获取 JSON 字符串
def GetJsonStr(json_name: str) -> str:
    json_str = str()

    if isPathExists(json_name):
        with open(json_name, "rb") as load_f:
            json_str = load_f.read().decode(current_encoding)

    return json_str


# 获取更新后的 JSON 字符串
# TODO 添加相同 key 的检测
def GetUpdatedJsonDict(origin_json_dict: dict, compare_json_dict: dict, deleteNewJsonDictComment: bool = False) -> tuple[dict, dict]:
    # 获取 key 集合
    origin_dict_items = origin_json_dict.items()
    compare_dict_items = compare_json_dict.items()

    # 新字典（基于 compare_json 更新 origin_json）
    new_json_dict = origin_json_dict.copy()
    # 旧字典（origin_json 不存在的词条）
    old_json_dict = compare_json_dict.copy()

    # 删除旧字典的注释 key（一般以 ‘_’ 为开头）
    for compare_dict_item in compare_dict_items:
        if compare_dict_item[0].startswith('_'):
            old_json_dict.pop(compare_dict_item[0])

    for origin_dict_item in origin_dict_items:
        # 跳过注释 key
        if origin_dict_item[0].startswith('_'):
            continue

        for compare_dict_item in compare_dict_items:
            # 判断 key 是否相同
            if origin_dict_item[0] == compare_dict_item[0]:
                # 修改新字典中 key 对应的 value
                new_json_dict[origin_dict_item[0]] = compare_dict_item[1]
                # 删除旧字典的 key-value 对
                old_json_dict.pop(compare_dict_item[0])
                break

    if deleteNewJsonDictComment:
        # 删除新字典的注释 key（默认不删除）
        for origin_dict_item in origin_dict_items:
            if origin_dict_item[0].startswith('_'):
                new_json_dict.pop(origin_dict_item[0])

    return new_json_dict, old_json_dict


# 获取正则表达式模版
def GetPattern(key: str) -> str:
    return regex.compile(r'\"{0}\":\s*\"(.*?)\"\s*,'.format(key))


# 获取更新后的 JSON 字符串
def GetUpdatedJsonStr(json_dict: dict, json_str: str) -> str:
    # 获取 key 集合
    json_dict_items = json_dict.items()

    # 复制为最终字符串
    final_json_str = json_str

    for json_dict_item in json_dict_items:
        key = json_dict_item[0]
        value = json_dict_item[1]

        # 正则表达式处理字符串
        final_json_str = regex.sub(GetPattern(key), lambda x: x.group(
            0).replace(x.group(1), value), final_json_str)

    return final_json_str


# 使用 Str 导出 JSON
def DumpJsonWithStr(json_str: str, json_name: str):
    # 判断字符串是否为空
    if len(json_str) == 0:
        return

    with open(json_name, "w", encoding=current_encoding, newline=str()) as dump_f:
        dump_f.write(json_str)


# 使用 Dict 导出 JSON
def DumpJsonWithDict(json_dict: dict, json_name: str):
    # 判断字典是否为空
    if not json_dict:
        return

    with open(json_name, "wb") as dump_f:
        dump_f.write(orjson.dumps(json_dict, option=orjson.OPT_INDENT_2))


# 主程序
if __name__ == "__main__":
    # 切换工作路径
    SwitchWorkPath()

    # 定义字符串
    origin_json_name = "en_us.json"
    compare_json_name = "zh_cn.json"
    new_json_name = "zh_cn_new.json"
    old_json_name = "zh_cn_old.json"

    # 获取 JSON 字典
    origin_json_dict = GetJsonDict(origin_json_name)
    compare_json_dict = GetJsonDict(compare_json_name)

    # 获取更新后的 JSON 字典
    new_json_dict, old_json_dict = GetUpdatedJsonDict(
        origin_json_dict, compare_json_dict, True)

    # 获取 JSON 字符串
    origin_json_str = GetJsonStr(origin_json_name)

    # 获得更新后的 JSON 字符串
    final_json_str = GetUpdatedJsonStr(new_json_dict, origin_json_str)

    # 导出 Json
    DumpJsonWithStr(final_json_str, new_json_name)
    DumpJsonWithDict(old_json_dict, old_json_name)
