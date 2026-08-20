# 07. 热重载与状态

## 两类修改

### 非结构性

- 函数体；
- 局部控制流；
- 普通算法；
- 日志；
- 不改变签名的 helper。

通常可在 PIE 中做 soft hot reload，但仍应观察异常、重复 Timer/Delegate 与运行状态。

### 结构性

- 新增/删除/重命名字段；
- 改字段类型；
- 改继承；
- 改 UPROPERTY/UFUNCTION；
- 改 RPC/Delegate 签名；
- 改默认组件；
- 改 class/struct 名；
- 改 Blueprint 可见 API。

可能触发类型重实例化、Blueprint 重编译、对象替换和状态迁移。

## 当前基线变化

UE‑AS `546c4d6...` 修复了 soft hot reload 可能重复生成默认析构函数的问题。EmmsUI `c5d4e30...` 改善了打开中的 `UMMEditorUtilityTab` 在脚本对象重实例化后的引用更新。

这两项修复只缩小已知故障面：

- 不保证任意结构改动都能无损迁移状态；
- 不保证旧 Delegate/Timer/Slate 引用自动清理；
- 不保证 Blueprint、资产默认值或网络对象状态正确；
- 不应把当前 head 的修复反推到项目的旧锁定 commit。

## 状态分类

| 状态 | 应放位置 |
|---|---|
| 资产默认值 | UPROPERTY/default |
| 运行时权威状态 | Actor/Component/Subsystem/Model |
| 可恢复缓存 | 普通脚本成员 |
| UI 输入 | Widget/ViewModel 持久成员 |
| Editor 关卡对象引用 | Weak |
| 跨地图资产 | Soft |
| 临时 Draw 值 | 局部 |

## 安全迭代

1. 小步修改；
2. 函数体与结构改动分开；
3. 结构改动前退出 PIE；
4. 重要资产保存前备份/版本控制；
5. 修改后检查实例默认值和 BP 子类；
6. Editor Tab/Delegate 检查旧对象；
7. 必要时完整重启 Editor。

## 脚本热重载 vs C++ Live Coding

UE‑AS 脚本热重载由项目专门支持。C++ Live Coding 对 UCLASS/UPROPERTY 布局和 CDO 的风险是另一套问题。修改 EmmsUI 或 UE‑AS C++ 反射结构时，按 Unreal C++ 安全流程完整构建/重启，不要因为脚本热重载可靠就推广到 C++。

## EmmsUI

Draw 函数更新通常非常适合热重载。风险来自：

- Tab 对象被重实例化；
- 旧 Slate Tab 仍引用旧对象；
- Strong 引用阻止销毁；
- 字段结构改变后 UI state 迁移；
- Delegate 重复绑定；
- 同类型 sibling 顺序改变导致焦点/选择映射变化。

当前锁定 EmmsUI 已包含 Tab object reinstancing 修复，但仍要在**打开 Tab 的状态下**测试非结构性和结构性两类修改。

## 验证清单

- 当前实例是否保留；
- 新字段默认值是否正确；
- Blueprint 子类是否 dirty/compile；
- Delegate 触发次数；
- Timer 是否重复；
- Editor Tab 是否只有一个；
- Tab 是否引用新脚本对象；
- UI 焦点/选择；
- 网络对象 Role/Owner；
- 退出 PIE 后对象是否释放；
- 完整 Editor 重启后是否仍正确。
