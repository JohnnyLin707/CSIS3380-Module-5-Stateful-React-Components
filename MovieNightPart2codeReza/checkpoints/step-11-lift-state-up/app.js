// Step 11 - ratings lifted up into App's state
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

// 页头组件：显示应用标题、电影总数和平均评分
// 作用：Header 组件——在标题和电影总数之外，新增平均评分徽章（props.averageRating）
// 解释：平均评分由 App 从 state 中的电影数据算出后传进来，Header 只负责显示；
//       徽章样式直接复用 .stats，并在 app.css 中用相邻选择器加间距
//       参考：Step 11 起 app.css 中 "header .stats + .stats" 的新增样式
const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
      <span className="stats">Avg rating: { props.averageRating }</span>
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

// 单部电影条目组件：删除按钮 + 电影信息 + 评分组件
// 评分改为受控：评分值来自 props，点击加减时通知父组件修改
// 作用：Movie 组件——把电影的 id 和父组件的 changeRating 一起传给 Rating
// 解释：从 Step 11 起评分不再由 Rating 自己保存（状态提升），
//       Rating 只显示 props.score，点击时调用 changeRating 通知 App 改数据
//       参考：Step 11 App 组件中的 handleRatingChange 函数
const Movie = (props) => {
  return (
    <div className="movie">
      {/* 作用：删除按钮——点击时调用父组件传来的 removeMovie 并传入本电影 id */}
      {/* 解释：箭头函数保证点击时才读取 props.id；
              参考：Step 10 App 组件中的 handleRemoveMovie 函数 */}
      <button className="remove-movie" onClick={() => props.removeMovie(props.id)}>✖</button>
      <div className="movie-info">
        <MovieDetails
          title={props.title}
          year={props.year}
          genre={props.genre}
          watched={props.watched}
          staffPick={props.staffPick}
        />
      </div>

      {/* 作用：把电影 id 和父组件的 changeRating 一起传给 Rating，实现评分修改 */}
      {/* 解释：id 让 Rating 点击时知道"改哪一部电影"，changeRating 是改数据的唯一通道；
              参考：下方 RATING_LIFTED 组件中 props.changeRating 的调用 */}
      <Rating
        score={props.rating}
        id={props.id}
        changeRating={props.changeRating}
      />
    </div>
  );
};

// No state of its own any more: the score comes from App, and clicks are reported to App
// 组件不再拥有自己的状态：评分由 App 提供，点击时向 App 汇报（状态提升）
// 作用：Rating 改回函数组件，评分完全由 props 提供，点击时通知 App 修改
// 解释：这一步叫"状态提升"——评分数据移到父组件 App 的 state 里，
//       Rating 变成纯展示组件；多个组件要共享的数据都应提升到公共父级
//       参考：教程第十一章；Step 11 App 组件中的 handleRatingChange
const Rating = (props) => {
  return (
    <div className="rating">
      {/* 作用：点击"-"——调用父组件的 changeRating(-1, id)，分数为 0 时禁用 */}
      {/* 解释：不在本组件里算新分数，只上报"要加/要减"和"是哪部电影"，
              具体怎么改由父组件决定（数据唯一来源）
              参考：Step 11 App 组件中的 handleRatingChange 函数 */}
      <button
        className="rating-action decrement"
        onClick={() => props.changeRating(-1, props.id)}
        disabled={props.score === 0}
      > - </button>
      {/* 作用：评分直接显示父组件传来的 props.score */}
      {/* 解释：本组件不再有 this.state，界面完全由 props 驱动
              参考：Step 07 中 Rating 自带 state 的写法对比 */}
      <span className="rating-score">{ props.score }</span>
      {/* 作用：点击"+"——调用父组件的 changeRating(1, id)，分数为 5 时禁用 */}
      {/* 解释：与减号对称，上报 +1 和电影 id；边界判断同样基于 props
              参考：Step 11 App 组件中的 handleRatingChange 函数 */}
      <button
        className="rating-action increment"
        onClick={() => props.changeRating(1, props.id)}
        disabled={props.score === 5}
      > + </button>
    </div>
  );
};

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

