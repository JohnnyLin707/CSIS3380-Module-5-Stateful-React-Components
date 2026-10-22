// Step 11 - ratings lifted up into App's state
// 电影数据源数组：每部电影包含标题、年份、类型、评分、是否看过、是否编辑推荐和唯一 id
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
const MovieDetails = (props) => {
  return (
    <>
      {/* 电影标题；如果是编辑推荐，追加一个 STAFF PICK 徽章 */}
      <span className="movie-title">
        { props.title }
        { props.staffPick && <span className="badge badge-pick">STAFF PICK</span> }
      </span>
      {/* 年份与类型；根据 watched 真假显示 WATCHED 或 NOT YET 徽章 */}
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
const Movie = (props) => {
  return (
    <div className="movie">
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

      {/* 把电影 id 和父组件的 changeRating 一起传给 Rating，实现评分修改 */}
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
const Rating = (props) => {
  return (
    <div className="rating">
      {/* 点击“-”：调用父组件的 changeRating(-1, id)，分数为 0 时禁用 */}
      <button
        className="rating-action decrement"
        onClick={() => props.changeRating(-1, props.id)}
        disabled={props.score === 0}
      > - </button>
      {/* 评分直接显示父组件传来的 props.score */}
      <span className="rating-score">{ props.score }</span>
      {/* 点击“+”：调用父组件的 changeRating(1, id)，分数为 5 时禁用 */}
      <button
        className="rating-action increment"
        onClick={() => props.changeRating(1, props.id)}
        disabled={props.score === 5}
      > + </button>
    </div>
  );
};

// 页脚组件：显示已看电影数和电影总数
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
class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  // 删除指定 id 的电影
  handleRemoveMovie = (id) => {
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  // 修改评分：delta 为 +1 或 -1；用 Math.min/Math.max 限制在 0~5
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
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;
    // 用 reduce 累加所有电影的评分得到总分
    const totalStars = this.state.movies.reduce((sum, movie) => sum + movie.rating, 0);
    // 平均评分 = 总分 / 电影数，保留一位小数；列表为空时显示占位符
    const averageRating = this.state.movies.length > 0
      ? (totalStars / this.state.movies.length).toFixed(1)
      : '–';

    return (
      <div className="watchlist">
        {/* 页头新增平均评分 */}
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
          averageRating={averageRating}
        />

        {/* Movie list */}
        {/* 列表为空时显示提示文字 */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

        {/* 遍历渲染电影，把删除和评分修改函数传给每个 Movie */}
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

        <Footer
          watchedCount={watchedCount}
          totalMovies={this.state.movies.length}
        />
      </div>
    );
  }
}

// 把 App 组件渲染到 id 为 root 的 DOM 节点，并传入电影初始数据
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
