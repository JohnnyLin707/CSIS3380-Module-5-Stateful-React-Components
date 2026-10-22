// Step 04 - handling a click
// 作用：电影数据源数组——每部电影包含标题、年份、类型、评分、是否看过、是否编辑推荐和唯一 id
// 解释：数据与组件分离；Part 2 会把这个数组搬进 App 的 state，
//       之后增删改电影都只动 state 不动组件；id 在 Part 2 中用作 key 和定位依据
//       参考：Movie Night Part 1 课堂代码中的数据数组
const movies = [
  {
    title: "Spirited Away",
    year: 2001,
    genre: "Animation",
    rating: 5,
    watched: true,
    staffPick: true,
    id: 1
  },
  {
    title: "Inception",
    year: 2010,
    genre: "Sci-Fi",
    rating: 4,
    watched: true,
    staffPick: false,
    id: 2
  },
  {
    title: "The Grand Budapest Hotel",
    year: 2014,
    genre: "Comedy",
    rating: 4,
    watched: false,
    staffPick: true,
    id: 3
  },
  {
    title: "Coco",
    year: 2017,
    genre: "Animation",
    rating: 5,
    watched: false,
    staffPick: false,
    id: 4
  }
];

// 页头组件：显示应用标题和电影总数
// 作用：Header 组件——显示应用标题（props.title）和电影总数（props.totalMovies）
// 解释：页头需要的数据全部由父组件 App 通过 props 传入，自己不存数据，
//       这种"数据从父级流入"的单向数据流是 React 的核心模式
//       参考：Movie Night Part 1 的 Header 组件代码
const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
    </header>
  );
};

// Returns two sibling spans with no wrapper element
// 返回两个并列的 span 元素，不需要额外的包裹节点（React Fragment 空标签）
// 作用：MovieDetails 组件——展示电影标题（含编辑推荐徽章）和年份类型（含看过状态徽章）
// 解释：React 组件只能返回一个根元素，用空标签 <>（Fragment）包住两个 span，
//       就不会在页面上多出一层无意义的 div，保持 CSS 布局干净
//       参考：React 官方文档 Fragment 一节；Movie Night Part 1 的 MovieDetails 代码
const MovieDetails = (props) => {
  return (
    <>
      {/* 作用：电影标题文字；如果是编辑推荐，追加一个 STAFF PICK 徽章 */}
      {/* 解释：{条件 && <徽章>} 是 React 条件渲染的常用写法——条件为 false 时
              React 什么都不渲染，比在 JSX 里写 if/else 更简洁；
              参考：app.css 中 .badge-pick 的样式 */}
      <span className="movie-title">
        { props.title }
        { props.staffPick && <span className="badge badge-pick">STAFF PICK</span> }
      </span>
      {/* 作用：年份与类型文字；根据 watched 真假显示 WATCHED 或 NOT YET 徽章 */}
      {/* 解释：三元运算符"条件 ? A : B"在两个徽章之间二选一，
              与上面的 && 写法分别对应"二选一"和"要/不要"两种场景；
              参考：app.css 中 .badge-watched 与 .badge-unwatched 两套样式 */}
      <span className="movie-meta">
        { props.year } · { props.genre }
        { props.watched
            ? <span className="badge badge-watched">WATCHED</span>
            : <span className="badge badge-unwatched">NOT YET</span> }
      </span>
    </>
  );
};

// 单部电影条目组件：左侧为电影信息，右侧为评分组件
// 作用：Movie 组件——一部电影在列表中的一行，左边是信息，右边是评分
// 解释：把一行电影拆成"信息 + 评分"两个子组件，各自负责一块 UI；
//       数据从 props 流入，组件本身无状态（Part 1 阶段）
//       参考：Movie Night Part 1 的 Movie 组件代码
const Movie = (props) => {
  return (
    <div className="movie">
      <div className="movie-info">
        <MovieDetails
          title={props.title}
          year={props.year}
          genre={props.genre}
          watched={props.watched}
          staffPick={props.staffPick}
        />
      </div>

      {/* 作用：评分组件，显示该电影的评分 */}
      {/* 解释：Rating 只接收一个 score 数值，完全依赖父组件传入；
              参考：下方 Rating 组件的定义 */}
      <Rating score={props.rating} />
    </div>
  );
};

