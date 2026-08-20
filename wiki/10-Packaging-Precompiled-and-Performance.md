# 10. 发布、预编译与性能

## 发布链

```text
Script source
  ├─ Development: runtime compile + hot reload
  ├─ Precompiled cache: PrecompiledScript.Cache
  └─ Optional generated/JIT C++: AS_JITTED_CODE
```

## 预编译缓存

典型生成参数：

```text
-as-generate-precompiled-data
```

官方文档强调缓存与生成它的 executable 严格匹配。任何引擎/项目 C++、绑定或 ABI 变化都应重新生成。

缓存模式通常不再读取脚本源，适合受控构建。开发中 `-as-development-mode` 可绕过缓存。

## Build.cs

使用生成 C++ 时，目标 module 需要 `AngelscriptCode` 依赖。具体生成文件接入方式以目标 commit 为准。

## 当前 5.8.1 基线的性能变化

当前 UE‑AS 同步包含新 iterator protocol 的 StaticJIT 支持，以及若干转译代码生成、非空值跟踪、delegate/TMap 和二进制尺寸优化。这些改进意味着旧版本的性能结论不能直接套到当前 head。

仍然必须：

- 在目标配置 Profile；
- 记录解释执行、预编译缓存和转译/JIT 的实际模式；
- 重新生成与 executable 匹配的缓存；
- 不把“上游有优化提交”写成项目已经变快的证据。

## 发布检查

- 版本锁；
- Clean C++ build；
- Unit/Integration；
- simulate-cooked；
- Cook；
- Package；
- 缓存生成；
- Package 启动并确认加载缓存；
- 无脚本源环境测试；
- Dedicated Server；
- 平台 smoke。

## 性能层级

### 先修结构

- 去无条件 Tick；
- 事件驱动；
- 缓存查找；
- 降低容器 churn；
- 避免反复字符串→FName；
- 数据批处理。

### 再看脚本热点

Profile 决定是否：

- 改算法；
- C++ Mixin；
- C++ 数据结构；
- 转译/JIT；
- 并行/任务系统。

不要因为脚本“可能慢”把所有 Gameplay 提前下沉 C++。

## Development-only 副作用

项目设置可把 Development-only 函数参数强制为 const，以捕获：

```angelscript
check(Inventory.Remove(Item)); // 错：Release 可能不执行
```

应写：

```angelscript
bool bRemoved = Inventory.Remove(Item);
check(bRemoved);
```

## EmmsUI

Draw 逻辑每帧执行。Widget 复用不代表 Draw 业务免费。大列表必须虚拟化，异步加载不要每帧重新请求，昂贵筛选只在查询变化时执行。

新 iterator protocol 只改变遍历协议，不会自动消除 Entry Draw 的业务成本。分别 Profile：

- list regeneration；
- 可见 Entry 数；
- Draw 时间；
- UWidget rebuild；
- UObject/Slate 分配与 GC。
