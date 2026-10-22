// --- Import React and ReactDOM ---
// 作用：从全局 React 对象中解构出 useState Hook，供后面的函数组件创建和管理状态
// 解释：本项目通过 CDN 引入 React，所有 API 都挂在全局 React 对象上；先解构出来，后面代码写起来更短
//       参考：React 官方文档 Hooks 一章中 useState 的用法示例
const { useState } = React;


// Counter Section Component
// 作用：定义"单个计数器面板"组件，包含名称标题和 增加 / 减少 / 重置 三个按钮
// 解释：Counter A 和 Counter B 的结构完全相同，抽成组件后复用同一份 UI，只靠 props 区分，
//       避免写两遍重复代码（组件化思想）
//       参考：老师课堂演示的 Counter 计数器示例
const CounterSection = ({ label, count, setCount }) => {
    return (
        <div className="counter-section">
            {/* 作用：用 h3 标题展示计数器名称（label）和当前数值（count） */}
            {/* 解释：label 和 count 都是父组件 App 通过 props 传进来的，本组件不自己保存数据；
                    参考：Movie Night Part 1 starter/app.js 中 Header 组件读取 props.title 的写法 */}
            <h3>{label}: {count}</h3>

            {/* 作用："增加"按钮，点击后调用 setCount 把当前计数 +1 */}
            {/* 解释：setCount 是父组件传进来的状态更新函数，只有调用它 React 才会重新渲染界面
                    （普通变量改了界面不会变，参考 Movie Night Part 2 Step 01 的实验）；
                    label.split(' ')[1] 把 "Counter A" 按空格切开取第二段，得到字母 "A" 拼进按钮文字 */}
            <button onClick={() => setCount(count + 1)}>+ Increment {label.split(' ')[1]}</button>

            {/* 作用："减少"按钮，点击后调用 setCount 把当前计数 -1 */}
            {/* 解释：与增加按钮同理，通过 props 拿到的更新函数修改状态；
                    参考：Movie Night Part 2 Step 06-07 中加减分的按钮写法 */}
            <button onClick={() => setCount(count - 1)}>- Decrement {label.split(' ')[1]}</button>

            {/* 作用："重置"按钮，点击后调用 setCount(0) 把该计数器归零 */}
            {/* 解释：直接传目标值 0 给更新函数，React 会用新值替换旧状态；
                    参考：Movie Night Part 2 Step 03 中 state 的初始化与更新写法 */}
            <button className="reset-button" onClick={() => setCount(0)}>Reset</button>
        </div>
    );
};


// Results Component
// 作用：定义"计算结果"组件，展示两个计数器的 加、减、乘、除 四种运算结果
// 解释：运算逻辑全部由 JS 表达式在 JSX 中直接算出，无需额外变量；
//       参考：实验要求（Exercise_LAB-INSTRUCTIONS.pdf）中四则运算展示的功能说明
const Results = ({ countA, countB }) => {
    return (
        <div className="results">
            <h2>Calculations</h2>

            {/* 作用：展示两个计数相加的结果 */}
            {/* 解释：JSX 花括号内可以写任意 JS 表达式，countA + countB 直接求值后显示；
                    参考：Movie Night Part 1 starter/app.js 中 { props.totalMovies } 的插值写法 */}
            <p>{countA} + {countB} = {countA + countB}</p>

            {/* 作用：展示两个计数相减的结果 */}
            {/* 解释：与加法同一模式，只换运算符，体现 JSX 中表达式插值的复用；
                    参考：同文件上一行加法结果的写法 */}
            <p>{countA} - {countB} = {countA - countB}</p>

            {/* 作用：展示两个计数相乘的结果 */}
            {/* 解释：乘法用 * 运算符，同样在 JSX 花括号内直接计算；
                    参考：同文件上方加减两行的写法 */}
            <p>{countA} * {countB} = {countA * countB}</p>

            {/* 作用：展示两个计数相除的结果；若除数为 0 则提示不能除以零，否则保留两位小数 */}
            {/* 解释：除法要先判断除数（countB）是否为 0，避免出现 Infinity 或 NaN，
                    用三元运算符做条件选择；toFixed(2) 把商保留两位小数
                    参考：JS 三元表达式与 Number.prototype.toFixed 的常用写法（MDN 文档） */}
            <p>{countA} / {countB} = {countB !== 0 ? (countA / countB).toFixed(2) :'Cannot divide by zero'}</p>
        </div>
    );
};


