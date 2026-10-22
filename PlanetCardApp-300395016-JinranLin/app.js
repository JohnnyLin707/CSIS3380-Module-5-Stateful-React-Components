// 八大行星数据源：每颗行星包含 id、名称、直径、卫星数、简介和图片路径
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
function Planet({ planet, onRemove }) {
  // planet：单颗行星的数据对象；onRemove：父组件传来的删除回调函数
  return (
    <div className="card">
      {/* 行星图片区域：黑色背景衬托星球照片 */}
      <div>
        <img src={planet.url} alt={planet.name} />
      </div>
      {/* 行星名称标题 */}
      <h2>{planet.name}</h2>
      {/* 行星简介文字 */}
      <p>{planet.desc}</p>
      <h3>Planet Profile</h3>
      {/* 行星档案列表：直径与卫星数量 */}
      <ul>
        <li>
          <strong>Diameter:</strong> {planet.diameter}
        </li>
        <li>
          <strong>Moons:</strong> {planet.moons}
        </li>
      </ul>
      {/* 删除按钮：点击时调用 onRemove 并把当前行星的 id 传出去 */}
      <button className="remove-btn" onClick={() => onRemove(planet.id)}>
        Remove
      </button>
    </div>
  );
}

// 2: Create a container component that iterates over the planets array
//    and renders a 'Planet' component for each object in the array
//    任务 2：创建一个容器组件，遍历行星数组，为每个行星对象渲染一个 'Planet' 组件
function PlanetList() {
  // 用 useState 把初始行星数组存进组件状态，planetList 是当前显示的行星列表
  const [planetList, setPlanetList] = React.useState(planets);

  // 删除指定 id 的行星：用 filter 过滤掉被点击的那颗，得到新数组并更新状态
  function removePlanet(id) {
    setPlanetList(planetList.filter((planet) => planet.id !== id));
  }

  // 重置行星列表：恢复为最初的完整数组
  function resetPlanets() {
    setPlanetList(planets);
  }

  return (
    // React.Fragment 允许返回多个并列元素而不需要额外的包裹节点
    <React.Fragment>
      {/* 顶部工具栏：显示标题（含当前行星数量）和重置按钮 */}
      <div className="toolbar">
        <h1>Planets ({planetList.length})</h1>
        <button className="reset-btn" onClick={resetPlanets}>
          Reset
        </button>
      </div>

      {/* 条件渲染：如果列表为空显示提示文字，否则渲染行星卡片网格 */}
      {planetList.length === 0 ? (
        <p className="empty">No planets left!</p>
      ) : (
        <div className="container">
          {/* 遍历行星列表，为每颗行星渲染一个 Planet 组件；key 用 id 保证 React 高效更新 */}
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
ReactDOM.createRoot(document.getElementById('root')).render(<PlanetList />);
