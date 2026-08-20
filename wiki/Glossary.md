# Glossary

**UE‑AS**  
Hazelight 的 UnrealEngine‑Angelscript，引擎修改 + 插件 + 定制 AngelScript。

**Structural change**  
改变类型布局、反射签名、继承、组件等，需要重实例化的修改。

**Reinstancing**  
用新脚本类版本替换已有 UObject 实例，并迁移引用/状态的过程。

**CDO**  
Class Default Object，Unreal 类默认值来源。

**Reflection surface**  
进入 Unreal 反射系统的属性、函数和类型集合。

**Automatic binding**  
通过 UHT 反射自动生成脚本 API。

**ScriptMixin**  
把 C++ 静态函数库绑定成脚本类型实例方法。

**PrecompiledScript.Cache**  
由匹配 executable 生成的脚本预编译缓存。

**simulate-cooked**  
去除 Editor-only API 后的脚本编译模拟，不等于完整 Cook。

**Immediate mode UI**  
每轮通过控制流声明 UI，而不是长期操作控件引用的 API 风格。

**Retained mode UI**  
框架保留控件对象与树，调用方增删和更新对象。

**EmmsUI**  
即时式声明 API，但底层保留并复用 UMG Widget 的混合实现。

**`mm<T>`**  
EmmsUI 对底层 UWidget element 的脚本 Handle。

**Pending attribute**  
本次 Draw 声明要应用的属性。

**Mirrored value**  
从真实 UWidget 读取、用于双向输入协调的值。

**Widget identity**  
EmmsUI 判断本轮节点与上一轮哪个节点对应的键。

**Draw cycle**  
一次 BeginDraw/Draw/EndDraw 或 UMMWidget 调用。

**`WasX`**  
按 Draw 周期消费的事件触发查询。

**`OnX`**  
绑定到真实 UMG delegate 的即时回调。

**SlateIM**  
Epic 的实验性 Slate 即时式包装，官方定位偏调试工具。
