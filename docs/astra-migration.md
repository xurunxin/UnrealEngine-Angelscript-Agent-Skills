# Astra 技能结构优化

依据 OpenAI 文章 [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)，本次精简常驻 description、为多模式入口提供按需参考，并将流程中间产物与任务完成条件分开。技能继续跨模型使用，不硬编码模型分支。

15 个 SKILL.md 合计从 54,101 字节降至 41,993 字节（约 22.4%）；description 从 4,815 字符降至 1,917 字符（约 60.2%）。这些是文本规模，不是 token、延迟或成功率实测。

Router 不再要求重复填写 Route/Result；已授权实现路由后继续执行。Project Context 按 create/refresh/review 选择资料与变更范围，将完整采集流程移到参考。Reflection 将回调、Widget、默认值和结构热重载详细规则移到按需参考。其余专题保留具体 API 和 UE-AS/EmmsUI 不变量，缩短触发描述；不再强制所有小改动跑无关全量检查、创建团队 fork 或重复询问已授权保存。

保留的关键约束包括源码引擎基线、项目 ref 优先、反射消费者最小化、GC、结构性热重载、Editor/Cook 隔离、真实 client/server 验证、EmmsUI 状态/身份/Begin-End、缓存与可执行文件匹配。未修改上游 API 或兼容性锁。

实际静态验证：技能/frontmatter/链接校验、包结构与 SHA256SUMS、46 个路由及 10 个行为用例的格式/引用、源码引用格式、10 项 unittest、Python compileall 和 `git diff --check` 通过。发布索引与哈希使用现有 `generate_release_metadata.py` 按 0.3.0 / 2026-09-11 重生成。

用例覆盖清晰任务直达专题、跨域实现继续执行、上下文仅审查不写入、Timer 生命周期参考及按风险选验证。用例文件是后续模型评测输入；格式检查并未执行模型行为评测。当前无目标 UE-AS/EmmsUI checkout，因此源码路径存在性、引擎编译、PIE、Dedicated Server、热重载、Cook/Package、性能及多模型 A/B 均为 `not-run`。
