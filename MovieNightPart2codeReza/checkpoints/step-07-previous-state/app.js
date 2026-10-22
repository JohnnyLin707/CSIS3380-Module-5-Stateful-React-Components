// Step 07 - updating state from the previous state
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

// updating state from the previous state
// 基于前一个状态来更新状态：用函数式 setState 保证多次连续点击也准确
// 同时用 Math.min / Math.max 把评分限制在 0~5，到边界时禁用按钮
// 作用：改用函数式 setState，并把评分限制在 0~5，到边界禁用按钮
// 解释：直接写 this.setState({score: this.state.score + 1}) 在连续快速点击时
//       可能读到旧值；传函数给 setState，React 会保证拿到最新的前一个状态；
//       Math.min/Math.max 做上下限 clamp，禁用按钮则从交互上兜底
//       参考：教程第八章；React 官方文档 "State Updates May Be Asynchronous"
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  // 作用：评分 +1，最高不超过 5；prevState 是前一个状态
  // 解释：setState 里传函数而非对象，prevState 参数由 React 提供，
  //       保证基于最新状态计算，避免批量更新时丢失
  //       参考：React 官方文档 setState 函数式用法
  incrementScore = () => {
    // 作用：Math.min(前值 + 1, 5)——加分但不超过上限 5
    // 解释：Math.min(a, b) 返回较小值，这里实现"封顶 5"的效果
    //       参考：MDN Math.min 文档
    this.setState( prevState => ({
      score: Math.min(prevState.score + 1, 5)
    }));
  }

  // 作用：评分 -1，最低不低于 0
  // 解释：与加分对称，用 Math.max 实现"保底 0"
  //       参考：上方 incrementScore 的写法
  decrementScore = () => {
    // 作用：Math.max(前值 - 1, 0)——减分但不低于下限 0
    // 解释：Math.max(a, b) 返回较大值，这里实现"兜底 0"的效果
    //       参考：MDN Math.max 文档
    this.setState( prevState => ({
      score: Math.max(prevState.score - 1, 0)
    }));
  }

  render() {
    return (
      <div className="rating">
        {/* 作用：减分按钮——评分为 0 时禁用 */}
        {/* 解释：disabled={条件} 是 React 里控制按钮禁用的标准写法；
                app.css 中 .rating-action:disabled 提供半透明禁用样式
                参考：app.css 中禁用态相关样式 */}
        <button
          className="rating-action decrement"
          onClick={this.decrementScore}
          disabled={this.state.score === 0}
        > - </button>
        <span className="rating-score">{ this.state.score }</span>
        {/* 作用：加分按钮——评分为 5 时禁用 */}
        {/* 解释：与减分按钮对称，到上限同样禁用，双保险防止越界
                参考：app.css 中禁用态相关样式 */}
        <button
          className="rating-action increment"
          onClick={this.incrementScore}
          disabled={this.state.score === 5}
        > + </button>
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
