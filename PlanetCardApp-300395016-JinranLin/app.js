// 作用：八大行星数据源——数组，每颗行星包含 id、名称、直径、卫星数、简介和图片路径
// 解释：把数据（planets）和界面（组件）分开，之后改数据不用动组件代码，
//       这是 React"数据驱动视图"的基础；数组中每个对象的字段与下方 Planet 组件里
//       planet.xxx 的读取一一对应
//       参考：老师提供的光盘文件 planets-starter.zip 中的原始数据
const planets = [
  {
    id: '1',
    name: 'Mercury',
    diameter: '3,031.67 mi',
    moons: 'none',
    desc: 'Mercury is the closest planet to the Sun. Due to its proximity, it\'s not easily seen except during twilight. For every two orbits of the Sun, Mercury completes three rotations about its axis. Up until 1965 it was thought that the same side of Mercury constantly faced the Sun.',
    url: 'img/mercury.jpg'
  },
  {
    id: '2',
    name: 'Venus',
    diameter: '7,521 mi',
    moons: 'none',
    desc: 'Venus is the second planet from the Sun and is the second brightest object in the night sky after the Moon. Venus is the second largest terrestrial planet and is sometimes referred to as the Earth’s sister planet due the their similar size and mass.',
    url: 'img/venus.jpg'
  },
  {
    id: '3',
    name: 'Earth',
    diameter: '7,917.5 mi',
    moons: '1',
    desc: 'Earth is the third planet from the Sun and is the largest of the terrestrial planets. The Earth is the only planet in our solar system not to be named after a Greek or Roman deity. The Earth was formed approximately 4.54 billion years ago and is the only known planet to support life.',
    url: 'img/earth.jpg'
  },
  {
    id: '4',
    name: 'Mars',
    diameter: '4,212 mi',
    moons: '2',
    desc: 'The fourth planet from the Sun and the second smallest planet in the solar system. Mars is often described as the "Red Planet" due to its reddish appearance. It\'s a terrestrial planet with a thin atmosphere composed primarily of carbon dioxide.',
    url: 'img/mars.jpg'
  },
  {
    id: '5',
    name: 'Jupiter',
    diameter: '86,881.4 mi',
    moons: '79',
    desc: 'The planet Jupiter is the fifth planet out from the Sun, and is two and a half times more massive than all the other planets in the solar system combined. It is made primarily of gases and is therefore known as a "gas giant".',
    url: 'img/jupiter.jpg'
  },
  {
    id: '6',
    name: 'Saturn',
    diameter: '72,367.4 mi',
    moons: '62',
    desc: 'Saturn is the sixth planet from the Sun and the most distant that can be seen with the naked eye. Saturn is the second largest planet and is best known for its fabulous ring system that was first observed in 1610 by the astronomer Galileo Galilei.',
    url: 'img/saturn.jpg'
  },
  {
    id: '7',
    name: 'Uranus',
    diameter: '31,518 mi',
    moons: '27',
    desc: 'Uranus is the seventh planet from the Sun. While being visible to the naked eye, it was not recognised as a planet due to its dimness and slow orbit. Uranus became the first planet discovered with the use of a telescope.',
    url: 'img/uranus.jpg'
  },
  {
    id: '8',
    name: 'Neptune',
    diameter: '30,599 mi',
    moons: '14',
    desc: 'Neptune is the eighth planet from the Sun making it the most distant in the solar system. This gas giant planet may have formed much closer to the Sun in early solar system history before migrating to its present position.',
    url: 'img/neptune.jpg'
  },
];

// =============================================================
//   WRITE YOUR CODE BELOW
//   在下方编写你的代码（代码补全部分）
// =============================================================

// 1: Create a 'Planet' component that renders a planet card
//    任务 1：创建一个渲染行星卡片的 'Planet' 组件
// 作用：定义单张行星卡片组件，接收父组件传入的一颗行星数据（planet）和删除回调（onRemove）
// 解释：一个组件只负责"一张卡片"，8 颗行星复用同一个组件，避免重复写 8 遍 HTML；
//       组件的输入全部来自 props，自己不存数据（纯展示 + 回调上报）
//       参考：Movie Night Part 1 starter/app.js 中 Movie 组件按 props 渲染一部电影的结构
function Planet({ planet, onRemove }) {
  // 作用：planet 是单颗行星的数据对象；onRemove 是父组件传下来的删除回调函数
  // 解释：用对象解构的写法从 props 里取字段，比 props.planet / props.onRemove 更短；
  //       参考：Movie Night Part 1 starter/app.js 中 const Movie = (props) => 的 props 传参方式
  return (
    <div className="card">
      {/* 作用：行星图片区域——用黑色背景衬托星球照片，图片地址来自数据里的 url 字段 */}
      {/* 解释：img 的 src 直接绑定 planet.url，换图片只改数据不改组件；
              参考：html-template.html 中静态卡片的 <img src="img/mercury.jpg"> 结构 */}
      <div>
        <img src={planet.url} alt={planet.name} />
      </div>

      {/* 作用：行星名称标题，内容来自 planet.name */}
      {/* 解释：alt 属性与名称保持一致，图片加载失败时也能显示文字，利于无障碍访问；
              参考：html-template.html 中的 <h2>Mercury</h2> */}
      <h2>{planet.name}</h2>

      {/* 作用：行星简介文字，内容来自 planet.desc */}
      {/* 解释：desc 是数据里的长文本，直接插值即可自动换行显示；
              参考：html-template.html 中卡片里的简介段落 */}
      <p>{planet.desc}</p>

      <h3>Planet Profile</h3>

      {/* 作用：行星档案列表——展示直径与卫星数量两项数据 */}
      {/* 解释：ul/li 是语义化的列表结构，比纯文字更清晰；
              strong 标签让"Diameter:""Moons:"这类标签加粗突出；
              参考：html-template.html 中的 <ul><li><strong>Diameter:</strong> ... */}
      <ul>
        <li>
          <strong>Diameter:</strong> {planet.diameter}
        </li>
        <li>
          <strong>Moons:</strong> {planet.moons}
        </li>
      </ul>

      {/* 作用：删除按钮——点击时调用 onRemove，并把当前行星的 id 传出去 */}
      {/* 解释：卡片自己不知道"怎么删"，只负责把 id 报告给父组件（状态在父组件里），
              这是"状态提升"的典型用法；箭头函数保证点击时才取到最新 id
              参考：Movie Night Part 2 Step 10 中删除电影按钮的写法 */}
      <button className="remove-btn" onClick={() => onRemove(planet.id)}>
        Remove
      </button>
    </div>
  );
}