// handling a click
// 处理一次点击事件：给"+"按钮绑定 onClick 事件处理器
// 作用：给"+"按钮绑定 onClick={this.incrementScore}，并定义对应的事件处理方法
// 解释：React 事件用驼峰命名（onClick 而不是 onclick），绑定的是函数引用；
//       此时方法里只打印一句话，先验证"点击确实触发了"
//       参考：教程第五章；React 官方文档 Handling Events
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  // 作用：点击"+"时触发的事件处理方法（暂时只在控制台打印）
  // 解释：先只打印不改状态，是为了确认事件链路（按钮→方法）已经通；
  //       下一步再在方法里调用 setState 真正改分
  //       参考：下一步（Step 05）在方法中调用 this.setState
  incrementScore() {
    console.log('Hi, from inside incrementScore!');
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        {/* 作用：把 incrementScore 绑定到"+"按钮的点击事件 */}
        {/* 解释：onClick 后传函数引用（不带括号），点击时 React 自动调用；
                如果写成 onClick={this.incrementScore()} 会在渲染时立即执行
                参考：React 官方文档 Handling Events 中的注意事项 */}
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}

// 页脚组件：显示已看电影数和电影总数
// 作用：Footer 组件——显示"已看 X 部 / 共 Y 部"的统计文字
// 解释：统计数字由 App 从 state 算出后通过 props 传入，Footer 只负责显示；
//       Part 2 中 watched 字段可切换后，这个数字会随之变化
//       参考：Movie Night Part 1 的 Footer 组件代码
const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};

// 应用根组件（函数组件版本）：从 props.initialMovies 读取电影列表
// 作用：App 根组件——组合页头、电影列表、页脚，并计算已看电影数量
// 解释：这是"无状态"版本的 App：电影列表来自 props，无法修改；
//       Step 09 会把这个列表搬进 App 自己的 state
//       参考：Movie Night Part 1 的 App 组件代码；下一步 Step 09
const App = (props) => {
  // 作用：统计已看过的电影数量
  // 解释：filter 返回满足条件的数组，.length 就是数量——这种"从数据派生统计值"
  //       的写法在 Part 2 会反复出现（平均评分同理）
  //       参考：Step 11 中计算 averageRating 的 reduce 写法
  const watchedCount = props.initialMovies.filter(movie => movie.watched).length;

  return (
    <div className="watchlist">
      {/* 作用：页头——标题 + 电影总数 */}
      {/* 解释：标题写死，总数用数组长度动态算出；
              参考：上方 Header 组件对 props.title / props.totalMovies 的定义 */}
      <Header
        title="Movie Night"
        totalMovies={props.initialMovies.length}
      />

      {/* Movie list */}
      {/* 电影列表：遍历数组，为每部电影渲染一个 Movie 组件；key 用电影 id 保证高效更新 */}
      {/* 解释：map 把数组逐项变成 JSX；key 必须是稳定唯一的标识（这里用 id），
              React 靠它判断哪一行变了，用数组下标会在删除时出错
              参考：Movie Night Part 1 的列表渲染代码；React 官方文档 Lists and Keys */}
      {props.initialMovies.map( movie =>
        <Movie
          title={movie.title}
          year={movie.year}
          genre={movie.genre}
          rating={movie.rating}
          watched={movie.watched}
          staffPick={movie.staffPick}
          key={movie.id.toString()}
        />
      )}

      {/* 作用：页脚——已看数量与总数 */}
      <Footer
        watchedCount={watchedCount}
        totalMovies={props.initialMovies.length}
      />
    </div>
  );
};

// 作用：渲染入口——创建 React 18 根节点，把 App 渲染进 #root，并传入电影数据
// 解释：createRoot 是 React 18 的入口 API；initialMovies 属性把数据交给 App，
//       Step 09 起这份数据会变成 App 内部的 state
//       参考：Movie Night Part 1 的渲染代码；React 官方文档 createRoot
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
