# 默认值与结构性热重载

## 热重载分类

### 通常较轻

- 普通函数体修改；
- 不改变反射签名的局部逻辑；
- 普通脚本 helper。

### 结构性修改

- 新增/删除/改类型的反射字段；
- UFUNCTION 参数、返回值或 specifier 变化；
- 父类、接口、默认子对象变化；
- `BindWidget` 名称/类型变化；
- Blueprint 可见 API 重命名。

结构性修改后检查 Blueprint 编译、CDO/实例值、Delegate、Timer、Widget 绑定和已打开 Editor
工具。出现不一致时优先完整编译、关闭 PIE、重新打开资产或重启 Editor，不用继续叠加热重载。

默认值来源包括脚本初始化/default、CDO、Blueprint Class Defaults、关卡或资产实例覆盖、运行时修改。值不更新时先定位持有覆盖值的层级。