// 2: Create a container component that iterates over the planets array
//    and renders a 'Planet' component for each object in the array
//    任务 2：创建一个容器组件，遍历行星数组，为每个行星对象渲染一个 'Planet' 组件
// 作用：容器组件 PlanetList——持有行星列表状态，负责遍历渲染所有卡片，并处理删除与重置
// 解释：把"数据存在哪、怎么增删"集中在容器组件，展示型子组件保持简单，
//       父组件通过 props 把数据和回调传下去
//       参考：Movie Night Part 2 Step 09-10 中 App 组件管理电影列表的写法
function PlanetList() {
  // 作用：用 useState 把初始行星数组存进组件状态，planetList 是当前显示的行星列表
  // 解释：放进 state 后，每次增删行星 React 都会自动重新渲染列表；
  //       初始值直接取上面定义好的 planets 常量
  //       参考：Movie Night Part 2 Step 03（state = { score: this.props.score } 的初始化思路）
  const [planetList, setPlanetList] = React.useState(planets);

  // 作用：删除指定 id 的行星——用 filter 过滤掉被点击的那颗，得到新数组并更新状态
  // 解释：filter 返回新数组而不是修改原数组，符合 React"不可变更新"的要求；
  //       条件 planet.id !== id 表示"保留 id 不等于传入 id 的行星"
  //       参考：Movie Night Part 2 Step 10 中 handleRemoveMovie 的 filter 写法
  function removePlanet(id) {
    setPlanetList(planetList.filter((planet) => planet.id !== id));
  }

  // 作用：重置行星列表——恢复为最初的完整数组
  // 解释：删除后想一键找回所有行星，直接再用一次初始数组 planets；
  //       参考：Movie Night Part 2 Step 09 中 App 的 state 初始化值
  function resetPlanets() {
    setPlanetList(planets);
  }

  return (
    // React.Fragment 允许返回多个并列元素而不需要额外的包裹节点
    // 作用：用 React.Fragment 包住多个并列元素，避免多加一层无意义的 div
    // 解释：Fragment 不会生成真实 DOM 节点，不影响布局和样式；
    //       参考：React 官方文档 Fragment 的说明
    <React.Fragment>
      {/* 作用：顶部工具栏——显示标题（含当前行星数量）和重置按钮 */}
      {/* 解释：planetList.length 实时反映剩余行星数量，删除后会立即变小；
              参考：Movie Night Part 1 starter/app.js 中 Header 组件显示统计数字的写法 */}
      <div className="toolbar">
        <h1>Planets ({planetList.length})</h1>
        <button className="reset-btn" onClick={resetPlanets}>
          Reset
        </button>
      </div>

      {/* 作用：条件渲染——列表为空显示提示文字，否则渲染行星卡片网格 */}
      {/* 解释：用三元运算符按条件二选一渲染，防止空数组时页面出现空白网格；
              参考：Movie Night Part 2 Step 10 中"列表为空显示提示"的写法 */}
      {planetList.length === 0 ? (
        <p className="empty">No planets left!</p>
      ) : (
        <div className="container">
          {/* 作用：遍历行星列表，为每颗行星渲染一个 Planet 组件；key 用 id 保证 React 高效更新 */}
          {/* 解释：map 把数组逐项变成 JSX 元素；key 是每项的唯一标识，
                  React 靠它判断哪些卡片变了/删了，不能用数组下标代替
                  参考：Movie Night Part 1 starter/app.js 中电影列表的 map + key 写法 */}
          {planetList.map((planet) => (
            <Planet key={planet.id} planet={planet} onRemove={removePlanet} />
          ))}
        </div>
      )}
    </React.Fragment>
  );
}

// 3: Render the container component to the DOM
//    任务 3：把容器组件渲染到页面 DOM 中
// 作用：创建 React 18 根节点，把 PlanetList 容器组件渲染进 id 为 root 的 DOM 节点
// 解释：createRoot 是 React 18 的新入口，替代旧的 ReactDOM.render；
//       整棵组件树从 PlanetList 开始向下渲染
//       参考：Movie Night Part 1 starter/app.js 文件末尾的渲染写法
ReactDOM.createRoot(document.getElementById('root')).render(<PlanetList />);
