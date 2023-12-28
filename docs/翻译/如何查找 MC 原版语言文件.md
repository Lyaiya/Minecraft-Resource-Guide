# 如何查找 MC 原版语言文件

此处以查找 MC 1.16 版本的简体中文语言文件为例。文本编辑器推荐选用 VSCODE（当然记事本也没问题）。

打开 `.minecraft\assets\indexes\1.16.json` 文件（MC 1.16 可替换为其他版本号）。

注：语言文件可能并非最新，可先删除以上文件，然后通过启动器来下载新文件（如 HMCL 的检查游戏完整性），再进行后续操作。

按 `Ctrl+F` 搜索 `minecraft/lang/zh_cn.json`。（MC 1.13 以下版本的语言文件后缀名为 lang）

例如

```json
"minecraft/lang/zh_cn.json": {
  "hash": "6026d3f2d27764e2d3eaae2eacd8ce7274a4ed2d",
  "size": 378726
},
```

记下 hash 的前两个字符，此处为 60。

打开 `.minecraft\assets\objects` 文件夹，再打开名称为 60 的文件夹。

找到 `6026d3f2d27764e2d3eaae2eacd8ce7274a4ed2d` 文件。

此文件即为 MC 1.16 的简体中文语言文件。

最后**可能**还需要将语言文件从 Unicode 转为中文。

推荐一个转码网站：<https://www.bejson.com/convert/unicode_chinese/>（不要勾选“英文数字是否转义”）

## en_us 语言文件

en_us 语言文件存放在游戏客户端 jar 文件

游戏客户端实例路径：`prismlauncher\libraries\com\mojang\minecraft\1.20.1\minecraft-1.20.1-client.jar`（以 PrismLauncher 为例）

使用压缩软件打开 jar 文件， `assets\minecraft\lang\en_us.json` 即为需要的语言文件。