// ratings lifted up into App's state
// 评分状态提升到 App：修改评分与删除电影一样，都通过更新 state 完成
// Header 增加平均评分展示
// 作用：把评分也收归 App 管理——新增 handleRatingChange，Header 增加平均评分
// 解释：评分原本存在每个 Rating 组件内部（Step 07 之前），提升后：
//       数据集中在 App，页头才能算出平均评分，Rating 变成纯展示组件
//       参考：教程第十一章；React 官方文档 "Lifting State Up"
class App extends React.Component {
  // 作用：用传入的初始电影数组初始化 state
  // 解释：state = {...} 类属性写法，初始值来自 props.initialMovies
  //       参考：Step 09 中 state 的初始化
  state = {
    movies: this.props.initialMovies
  };

  // 作用：删除指定 id 的电影
  // 解释：与 Step 10 相同，filter 生成新数组实现删除
  //       参考：Step 10 中 handleRemoveMovie 的写法
  handleRemoveMovie = (id) => {
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  // 作用：修改评分——delta 为 +1 或 -1；用 Math.min/Math.max 限制在 0~5
  // 解释：map 遍历所有电影，只给 id 匹配的那部改分数（用展开运算符复制对象后
  //       覆盖 rating 字段），其余原样返回——同样是不可变更新
  //       参考：MDN Array.prototype.map 与对象展开语法
  handleRatingChange = (delta, id) => {
    this.setState( prevState => ({
      movies: prevState.movies.map( movie =>
        movie.id === id
          ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
          : movie
      )
    }));
  }

  render() {
    // 作用：从 state 统计已看电影数
    // 解释：统计值每次渲染从 state 现算，不单独存放
    //       参考：Step 09 中 watchedCount 的算法
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;
    // 作用：用 reduce 累加所有电影的评分得到总分
    // 解释：reduce 把数组"归纳"成一个值：sum 是累加器，从 0 开始，
    //       逐部电影把 rating 加进去
    //       参考：MDN Array.prototype.reduce 文档
    const totalStars = this.state.movies.reduce((sum, movie) => sum + movie.rating, 0);
    // 作用：平均评分 = 总分 / 电影数，保留一位小数；列表为空时显示占位符
    // 解释：先判空避免 0/0 得到 NaN；toFixed(1) 保留一位小数让显示稳定
    //       参考：MDN Number.prototype.toFixed 文档
    const averageRating = this.state.movies.length > 0
      ? (totalStars / this.state.movies.length).toFixed(1)
      : '–';

    return (
      <div className="watchlist">
        {/* 作用：页头新增平均评分 */}
        {/* 解释：averageRating 由本组件算出后传给 Header，Header 只管显示；
                新增的 .stats 徽章样式见 app.css
                参考：app.css 中 "header .stats + .stats" 样式 */}
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
          averageRating={averageRating}
        />

        {/* Movie list */}
        {/* 作用：列表为空时显示提示文字 */}
        {/* 解释：删光所有电影后显示引导文案；
                参考：Step 10 中同样条件的写法 */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

        {/* 作用：遍历渲染电影，把删除和评分修改函数传给每个 Movie */}
        {/* 解释：delete 和 rating 两个操作都通过 props 回调上报到 App 统一处理，
                子组件不直接改数据
                参考：Step 11 Movie 组件中 Rating 的 changeRating 调用 */}
        {this.state.movies.map( movie =>
          <Movie
            title={movie.title}
            year={movie.year}
            genre={movie.genre}
            rating={movie.rating}
            watched={movie.watched}
            staffPick={movie.staffPick}
            id={movie.id}
            key={movie.id.toString()}
            removeMovie={this.handleRemoveMovie}
            changeRating={this.handleRatingChange}
          />
        )}

        {/* 作用：页脚——已看数量与总数来自 state */}
        {/* 解释：与页头同源，全部由 state.movies 派生
                参考：上方 Footer 组件对 props 的定义 */}
        <Footer
          watchedCount={watchedCount}
          totalMovies={this.state.movies.length}
        />
      </div>
    );
  }
}

// 作用：渲染入口——创建 React 18 根节点，把 App 渲染进 #root，并传入电影数据
// 解释：createRoot 是 React 18 的入口 API；initialMovies 属性把数据交给 App，
//       Step 09 起这份数据会变成 App 内部的 state
//       参考：Movie Night Part 1 的渲染代码；React 官方文档 createRoot
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
