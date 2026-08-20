# 03. 项目布局与加载

## Script 根

第一次用自定义 Editor 打开项目时，UE‑AS 会在项目根建立：

```text
<Project>/Script/
```

所有 `.as` 文件自动被加载。官方 VS Code 扩展要求把 `Script/` 作为打开的工作区根，而不是把整个 Unreal 项目根当成脚本工作区。

## 推荐目录

```text
Script/
  Game/
    Characters/
    Abilities/
    Interaction/
    AI/
    UI/
  Framework/
    Messaging/
    Tasks/
    Save/
  Shared/
    Math/
    Data/
  Tests/
    Unit/
    Integration/
  Editor/
    Menus/
    Tabs/
    Details/
  Dev/
  Examples/
```

`Editor`、`Dev`、`Examples` 目录在 cooked 脚本编译中被忽略。不要把运行时依赖放进去。

## 文件粒度

推荐一个主要类型一个文件，紧密耦合的小 struct/enum 可同文件。测试通常使用：

```text
Inventory.as
Inventory_Test.as
```

集成测试：

```text
Interaction_IntegrationTest.as
Content/Testing/IntegrationTest_Interaction.umap
```

## 命名空间

项目默认通常不允许跨文件暴露无命名空间全局函数。公共函数库使用：

```angelscript
namespace Inventory
{
    bool CanAdd(const FInventoryState& State, const FItemData& Item)
    {
        ...
    }
}
```

命名空间同时减少脚本符号冲突并使 API 搜索更清晰。

## 依赖方向

```text
Shared/Data
    ↑
Domain Rules
    ↑
Components / Subsystems
    ↑
Actors / UI / Editor Tools
```

Editor 可以依赖 Runtime；Runtime 不得依赖 Editor。UI 可以读取 ViewModel，不应成为唯一业务状态持有者。

## API 发现

优先顺序：

1. 目标项目已有调用；
2. VS Code LSP completion / hover；
3. UE‑AS Script API Reference；
4. C++ UHT 反射定义与 Bind Database；
5. 官方源码示例；
6. 最后才根据命名规则推断。

常见 C++ API 在脚本中会被简化命名，直接搜索 C++ 全名可能找不到。

## Agent 浏览策略

不要一次读取整个 `Script/`。先：

- 搜同类基类；
- 搜目标 UFUNCTION/UPROPERTY；
- 搜命名空间；
- 搜测试；
- 搜 Build.cs / Config；
- 读取最小闭包。

输出时记录采用了哪些项目约定。
