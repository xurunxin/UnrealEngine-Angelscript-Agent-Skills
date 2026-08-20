# 32. 故障排查

## Script 文件不加载

- 是否在 `<Project>/Script`；
- 扩展名 `.as`；
- 是否使用自定义 UE‑AS Editor；
- Output Log Angelscript 模块；
- 文件是否在 Editor/Dev/Examples 且当前 simulate-cooked；
- 编译错误导致模块失败。

## VS Code 无补全

- 打开的根是否正好是 `Script/`；
- Editor 是否运行；
- 扩展是否连接到正确实例；
- 防火墙/多 Editor 实例；
- 目标 Engine source path；
- Reload Window。

## C++ API 在脚本不可见

- 是否 BlueprintType/Callable/Visible；
- `NotInAngelscript` / `NoAutoAngelscriptBind`；
- deprecated；
- 签名类型能否绑定；
- 名称是否被简化；
- Bind Database；
- 重启 Editor 重新生成绑定。

## Hot reload 后数据异常

- 是否结构性修改；
- BP 子类；
- 字段重命名/类型改变；
- CDO/default；
- 旧 Delegate/Timer；
- 完整重启验证；
- 必要时撤回结构改动并迁移资产。

## simulate-cooked 失败

- Runtime 脚本引用 Editor 类型；
- Editor 文件位置不正确；
- `#if EDITOR` 只包函数体但签名仍泄漏；
- Dev/Examples 类型被 Runtime 引用；
- Editor-only UPROPERTY；
- C++ module dependency。

## EmmsUI “No root active”

- 缺 BeginDraw；
- EndDraw 过早；
- 跨根 Handle；
- 异常/早退；
- Begin/End 不成对。

## Mismatched Begin/End

检查嵌套顺序，`BeginHorizontalBox` 必须对应 `EndHorizontalBox`，不能用通用 End 替代特定自动绑定 End。

## 输入文本跳动/被清空

- state 是否局部变量；
- EmmsUI 是否含 mutable state 修复；
- 程序每帧覆盖模型；
- 同类型 sibling 身份错位；
- 属性 getter/setter 同时竞争。

## ListView for-loop 不编译

- EmmsUI 使用新 iterator protocol；
- 目标 UE‑AS 太旧；
- 固定匹配 commit；
- 临时使用目标旧版本支持的迭代 API；
- 不凭猜测修改 `Iterate`，检查绑定源码。

## Editor Tab 热重载后重复/消失

- 目标 EmmsUI 是否有 object reinstancing 修复；
- Reinstance delegate 是否移除；
- StrongSelf；
- Tab 注册重复；
- 完整重启；
- 回移最新相关 commit。

## Cook 加载不到脚本

- 是否生成/包含 PrecompiledScript.Cache；
- executable 是否与缓存匹配；
- 是否意外启用 development mode；
- AS_JITTED_CODE module；
- pak staging；
- 日志中的 cache mismatch。
