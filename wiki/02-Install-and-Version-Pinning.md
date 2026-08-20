# 02. 安装与版本固定

## 官方安装事实

UE‑AS 对 Unreal Engine 源码有直接修改，因此需要：

1. Epic Games GitHub 账号授权；
2. 访问 UE‑AS 引擎 fork；
3. 从源码执行 Unreal 依赖下载、项目生成和 Editor 构建；
4. 使用该自定义 Editor 打开项目。

仅复制 `Engine/Plugins/Angelscript` 不足以构成完整集成。

## 推荐仓库策略

```text
company/
  UnrealEngine-Angelscript-fork   # 私有、保留 Epic 许可边界
  GameProject
    Plugins/EmmsUI                # submodule 或固定 vendor SHA
```

生产线固定：

- Unreal Major/Minor/Patch；
- UE‑AS commit；
- EmmsUI commit；
- 所有源码插件 commit；
- Toolchain/Compiler/SDK；
- 预编译缓存生成 executable hash。

## 当前锁文件示例

```json
{
  "unreal": "5.8.1",
  "ueas_commit": "546c4d6af141f1e820be1b2976211a756ca2639d",
  "emmsui_commit": "c5d4e303f1fc8a1545de4d336be19e69dc8518c0",
  "iterator_protocol": "source-signals-aligned",
  "status": "runtime-verification-required"
}
```

`source-signals-aligned` 只表示当前 UE‑AS 与 EmmsUI 都包含新 `Iterate()` 协议；不要把它写成 `compatible: true`，除非已有目标构建与运行证据。

不要只写 `master`、`latest` 或 `UE5`。

## 第一次构建验证

- Editor 构建成功；
- `Angelscript` 插件已启用；
- 项目根生成 `Script/`；
- `.as` 保存后自动编译；
- Place Actors 能看到脚本 Actor；
- VS Code 扩展连接 Editor；
- Debug F5 可用；
- EmmsUI Runtime/Editor 模块编译；
- 最小 `UMMWidget` 可显示；
- ListView 新 `Iterate()` range-for 可编译并只遍历可见 entry；
- EditableText/Slider 双向状态可保持；
- 打开的 Editor Tab 经结构性脚本热重载后仍指向新对象；
- simulate-cooked 通过；
- Cook/Package smoke 通过。

## 二进制插件

源码引擎 fork 的 Build ID、ABI 或 UE 版本可能与 Marketplace 二进制插件不同。优先获取第三方插件源码并在目标引擎构建。无法获取源码时，在升级计划中把它列为阻断依赖。

## 升级分支

建议：

```text
engine/ueas-5.8.1-pinned
engine/ueas-upgrade-5.9
project/upgrade-ueas-5.9
```

先让空项目与核心插件在新引擎通过，再迁移项目。保留旧引擎和可回退项目分支，避免资产被新版本保存后无法回退。

升级时分开提交：

1. UE/UE‑AS 同步与引擎构建；
2. EmmsUI 更新；
3. 项目脚本迁移；
4. 资产保存升级；
5. Cook/Package。

这样才能定位是引擎、binding、脚本还是资产导致失败。

## 当前研究快照的判断

本包 0.1.1 观察到 UE‑AS `546c4d6...` / UE 5.8.1 与 EmmsUI `c5d4e30...`。UE‑AS 的 `1a06a2bf...` 和 EmmsUI 的 `c9985c1...` 对同一新 iterator protocol 作了对应修改，因此不再存在 0.1.0 所记录的旧引擎协议缺口。

保留兼容性 Gate 的原因不是“已知不匹配”，而是 EmmsUI 使用 UE‑AS 手工 binding internals，源码信号无法证明全部 ABI、属性生成、热重载和 Cook 行为。

参阅 [版本兼容性](31-Version-Compatibility.md)。
