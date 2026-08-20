# 31. 版本兼容性

## 本包 0.1.1 锁定

| 源 | Commit | 日期 / 版本 |
|---|---|---|
| Docs | `3864c72fa3c1ef67413dfaad24417bad01879b4d` | 2026‑03‑23 |
| UE‑AS 引擎 | `546c4d6af141f1e820be1b2976211a756ca2639d` | 2026‑08‑14 |
| Unreal | 5.8.1 | `Engine/Build/Build.version` |
| EmmsUI | `c5d4e303f1fc8a1545de4d336be19e69dc8518c0` | 2026‑08‑12 |

## 修订后的兼容性结论

旧包 0.1.0 观察到的 UE‑AS 镜像尚未同步上游，因此错误地把 UE 5.5.4 与 2026‑08 EmmsUI 当成当前组合。该组合不再是用户当前基线。

当前事实：

- UE‑AS commit `1a06a2bf...` 引入新的 `Iterate()` iterator protocol、range-for 解析路径和原生/JIT 支持；
- EmmsUI commit `c9985c1...` 为 `FMMListViewIterator` 增加匹配的 `if_handle_then_const Iterate() const`；
- 两个 commit 都包含在当前锁定 head 中。

因此，当前组合应标记为：

```text
source-signals-aligned-runtime-unverified
```

它表示“已删除旧协议缺口警告”，而不是“已经通过目标项目兼容认证”。

## 为什么仍需兼容性 Gate

EmmsUI 紧密依赖 UE‑AS 手工 binding internals，例如：

- `FAngelscriptBinds`；
- `FAngelscriptTypeUsage`；
- template flags 与协变 `mm<T>`；
- `if_handle_then_const`；
- iterator protocol；
- UWidget 反射生成的属性和事件 API；
- Script docs metadata；
- 热重载对象替换通知。

这些不是普通稳定 UE API。iterator 对齐只覆盖其中一个高风险面。

## 当前同步带来的其他变化信号

- UE‑AS head 修复 soft hot reload 重复默认析构函数；
- Editor 目录脚本生成的 UASClass/UASStruct 能正确报告 Editor-only；
- BlueprintCallable/BlueprintEvent 参数名 `Self` 会在编译阶段报错；
- 当前 EmmsUI 包含 mutable input state 与 Editor Tab object reinstancing 修复。

这些变化应写入升级测试，不应被理解为无需测试。

## 兼容性探针

```bash
python tools/probe_compatibility.py \
  --engine-root <UE-AS> \
  --emmsui-root <EmmsUI> \
  --project-root <Project> \
  --json-out <Project>/Saved/ueas-compatibility.json
```

主要判断：

| 探针结果 | 含义 | 下一步 |
|---|---|---|
| `compat.iterator_protocol_aligned` | 双方发现新协议源码信号 | 运行最小 ListView 脚本编译 |
| `compat.iterator_protocol_engine_missing` | EmmsUI 新协议、引擎未发现 | 阻止默认集成，检查 commit/回移 |
| `compat.iterator_protocol_emmsui_legacy` | 引擎新协议、EmmsUI 可能旧 | 检查插件 iterator bind |
| `compat.known_source_aligned_pair` | 命中本包精确基线 | 仍继续运行全部 runtime gates |
| blocker | 缺 Build.version 或插件入口 | 先修安装/路径 |

静态扫描可能有假阴性或假阳性，不能替代编译器。

## 最小运行验证矩阵

1. **C++ build**：EmmsUI Runtime + Editor modules；
2. **Basic widget**：`UMMWidget::DrawWidget`；
3. **ListView**：`for (Entry : List)` 编译、可见项数量、滚动回收；
4. **TreeView**：children callback、展开、选择；
5. **Input**：EditableText、Slider、Checkbox 的用户值与程序值冲突；
6. **Tab reload**：打开 Tab 后改 class 字段/UFUNCTION，再热重载；
7. **Overlay**：BeginDrawViewportOverlay/EndDraw；
8. **Editor-only**：Editor 目录 class/struct 与 Blueprint；
9. **simulate-cooked**；
10. **Cook/Package**。

## 升级和回退策略

### 当前基线

优先固定本页精确 SHA，完成矩阵后把证据写入项目锁文件。不要在生产线上跟随浮动 `master`。

### 未来 UE‑AS 更新

先更新 UE‑AS，保持 EmmsUI SHA 不变，运行探针和 C++ build。再更新 EmmsUI，单独跑 List/Input/Tab 测试。

### 未来出现协议缺口

按顺序选择：

1. 找到双方共同通过的精确 SHA；
2. 固定较旧 EmmsUI；
3. 回移单个 EmmsUI 修复但保留匹配 iterator bind；
4. 最后才修改 UE‑AS/EmmsUI binding internals。

所有回移都要附编译和运行测试，不靠 commit 日期猜测。

## 项目记录矩阵

```text
UE-AS SHA | UE version | EmmsUI SHA | C++ build | basic | input | list | tree | tab reload | simulate-cooked | cook
```

每个 release 更新，并附日志、退出码和产物引用。
