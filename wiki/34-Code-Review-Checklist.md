# 34. 代码审查清单

## 版本

- [ ] Unreal 版本；
- [ ] UE‑AS SHA；
- [ ] EmmsUI SHA；
- [ ] 新 API 在目标版本存在；
- [ ] iterator protocol 双方信号一致；
- [ ] “source aligned” 未被误写成“runtime passed”；
- [ ] 锁文件更新。

## UE‑AS

- [ ] 无 C++ 指针/箭头误用；
- [ ] `float` 精度明确；
- [ ] 普通成员/函数未过度反射；
- [ ] 默认值使用 initializer/default；
- [ ] DefaultComponent 声明正确；
- [ ] BP Hook 不可跳过不变量；
- [ ] BlueprintCallable/BlueprintEvent 参数未命名为 `Self`；
- [ ] Delegate/Timer handler 为 UFUNCTION；
- [ ] World Context 有效；
- [ ] Editor-only 隔离；
- [ ] 结构性热重载风险说明。

## 网络

- [ ] Authority；
- [ ] Ownership；
- [ ] Reliable/Unreliable；
- [ ] 晚加入；
- [ ] OnRep；
- [ ] Dedicated tests。

## EmmsUI

- [ ] Begin/End；
- [ ] 状态持久；
- [ ] Slot 顺序；
- [ ] 同类型 sibling 身份；
- [ ] Was/On 语义；
- [ ] List virtualization；
- [ ] Draw 无重任务；
- [ ] UnderlyingWidget 生命周期；
- [ ] Weak editor refs；
- [ ] rebuild 属性频率；
- [ ] 目标 iterator protocol；
- [ ] ListView range-for 有真实编译/滚动证据；
- [ ] Editor Tab 结构性热重载有对象替换证据。

## 测试

- [ ] Unit；
- [ ] Integration；
- [ ] simulate-cooked；
- [ ] C++ build；
- [ ] Cook/Package；
- [ ] Hot reload；
- [ ] Editor restart；
- [ ] 实际退出码、日志和产物记录。

## 文档

- [ ] 公共 API；
- [ ] 非直观约束；
- [ ] 版本依赖；
- [ ] 回滚；
- [ ] 上游来源。
