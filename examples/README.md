# Examples

这些示例是根据官方语义重新编写的最小模式，不是上游源码复制。UE‑AS 和 EmmsUI API 会随 fork 变化，使用前：

1. 在目标 Editor 的 LSP/API Reference 确认类型与方法名；
2. 检查项目已有命名和基类；
3. 逐个保存编译；
4. 为项目行为补测试；
5. 运行 simulate-cooked。

目录：

- `Scripts/`：UE‑AS Gameplay、反射、网络、测试和 Editor；
- `EmmsUI/`：运行时 Widget、Overlay、Editor Tab、List；
- `CppBindings/`：自动绑定与 ScriptMixin 骨架；
- `EmmsUIExtension/`：新增 helper 的结构骨架。
