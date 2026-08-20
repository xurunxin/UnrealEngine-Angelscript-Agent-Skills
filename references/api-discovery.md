# API Discovery Workflow

## 1. 项目内搜索

```text
目标类型名
目标函数的脚本名
对应 C++ 名
UFUNCTION/UPROPERTY
同类测试
```

项目代码是最可信用法。

## 2. LSP

- completion；
- hover；
- go to definition；
- find references；
- signature help；
- Problems；
- API Reference link。

Editor 必须运行才能获得全部绑定信息。

## 3. 官方 Script API Reference

网站首页提供当前生成 API，但它可能对应官方最新构建，不一定是项目 fork。用来发现候选，再在目标 Editor 验证。

## 4. C++ 反射

检查：

- UCLASS/USTRUCT；
- BlueprintType；
- UFUNCTION；
- UPROPERTY；
- Script metadata；
- Deprecated；
- 参数类型；
- module dependency。

## 5. Bind Database / settings

名称可能经过 ScriptName、prefix/suffix stripping、项目 naming data。检查 `UAngelscriptSettings` 和 Bind Database。

## 6. 手工 binding

搜索：

```text
FAngelscriptBinds
AS_FORCE_LINK
ExistingClass
ValueClass
GenericMethod
PreviousBindPassScriptFunctionAsFirstParam
```

## 7. 最小编译探针

不要在主功能中试错。建立一段最小 `.as`，只引用目标 API，保存并记录 Editor 诊断。

## 禁止

- 从普通 AngelScript API 猜 UE‑AS；
- 从 C++ 名直接机械转换；
- 从最新网站推断旧 fork；
- 只看 IDE 语法高亮；
- 遇到不可见 API立即写手工 binding。
