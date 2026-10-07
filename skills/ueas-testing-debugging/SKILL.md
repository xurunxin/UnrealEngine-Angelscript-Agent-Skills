---
name: ueas-testing-debugging
description: Use when diagnosing UE-AS failures or building tests and CI evidence. Do not use as the primary skill for feature implementation.
metadata:
  version: "0.3.0"
  language: zh-CN
  owner: xurunxin
---

# UE‑AS Testing and Debugging

## 测试层级

### 单元测试

文件约定 `Feature_Test.as`：

```angelscript
void Test_ClampHealth(FUnitTest& T)
{
    FHealthState State;
    State.Current = 125.0;
    State.Maximum = 100.0;

    Health::Clamp(State);

    T.AssertEquals(100.0, State.Current);
}
```

单元测试随脚本热重载运行，也可由 Automation/命令行运行。纯规则优先放到可单测的普通函数。

### 集成测试

`IntegrationTest_Name(FIntegrationTest& T)` 配合测试地图。用于生命周期、World、网络和异步流程。默认 client/dedicated-server 模型是有价值的压力，不要随意关闭。

### Cook 编译门

```powershell
UnrealEditor-Cmd.exe "<Project>.uproject" `
  -unattended -nop4 -nosplash `
  -as-simulate-cooked -run=AngelscriptTest
```

这一步捕获 Editor-only 泄漏，但不等价于完整 Cook/Package。

## 推荐 CI 阶段

1. 脚本编译 + UnitTests；
2. simulate-cooked；
3. IntegrationTests；
4. C++ 编译；
5. Cook/Package smoke；
6. 项目需要时生成覆盖率。

命令参数以目标分支的 Automation 测试名称为准；官方旧文档中可能仍出现 `UE4Editor-Cmd.exe`，UE5 使用 `UnrealEditor-Cmd.exe`。

## 覆盖率

通过 Project Settings 或 `-as-enable-code-coverage` 开启，报告写入 `Saved/CodeCoverage`。覆盖率会增加启动成本，CI 独立 Job 使用，不建议所有本地启动常开。

## 调试

官方 VS Code 扩展：

- Editor 运行时建立连接；
- 保存即编译/热重载；
- F5 连接 Debug Adapter；
- 断点、单步、变量查看；
- 脚本异常时自动暂停。

异常诊断时记录：

- 完整脚本栈；
- 当前 World/NetMode；
- 热重载前后类型版本；
- 是否在 Editor-only 路径；
- 是否由自动求值/调试器访问器触发。

## Agent 工作流

- 用失败日志或可复现案例定位；适合自动化的缺陷补充回归测试；
- 先运行覆盖受影响行为的检查；只有跨模块风险、相关失败或项目 CI 要求时扩展到全量验证；
- 不把输出日志中出现测试名当作通过；
- 保存实际退出码和失败列表；
- 无法运行 Editor 时明确标记“仅静态审查”，不要伪造结果。

## 完成标准

至少包含一个可复现测试或明确说明为何当前改动只能通过集成/Cook 验证。
