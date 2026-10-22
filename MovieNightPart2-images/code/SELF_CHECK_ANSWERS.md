# Movie Night — Part 2: Step 14 Self-Check 问答与中文注释解析

本文档整理了教程 **Step 14 — Wrap-up and self-check**（第 29–31 页）中的 10 道自测题、标准答案及详细中文解析。

---

### 1. In Step 01 the variable reached 8 but the page showed 5. Give both reasons.
- **English Answer**: React was never told that anything changed, so it did not re-render, and even if it had, `let score = props.score` would have run again and reset the value to 5.
- **中文作答与注释**：
  1. 普通局部变量不受 React 监控，修改 `score` 不会通知 React 触发组件重新渲染（re-render），所以界面保持原样；
  2. 即使触发了重新渲染，函数组件重新执行时也会再次运行 `let score = props.score`，把 `score` 重置回初始值 `5`。

### 2. What is the difference between `this.props.score` and `this.state.score` inside `Rating` in Step 03? Which one does the page show?
- **English Answer**: `this.props.score` is the value the parent passed in, and here it is only used as the starting value. `this.state.score` is the component's own value, which changes with `setState()`. The page shows `this.state.score`.
- **中文作答与注释**：
  - `this.props.score` 是父组件传递进来的只读属性，在 Step 03 中仅作为初始化 `state` 的起始值；
  - `this.state.score` 是组件自己拥有并维护的状态，可以通过 `this.setState()` 动态修改；
  - 页面渲染显示的是 `this.state.score`。

### 3. Why does `onClick={this.incrementScore()}` print the message when the page loads, and not when you click?
- **English Answer**: The parentheses call the function immediately while the JSX is being built, once per `Rating`. `onClick` receives its return value, `undefined`, so there is nothing to call on click.
- **中文作答与注释**：
  - 加上括号 `()` 会在构建/渲染 JSX 时**立即调用**该函数（每个 `Rating` 组件渲染时都会执行一次）；
  - `onClick` 实际接收到的是函数的返回值 `undefined`，因此后续真正点击按钮时没有任何函数可执行。

### 4. Why was `this` undefined in Step 05, and why does `incrementScore = () => { ... }` fix it?
- **English Answer**: React calls the handler as a plain function, not as a method of the component, so `this` is lost. An arrow function has no `this` of its own; as a class property, it captures the component instance permanently.
- **中文作答与注释**：
  - 当点击事件触发时，React 是将事件处理函数作为普通函数独立调用的，而不是通过组件对象调用（即不是 `rating.incrementScore()`），因此在严格模式下普通方法里的 `this` 会丢失并变为 `undefined`；
  - 箭头函数没有自己的 `this`，作为类属性定义时，它会永久捕获外层词法作用域（即当前组件实例）的 `this`。

### 5. Two calls of `this.setState({ score: this.state.score + 1 })` add only 1. Why? What should you write instead?
- **English Answer**: Updates can be batched, so both calls read the same old `this.state.score`. Use the function form: `this.setState(prevState => ({ score: prevState.score + 1 }))`.
- **中文作答与注释**：
  - React 会对状态更新进行批处理（batching），连续两次对象形式的 `setState` 都会读取同一个尚未更新的 `this.state.score`；
  - 应改用函数式更新：`this.setState(prevState => ({ score: prevState.score + 1 }))`，确保每次都基于最新的前一个状态 `prevState` 计算。

### 6. Name three differences between props and state.
- **English Answer**:
  1. Props come from the parent, while state is owned by the component.
  2. Props are read-only to the component, while state changes through `setState()` (or a `useState` setter).
  3. Props configure a component, while state remembers changes over time. (Also: one component's state is often passed to its children as props.)
- **中文作答与注释**：
  1. **来源不同**：`props` 由父组件传入，而 `state` 由组件自身拥有和管理；
  2. **可变性不同**：`props` 在组件内部是只读的（不可修改），而 `state` 可以通过 `setState()` / `useState` 更新函数进行修改；
  3. **用途不同**：`props` 用于配置组件和向下传递数据，而 `state` 用于记录随时间或用户交互而变化的数据。

### 7. Why does the list of movies live in `App` and not in `Movie`?
- **English Answer**: The `Header`, the list and the `Footer` all need it, and `App` is their closest common parent. Data can only be passed down, so it must live above everything that uses it.
- **中文作答与注释**：
  - `Header`（电影总数与平均分）、电影列表以及 `Footer`（已观看计数）都需要依赖电影数组数据；
  - React 中数据遵循自顶向下的单向数据流（只能通过 `props` 向下传递），因此共享状态必须存放在所有使用该数据的组件的**最近公共父组件** `App` 中。

### 8. `Movie` cannot change `App`'s state, yet clicking ✖ in a `Movie` removes it. How?
- **English Answer**: `App` passes a function (`handleRemoveMovie`) down as a prop. `Movie` calls it with its `id`, and the function, which belongs to `App`, calls `App`'s `setState()`.
- **中文作答与注释**：
  - **数据向下流，事件向上流**：`App` 将定义在自己内部的 `handleRemoveMovie` 函数作为 `prop`（`removeMovie`）向下传给 `Movie`；
  - 当点击 `✖` 时，`Movie` 调用 `props.removeMovie(props.id)` 将自己的 `id` 传回给 `App` 的方法，由 `App` 自己调用 `setState()` / `setMovies()` 更新状态。

### 9. Why is `averageRating` computed in `render()` instead of being kept in state?
- **English Answer**: It can be calculated from `movies`. Storing it as well would create a second copy that must be kept in sync by hand. Computing it in render means it can never be wrong.
- **中文作答与注释**：
  - `averageRating`（以及 `watchedCount`）完全可以由 `movies` 数组直接计算得出（属于派生数据 Derived State）；
  - 如果把它也单独放进 `state`，就会产生两份冗余数据，每次增删电影或修改评分都必须手动同步，容易出错；在渲染时实时计算能保证永远保持一致。

### 10. What is wrong with `prevState.movies.push(newMovie)` inside `setState()`?
- **English Answer**: `push()` changes the existing array in place. State must be replaced with a new array, for example `[...prevState.movies, newMovie]`, so React can see that it changed.
- **中文作答与注释**：
  - `push()`（以及 `splice()` 等原地修改方法）会直接修改原数组（mutate state in place），破坏了 React 状态的不可变性（Immutability），可能导致 React 无法检测到变化或引发渲染异常；
  - 正确做法是使用 `filter()`、`map()` 或展开运算符 `[...prevState.movies, newMovie]` 创建一个**新数组**来替换旧状态。
