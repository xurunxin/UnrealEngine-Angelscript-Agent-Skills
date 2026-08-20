# UE‑AS / EmmsUI Agent Routing

当任务涉及以下任一内容时，先读取 `skills/ueas-router/SKILL.md`：

- `.as` 文件、`Script/` 目录；
- UnrealEngine‑Angelscript、AngelscriptCode、AngelscriptEditor；
- `UPROPERTY`、`UFUNCTION`、`BlueprintOverride`、`BlueprintEvent`；
- `UMMWidget`、`mm::`、`mm<T>`、EmmsUI；
- UE‑AS 的测试、网络、预编译脚本或 C++ 绑定。

执行前必须：

1. 记录 Unreal、UE‑AS、EmmsUI 的精确版本或 commit；
2. 查看项目级 `AGENTS.md`、编码规范、Build.cs、Config 与已有同类实现；
3. 只加载路由选中的专题 Skill；
4. 说明结构性热重载风险、Cook/Editor 边界以及验证方式；
5. 修改后运行最小相关验证，不以静态猜测代替可执行结果。

禁止：

- 把 UE‑AS 当作普通项目插件安装；
- 从普通 AngelScript 文档猜测 UE‑AS API；
- 无理由扩大反射表面；
- 在 Shipping 路径依赖 Editor-only 类型；
- 在没有身份稳定性分析时重排条件式 EmmsUI 同类型兄弟节点；
- 用 `GetUnderlyingWidget()` 绕过属性差分后不负责复位；
- 未验证版本就使用 EmmsUI 主分支新增 API。
