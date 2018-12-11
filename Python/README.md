# Python

## 终端执行python

`$ python`进入python环境

第一行提示版本号和更新日期

下面的`>>>`是提示符，这里可以输入Python代码

`Ctrl D` 或者执行 `exit()` 退出

在 IPython 中使用 `Ctrl D` 后还需要确认一下才能退出

## 创建空集合

```py
s = set()
s = {i for i in []}  # 推导式产生的一定是集合类型，不会因为空数据而变成字典
```