const App = () => {
// Initialize state for two counters
// 初始化两个计数器的状态
    // 作用：第一个计数器状态 countA，初始值为 0；setCountA 是更新它的函数
    // 解释：界面要随数据变化，必须把数据放进 state——普通变量改变不会触发重新渲染；
    //       useState 是函数组件里创建 state 的标准方式
    //       参考：Movie Night Part 2 Step 03（把 score 放进组件的 state）
    const [countA, setCountA] = useState(0);

    // 作用：第二个计数器状态 countB，初始值为 1
    // 解释：初始值设为 1 而不是 0，是为了让页面刚打开时除法运算不会出现"除以零"的提示；
    //       两个 state 各自独立，修改一个不会影响另一个
    //       参考：实验要求中"第二个计数器从 1 开始"的设定
    const [countB, setCountB] = useState(1); // Let's start the second one at 1 / 让第二个计数器从 1 开始

    // 作用：一键重置函数，把两个计数器同时恢复为 0
    // 解释：一个函数里调用两次 setCount，React 会合并这批状态更新，只重新渲染一次；
    //       参考：Movie Night Part 2 Step 09 中 App 组件里定义事件处理函数的写法
    const resetAll = () => {
        setCountA(0);
        setCountB(0);
    };

    return (
        <div>
            <h1>React Stateful Counter</h1>

            {/* 作用：页面顶部的"全部重置"按钮，点击后两个计数器同时归零 */}
            {/* 解释：onClick 直接绑定上面定义好的 resetAll 函数（传引用而不调用），
                    点击时 React 自动触发；参考：Movie Night Part 2 Step 04 处理点击事件 */}
            <button className="reset-all-button"
                onClick={resetAll}>Reset All
            </button>

            {/* 作用：把两个计数器面板并排排列的容器 */}
            {/* 解释：用 div 包裹并排布局，样式在 styles.css 的 .controls 中定义；
                    参考：styles.css 中 .controls 的注释说明 */}
            <div className="controls">
                {/* 作用：渲染计数器 A，把 countA 的状态和它的更新函数传给子组件 */}
                {/* 解释：state 定义在 App 里，通过 props 向下传递给 CounterSection，
                        子组件只能通过传下来的函数修改状态（单向数据流）；
                        参考：Movie Night Part 1 starter/app.js 中 App 向 Movie 传 props 的写法 */}
                <CounterSection
                    label="Counter A"
                    count={countA}
                    setCount={setCountA}
                />

                {/* 作用：渲染计数器 B，把 countB 的状态和它的更新函数传给子组件 */}
                {/* 解释：与计数器 A 完全相同的传参模式，只是换了数据源，体现组件复用；
                        参考：同文件上方 CounterSection A 的写法 */}
                <CounterSection
                    label="Counter B"
                    count={countB}
                    setCount={setCountB}
                />
            </div>

            {/* 作用：在页面底部展示两个计数器的四则运算结果 */}
            {/* 解释：把两个 state 作为 props 传给 Results 组件，由它负责计算和展示；
                    参考：同文件上方 Results 组件的定义 */}
            <Results countA={countA} countB={countB} />

        </div>
    );
};

// --- Render the App to the DOM ---
// --- 将 App 组件渲染到页面 DOM 中 ---
// 作用：获取 id 为 root 的 DOM 容器，作为 React 组件的挂载点
// 解释：React 组件必须挂载到一个真实的 DOM 节点上才能显示；
//       参考：index.html 中 <div id="root"></div> 的结构
const container = document.getElementById('root');

// 作用：用 React 18 的 createRoot 创建根节点
// 解释：React 18 起推荐用 createRoot 代替旧的 ReactDOM.render，支持并发特性；
//       参考：React 官方文档 createRoot 的升级说明
const root = ReactDOM.createRoot(container);

// 作用：把 App 组件渲染进根节点，页面随之显示计数器界面
// 解释：render 方法接收一个 JSX 元素，React 负责把它转换成真实 DOM；
//       参考：Movie Night Part 1 starter/app.js 文件末尾的渲染写法
root.render(<App />);
