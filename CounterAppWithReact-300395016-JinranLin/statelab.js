// --- Import React and ReactDOM ---
// --- 导入 React 和 ReactDOM ---
const { useState } = React;
// 从全局 React 对象中解构出 useState Hook，用于在函数组件中创建和管理状态


// Counter Section Component
// 计数器区域组件（单个计数器的显示与操作面板）
const CounterSection = ({ label, count, setCount }) => {
    return (
        <div className="counter-section">
            {/* 显示计数器名称和当前数值 */}
            <h3>{label}: {count}</h3>
            {/* 点击按钮时调用 setCount，将当前计数 +1（增加） */}
            <button onClick={() => setCount(count + 1)}>+ Increment {label.split(' ')[1]}</button>
            {/* 点击按钮时调用 setCount，将当前计数 -1（减少） */}
            <button onClick={() => setCount(count - 1)}>- Decrement {label.split(' ')[1]}</button>
            {/* 点击按钮时调用 setCount，将计数重置为 0 */}
            <button className="reset-button" onClick={() => setCount(0)}>Reset</button>
        </div>
    );
};


// Results Component
// 计算结果组件（展示两个计数器的加减乘除运算结果）
const Results = ({ countA, countB }) => {
    return (
        <div className="results">
            <h2>Calculations</h2>
            {/* 两个计数相加的结果 */}
            <p>{countA} + {countB} = {countA + countB}</p>
            {/* 两个计数相减的结果 */}
            <p>{countA} - {countB} = {countA - countB}</p>
            {/* 两个计数相乘的结果 */}
            <p>{countA} * {countB} = {countA * countB}</p>
            {/* 两个计数相除的结果；若除数为 0 则提示不能除以零，否则保留两位小数 */}
            <p>{countA} / {countB} = {countB !== 0 ? (countA / countB).toFixed(2) :'Cannot divide by zero'}</p>
        </div>
    );
};


const App = () => {
// Initialize state for two counters
// 初始化两个计数器的状态
    // 第一个计数器状态 countA，初始值为 0；setCountA 用于更新它
    const [countA, setCountA] = useState(0);
    // 第二个计数器状态 countB，初始值为 1（从 1 开始，避免初始除法出现除以零）
    const [countB, setCountB] = useState(1); // Let's start the second one at 1 / 让第二个计数器从 1 开始

    // 一键重置函数：将两个计数器都恢复为 0
    const resetAll = () => {
        setCountA(0);
        setCountB(0);
    };

    return (
        <div>
            <h1>React Stateful Counter</h1>

            {/* 页面顶部的“全部重置”按钮，点击后两个计数器同时归零 */}
            <button className="reset-all-button" 
                onClick={resetAll}>Reset All
            </button>

            {/* 两个计数器面板并排排列 */}
            <div className="controls">
                {/* 计数器 A：把 countA 状态和它的更新函数传给子组件 */}
                <CounterSection
                    label="Counter A"
                    count={countA}
                    setCount={setCountA}
                />
                {/* 计数器 B：把 countB 状态和它的更新函数传给子组件 */}
                <CounterSection
                    label="Counter B"
                    count={countB}
                    setCount={setCountB}
                />
            </div>
            
            {/* 底部展示两个计数器的四则运算结果 */}
            <Results countA={countA} countB={countB} />
            
        </div>
    );
};

// --- Render the App to the DOM ---
// --- 将 App 组件渲染到页面 DOM 中 ---
// 获取 id 为 root 的 DOM 容器
const container = document.getElementById('root');
// 创建 React 18 的根节点
const root = ReactDOM.createRoot(container);
// 把 App 组件渲染进根节点，页面随之显示
root.render(<App />);
