// Step 12 - toggling watched
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
// 作用：MovieDetails 组件——在 Step 12 中把"看过/未看"徽章从 span 改成可点击按钮
// 解释：徽章变成 button 后，点击即可切换观看状态：onClick 调用父组件传来的
//       toggleWatched 并传入电影 id；按钮的 class 随 watched 真假切换配色
//       参考：Step 12 app.css 中新增的 button.badge 样式
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
      {/* 作用：年份与类型文字；"看过/未看"徽章改为按钮，点击调用父组件的 toggleWatched 切换状态 */}
      {/* 解释：class 用三元表达式在 badge-watched / badge-unwatched 之间切换，
              文字也随之变化；点击时把 props.id 传给父组件去改数据
              参考：Step 12 App 组件中的 handleToggleWatched 函数 */}
      <span className="movie-meta">
        { props.year } · { props.genre }
        <button
          className={ props.watched ? "badge badge-watched" : "badge badge-unwatched" }
          onClick={() => props.toggleWatched(props.id)}
        >
          { props.watched ? "WATCHED" : "NOT YET" }
        </button>
      </span>
    </>
  );
};

// 单部电影条目组件：删除按钮 + 电影信息（可切换看过状态）+ 受控评分组件
// 作用：Movie 组件——Part 2 最终版，同时支持删除、切换看过、修改评分三种操作
// 解释：三个操作全部通过 props 回调上报父组件，本组件只负责渲染和传递；
//       MovieDetails 新增 id 和 toggleWatched 两个 props 支持徽章点击
//       参考：Step 12 App 组件中的三个处理函数（remove/rating/toggle）
const Movie = (props) => {
  return (
    <div className="movie">
      {/* 作用：删除按钮——点击时调用父组件传来的 removeMovie 并传入本电影 id */}
      {/* 解释：箭头函数保证点击时才读取 props.id；
              参考：Step 10 App 组件中的 handleRemoveMovie 函数 */}
      <button className="remove-movie" onClick={() => props.removeMovie(props.id)}>✖</button>
      <div className="movie-info">
        {/* 作用：把 id 和 toggleWatched 传给 MovieDetails，实现"看过/未看"切换 */}
        {/* 解释：徽章按钮在 MovieDetails 内部，切换逻辑在 App，
                靠这两个 props 把两边连起来
                参考：Step 12 MovieDetails 组件中 button 的 onClick */}
        <MovieDetails
          title={props.title}
          year={props.year}
          genre={props.genre}
          watched={props.watched}
          staffPick={props.staffPick}
          id={props.id}
          toggleWatched={props.toggleWatched}
        />
      </div>

      {/* 作用：受控评分组件——评分值来自 props，点击时通知父组件修改 */}
      {/* 解释：Rating 不保存自己的分数（无状态组件），
              所有点击都转换成 changeRating 调用上报给 App
              参考：Step 11 App 组件中的 handleRatingChange 函数 */}
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

// toggling watched
// 切换"看过"状态：点击徽章时反转该电影的 watched 值
// 作用：新增 handleToggleWatched——点击徽章时反转该电影的 watched 字段
// 解释：与改评分同一模式：map 找到目标电影，用展开运算符复制并反转 watched；
//       切换后已看数量、页脚统计、徽章颜色全部自动更新（数据驱动）
//       参考：教程第十二章；Step 11 中 handleRatingChange 的 map 写法
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

  // 作用：修改评分——delta 为 +1 或 -1；限制在 0~5
  // 解释：map + 展开运算符实现不可变更新；Math.min/Math.max 夹紧范围
  //       参考：Step 11 中 handleRatingChange 的写法
  handleRatingChange = (delta, id) => {
    this.setState( prevState => ({
      movies: prevState.movies.map( movie =>
        movie.id === id
          ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
          : movie
      )
    }));
  }

  // 作用：切换看过状态——用展开运算符复制该电影对象并反转 watched
  // 解释：{ ...movie, watched: !movie.watched } 先复制整部电影，
  //       再覆盖 watched 字段（取反）；其余字段原样保留
  //       参考：Step 11 中修改 rating 的展开运算符写法
  handleToggleWatched = (id) => {
    this.setState( prevState => ({
      movies: prevState.movies.map( movie =>
        movie.id === id
          ? { ...movie, watched: !movie.watched }
          : movie
      )
    }));
  }

  render() {
    // 作用：从 state 统计已看电影数
    // 解释：统计值每次渲染从 state 现算，切换 watched 后自动更新
    //       参考：Step 09 中 watchedCount 的算法
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;
    // 作用：总分与平均评分
    // 解释：reduce 累加 rating，再除以电影数；空列表时显示占位符
    //       参考：Step 11 中 totalStars 与 averageRating 的算法
    const totalStars = this.state.movies.reduce((sum, movie) => sum + movie.rating, 0);
    const averageRating = this.state.movies.length > 0
      ? (totalStars / this.state.movies.length).toFixed(1)
      : '–';

    return (
      <div className="watchlist">
        {/* 作用：页头显示标题、电影总数与平均评分 */}
        {/* 解释：三个数字全部由 state.movies 派生；
                参考：Step 11 中 Header 的新增用法 */}
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

        {/* 作用：遍历渲染电影，把删除、改评分、切换看过三个函数传给每个 Movie */}
        {/* 解释：三种用户操作统一通过 props 回调上报到 App，
                本组件是唯一修改 state 的地方（单一数据源）
                参考：Step 12 Movie 组件对三个回调的使用 */}
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
            toggleWatched={this.handleToggleWatched}
          />
        )}

        {/* 作用：页脚——已看数量与总数来自 state */}
        {/* 解释：切换 watched 后这个数字会实时变化；
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
