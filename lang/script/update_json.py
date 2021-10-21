import os
from pathlib import Path

import orjson
import regex

current_encoding = "utf-8"


# 工作路径切换到脚本所在路径
def SwitchWorkPath():
    # 当前工作路径
    cwd_path = Path.cwd()
    # 脚本所在路径
    script_path = Path(__file__).parent

    # 判断当前工作路径是否为脚本所在路径
    if cwd_path != script_path:
        os.chdir(script_path)


# 判断文件是否存在
def isPathExists(path_name: str) -> bool:
    return Path(path_name).exists()


# 获取 JSON 字典
def GetJsonDict(path_name: str) -> dict:
    json_dict = dict()

    if isPathExists(path_name):
        with open(path_name, "rb") as load_f:
            json_dict = orjson.loads(load_f.read())

    return json_dict


# 获取 JSON 字符串
def GetJsonStr(path_name: str) -> str:
    json_str = str()

    if isPathExists(path_name):
        with open(path_name, "rb") as load_f:
            json_str = load_f.read().decode(current_encoding)

    return json_str


# 获取更新后的 JSON 字符串
def GetUpdatedJsonDict(origin_json_dict: dict, compare_json_dict: dict, deleteCommentKey: bool) -> tuple[dict, dict, dict]:
    # 获取 key 集合
    origin_dict_items = origin_json_dict.items()
    compare_dict_items = compare_json_dict.items()

    # 注释 key 前缀（一般以 ‘_’ 为开头）
    comment_key_prefix = '_'

    # 无注释字典（删除 origin_json 里面的注释 key）
    nocomment_json_dict = origin_json_dict.copy()
    # 新字典（基于 compare_json 的词条来替换 origin_json 的词条）
    new_json_dict = origin_json_dict.copy()
    # 旧字典（保留 origin_json 不存在的词条）
    old_json_dict = compare_json_dict.copy()

    # 删除旧字典的注释 key
    for compare_dict_item in compare_dict_items:
        if compare_dict_item[0].startswith(comment_key_prefix):
            old_json_dict.pop(compare_dict_item[0])

    for origin_dict_item in origin_dict_items:
        # 跳过注释 key
        if origin_dict_item[0].startswith(comment_key_prefix):
            continue

        for compare_dict_item in compare_dict_items:
            # 判断 key 是否相同
            if origin_dict_item[0] == compare_dict_item[0]:
                # 替换新字典中 key 对应的 value
                new_json_dict[origin_dict_item[0]] = compare_dict_item[1]
                # 删除旧字典的 key-value 对
                old_json_dict.pop(compare_dict_item[0])
                break

    if deleteCommentKey:
        # 删除 nocomment_json_dict 和 new_json_dict 的注释 key
        for origin_dict_item in origin_dict_items:
            if origin_dict_item[0].startswith(comment_key_prefix):
                nocomment_json_dict.pop(origin_dict_item[0])
                new_json_dict.pop(origin_dict_item[0])

    return nocomment_json_dict, new_json_dict, old_json_dict


# 获取正则表达式模版
def GetPattern(key: str) -> str:
    return regex.compile(r'\"{0}\":\s*\"(.*?)\"\s*,'.format(key))


# 获取更新后的 JSON 字符串
# FIXME 存在转义问题
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


# 创建目录
def CreatePath(path_name: str) -> Path:
    output_path = Path(path_name)
    output_path.mkdir(exist_ok=True)
    return output_path


# 根据字符串导出 JSON
def DumpJsonWithStr(json_str: str, path_name: str):
    # 判断字符串是否为空
    if len(json_str) == 0:
        return

    with open(path_name, "w", encoding=current_encoding, newline=str()) as dump_f:
        dump_f.write(json_str)


# 根据字典导出 JSON
def DumpJsonWithDict(json_dict: dict, path_name: str):
    # 判断字典是否为空
    if not json_dict:
        return

    with open(path_name, "wb") as dump_f:
        dump_f.write(orjson.dumps(json_dict, option=orjson.OPT_INDENT_2))


# 主程序
if __name__ == "__main__":
    # 切换工作路径
    SwitchWorkPath()
    output_path = CreatePath("output")

    # 定义文件名字符串
    origin_json_name = "en_us.json"
    compare_json_name = "zh_cn.json"
    old_json_name = "zh_cn_old.json"

    # 获取 JSON 字典
    origin_json_dict = GetJsonDict(origin_json_name)
    compare_json_dict = GetJsonDict(compare_json_name)

    # 获取更新后的 JSON 字典
    nocomment_json_dict, new_json_dict, old_json_dict = GetUpdatedJsonDict(
        origin_json_dict, compare_json_dict, True)

    # 获取 JSON 字符串
    origin_json_str = GetJsonStr(origin_json_name)

    # 获得更新后的 JSON 字符串
    # final_json_str = GetUpdatedJsonStr(new_json_dict, origin_json_str)

    # 导出 JSON
    # DumpJsonWithStr(final_json_str, new_json_name)
    DumpJsonWithDict(nocomment_json_dict, output_path / origin_json_name)
    DumpJsonWithDict(new_json_dict, output_path / compare_json_name)
    DumpJsonWithDict(old_json_dict, output_path / old_json_name)
