// ============================================================================
// Movie Night — Part 2: Interactive State & Events (完整项目代码)
// ============================================================================

// 【作答部分 - Step 13】从 React 中解构出 useState Hook，用于在函数组件中管理状态
const { useState } = React;

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

const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
      {/* 【作答部分 - Step 11】新增第二个胶囊标签，实时显示由 App 计算并传入的平均分 */}
      <span className="stats">Avg rating: { props.averageRating }</span>
    </header>
  );
};

// Returns two sibling spans with no wrapper element
const MovieDetails = (props) => {
  return (
    <>
      <span className="movie-title">
        { props.title }
        { props.staffPick && <span className="badge badge-pick">STAFF PICK</span> }
      </span>
      <span className="movie-meta">
        { props.year } · { props.genre }
        {/* 【作答部分 - Step 12 (Your turn: toggle WATCHED)】
            将原本静态的 <span> 替换为可点击的 <button>：
            1. className 根据 props.watched 动态切换样式（badge-watched / badge-unwatched）
            2. onClick 使用箭头函数把当前电影的 props.id 向上传递给 props.toggleWatched
            3. 按钮文字根据 props.watched 动态显示 "WATCHED" 或 "NOT YET" */}
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

const Movie = (props) => {
  return (
    <div className="movie">
      {/* 【作答部分 - Step 10】在 .movie 容器最前面添加删除按钮 ✖
          必须使用箭头函数 () => props.removeMovie(props.id) 包装，
          这样只会在点击时调用并传入当前电影 id，而不会在渲染时立即执行 */}
      <button className="remove-movie" onClick={() => props.removeMovie(props.id)}>✖</button>

      <div className="movie-info">
        <MovieDetails
          title={props.title}
          year={props.year}
          genre={props.genre}
          watched={props.watched}
          staffPick={props.staffPick}
          /* 【作答部分 - Step 12】将电影 id 与切换观看状态的回调继续向下传递给 MovieDetails */
          id={props.id}
          toggleWatched={props.toggleWatched}
        />
      </div>

      {/* 【作答部分 - Step 11】状态提升后，将评分 score、电影 id 和修改评分回调 changeRating 传给 Rating */}
      <Rating
        score={props.rating}
        id={props.id}
        changeRating={props.changeRating}
      />
    </div>
  );
};

// 【作答部分 - Step 11】状态提升（Lifting State Up）：
// Rating 不再维护自己的私有 state，而是改回无状态函数组件；
// 分数直接从 props.score 读取，点击 - / + 按钮时通过 props.changeRating(delta, props.id) 向上汇报给 App，
// 同时保留 Step 07 的边界禁用逻辑（0 分禁用减号，5 分禁用加号）。
const Rating = (props) => {
  return (
    <div className="rating">
      <button
        className="rating-action decrement"
        onClick={() => props.changeRating(-1, props.id)}
        disabled={props.score === 0}
      > - </button>
      <span className="rating-score">{ props.score }</span>
      <button
        className="rating-action increment"
        onClick={() => props.changeRating(1, props.id)}
        disabled={props.score === 5}
      > + </button>
    </div>
  );
};

const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};

// 【作答部分 - Step 09 ~ Step 13】App 组件：全应用的唯一数据源（Single Source of Truth）
// 在 Step 09-12 中使用 Class 组件（this.state / this.setState），
// 在 Step 13 中重构为现代 React 的函数组件 + useState Hook：
const App = (props) => {
  // 【作答部分 - Step 13】使用 useState 初始化 movies 状态数组
  const [movies, setMovies] = useState(props.initialMovies);

  // 【作答部分 - Step 10 & Step 13】删除指定 id 的电影：
  // 使用 filter() 返回一个不包含该 id 的全新数组（不可直接修改原数组）
  const handleRemoveMovie = (id) => {
    setMovies( prevMovies => prevMovies.filter( movie => movie.id !== id ) );
  };

  // 【作答部分 - Step 11 & Step 13】修改指定 id 电影的评分（步长为 delta，范围限制在 0 ~ 5）：
  // 使用 map() 返回新数组，对匹配 id 的电影用对象展开运算符 { ...movie, rating: ... } 创建新对象拷贝
  const handleRatingChange = (delta, id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
        : movie
    ));
  };

  // 【作答部分 - Step 12 (Your turn) & Step 13】切换指定 id 电影的已看状态（watched 取反）：
  // 同样使用函数式更新与 map() + 展开运算符，保持不可变数据更新（Immutability）
  const handleToggleWatched = (id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, watched: !movie.watched }
        : movie
    ));
  };

  // 【作答部分 - Step 09 & Step 11】派生状态（Derived State）在每次渲染时直接计算，而不额外存入 state：
  // 1. watchedCount：统计已观看的电影数量
  // 2. totalStars：使用 reduce() 累加所有电影的评分
  // 3. averageRating：计算平均分并保留 1 位小数；当列表为空时返回 '-' 防止除以 0
  const watchedCount = movies.filter(movie => movie.watched).length;
  const totalStars = movies.reduce((sum, movie) => sum + movie.rating, 0);
  const averageRating = movies.length > 0
    ? (totalStars / movies.length).toFixed(1)
    : '-';

  return (
    <div className="watchlist">
      <Header
        title="Movie Night"
        totalMovies={movies.length}
        averageRating={averageRating}
      />

      {/* Movie list */}
      {/* 【作答部分 - Step 10】当所有电影被移除（列表长度为 0）时，利用 && 短路求值显示空列表提示信息 */}
      {movies.length === 0 &&
        <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

      {movies.map( movie =>
        <Movie
          title={movie.title}
          year={movie.year}
          genre={movie.genre}
          rating={movie.rating}
          watched={movie.watched}
          staffPick={movie.staffPick}
          /* 【作答部分 - Step 10 ~ Step 12】
             key 仅供 React 内部识别列表项，组件内部无法通过 props.key 读取，
             因此必须单独传递 id={movie.id}，并将三个事件处理函数通过 props 向下传递 */
          id={movie.id}
          key={movie.id.toString()}
          removeMovie={handleRemoveMovie}
          changeRating={handleRatingChange}
          toggleWatched={handleToggleWatched}
        />
      )}

      <Footer
        watchedCount={watchedCount}
        totalMovies={movies.length}
      />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
