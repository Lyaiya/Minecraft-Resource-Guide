# 脚本

## update_json.py

Json 语言文件更新，保留原始语言文件换行（目前需要 python 环境和相关库）。

1. 把 `update_json.py`、`en_us.json` 和 `zh_cn.json` 放在同一路径。
2. 运行 python 脚本，在 output 目录下生成 `en_us.json`（去注释）、`zh_cn.json`（更新后）、 `zh_cn_old.json`（遗留词条）。
