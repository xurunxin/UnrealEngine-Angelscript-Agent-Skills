# 项目证据采集

## 工作流

### 1. 确定唯一项目根

查找 `.uproject`，同时记录工作区边界。

- 找到一个：以它的父目录为项目根。
- 找到多个：列出候选及证据，停止自动选择；除非用户或已有项目配置明确指定。
- 找不到：报告缺失，不把任意 `Script/` 或 `Content/` 目录当项目根。

不得按“最近修改”“目录名最像”或第一个搜索结果静默选择。

### 2. 识别实际 Unreal 源码构建

读取：

- `.uproject` 的 `EngineAssociation`；
- `<Engine>/Engine/Build/Build.version`；
- 引擎 Git branch、commit、dirty 状态（可用时）；
- 项目脚本、构建脚本或环境文件中明确记录的 Engine root。

确认这是包含 UE-AS 修改的源码引擎，而不是仅根据目录名推断。记录引擎路径时允许在共享
文档中使用占位符或相对描述，避免泄露私有绝对路径。

### 3. 识别 UE-AS 插件与源码 ref

优先核对：

```text
<Engine>/Engine/Plugins/Angelscript/Angelscript.uplugin
<Engine>/Engine/Plugins/Angelscript/Source/
```

记录插件来源、实际 commit、是否 dirty、主要模块和版本敏感信号。若项目另有同名插件，
必须报告重复来源，不能假定哪一个生效。

### 4. 识别 EmmsUI

在项目与引擎插件目录中查找 `EmmsUI.uplugin`，记录：

- 生效位置与是否存在重复副本；
- Git ref/commit 与 dirty 状态；
- Runtime/Editor 模块；
- 项目是否实际启用；
- ListView、mutable input、Editor Tab reinstancing 等版本敏感能力的源码证据。

源码能力存在只写 `source-signal-present`；完成目标项目编译和 smoke 后才能写 `passed`。

### 5. 扫描项目结构

读取并归纳：

- `.uproject` 模块和插件；
- `Source/**/*.Build.cs`、`*.Target.cs`；
- 项目与插件 `Script/` 目录、额外 Script roots；
- `Config/*.ini` 中 Angelscript、测试、地图和 Cook 相关设置；
- 自定义插件、Editor 模块和 ThirdParty 模块；
- 现有 `AGENTS.md`、编码规范、测试说明与版本锁。

只记录会改变实现、路由或验收的事实，不把所有文件清单灌入上下文。

### 6. 识别 C++ Binding 边界

搜索项目模块中与以下内容相关的实现：

```text
FAngelscriptBinds
ScriptMixin
AngelscriptCode
AngelscriptBinds
AS_FORCE_LINK
```

记录 Binding 所属模块、初始化顺序、Runtime/Editor 边界和已有测试。不要因为某个原生 API
在脚本中不可见就立即设计手工绑定；先确认自动反射或 Mixin 是否已经覆盖。

### 7. 记录项目约定与风险

至少覆盖：

- 反射默认策略和 Blueprint 边界；
- Soft/Structural Hot Reload 的允许范围；
- 网络拓扑、Authority 和 Dedicated Server 要求；
- EmmsUI 的使用位置与 Widget identity 约束；
- Cook/Package、Static JIT、Precompiled Script 的发布 Gate；
- 当前已知 Blocker 与人工决定。

不能从代码可靠推断的团队约定标为 `unknown`，不虚构。

### 8. 写入上下文

使用模板生成小而可维护的文件。每个可变事实至少包含：

```yaml
value: ""
status: confirmed | inferred | unknown | stale
source: "file/ref/tool observation"
observed_at: "YYYY-MM-DD"
```

对路径和 commit 使用可复制值；对兼容性使用分层状态：

```text
not-checked
source-signals-aligned
build-passed
script-compile-passed
runtime-smoke-passed
cook-passed
package-launch-passed
```

不得跨级推断。
