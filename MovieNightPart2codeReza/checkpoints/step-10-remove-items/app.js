// Step 10 - removing items from state
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

// 单部电影条目组件：新增删除按钮，点击调用父组件的 removeMovie 删除该电影
// 作用：Movie 组件——在原有结构上新增一个删除按钮
// 解释：删除按钮通过 props.removeMovie 把本电影的 id 报告给父组件，
//       由父组件去更新 state（电影列表不在本组件里）；
//       这是 Part 2"状态提升"思想的第一次应用
//       参考：Step 10 App 组件中的 handleRemoveMovie 函数
const Movie = (props) => {
  return (
    <div className="movie">
      {/* 作用：删除按钮——点击时调用父组件传来的 removeMovie 并传入本电影 id */}
      {/* 解释：箭头函数保证点击时才读取 props.id（直接写 onClick={props.removeMovie}
              会把 id 参数漏掉）；按钮文字用 ✖ 符号保持简洁
              参考：app.css 中 .remove-movie 的样式 */}
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

      {/* 作用：评分组件，显示该电影的评分 */}
      {/* 解释：此时评分还是纯展示（评分交互从 Step 11 开始加）；
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

// removing items from state
// 从 state 中删除条目：用 filter 生成不含该电影的新数组
// 作用：新增删除功能——handleRemoveMovie 用 filter 从 state 中移除指定电影
// 解释：React 要求"不可变更新"：不能直接改原数组，而是用 filter 生成新数组
//       再交给 setState；删除函数通过 props 逐层传给每个 Movie 的删除按钮
//       参考：教程第十章；React 官方文档 "Updating Objects in State"
class App extends React.Component {
  // 作用：用传入的初始电影数组初始化 state
  // 解释：state = {...} 类属性写法，初始值来自 props.initialMovies
  //       参考：Step 09 中 state 的初始化
  state = {
    movies: this.props.initialMovies
  };

  // 作用：删除指定 id 的电影——箭头函数保证 this 指向组件实例
  // 解释：箭头函数类属性的写法让方法作为回调传递时 this 不丢失
  //       （Step 05-06 学到的教训）；函数被 Movie 组件的删除按钮调用
  //       参考：Step 06 中箭头函数绑定 this 的写法
  handleRemoveMovie = (id) => {
    // 作用：用函数式 setState 基于前一个状态过滤，保证连续删除也正确
    // 解释：prevState => ({...}) 的写法保证拿到最新状态；
    //       filter 保留 id 不等于传入 id 的电影，等于"删掉那一部"
    //       参考：MDN Array.prototype.filter 文档
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  render() {
    // 作用：从 state 统计已看电影数
    // 解释：统计值每次渲染从 state 现算，不单独存放
    //       参考：Step 09 中 watchedCount 的算法
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;

    return (
      <div className="watchlist">
        {/* 作用：页头数据来自 state */}
        {/* 解释：电影总数随删除实时变化；
                参考：Step 09 中 Header 的用法 */}
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
        />

        {/* Movie list */}
        {/* 作用：列表为空时显示提示文字 */}
        {/* 解释：用 && 做条件渲染——删光后给用户一句引导文案，
                避免页面出现空白区域；app.css 中 .empty 提供样式
                参考：app.css 中 .empty 样式；React 条件渲染文档 */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

        {/* 作用：遍历渲染电影，并把 id 和删除函数传给每个 Movie */}
        {/* 解释：id 让子组件知道"我是谁"，removeMovie 让子组件能"要求删除自己"；
                props 是父子组件通信的唯一通道
                参考：Step 10 Movie 组件中删除按钮的 onClick */}
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
