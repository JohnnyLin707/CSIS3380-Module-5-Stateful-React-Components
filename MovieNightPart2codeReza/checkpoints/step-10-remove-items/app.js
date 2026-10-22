// Step 10 - removing items from state
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

// 页头组件：显示应用标题和电影总数
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

// 单部电影条目组件：新增删除按钮，点击调用父组件的 removeMovie 删除该电影
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

      <Rating score={props.rating} />
    </div>
  );
};

// updating state from the previous state
// 基于前一个状态来更新状态：用函数式 setState 保证多次连续点击也准确
// 同时用 Math.min / Math.max 把评分限制在 0~5，到边界时禁用按钮
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  // 评分 +1，最高不超过 5；prevState 是前一个状态
  incrementScore = () => {
    this.setState( prevState => ({
      score: Math.min(prevState.score + 1, 5)
    }));
  }

  // 评分 -1，最低不低于 0
  decrementScore = () => {
    this.setState( prevState => ({
      score: Math.max(prevState.score - 1, 0)
    }));
  }

  render() {
    return (
      <div className="rating">
        {/* 评分为 0 时禁用“-”按钮 */}
        <button
          className="rating-action decrement"
          onClick={this.decrementScore}
          disabled={this.state.score === 0}
        > - </button>
        <span className="rating-score">{ this.state.score }</span>
        {/* 评分为 5 时禁用“+”按钮 */}
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
const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};

// removing items from state
// 从 state 中删除条目：用 filter 生成不含该电影的新数组
class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  // 删除指定 id 的电影：箭头函数保证 this 指向组件实例
  handleRemoveMovie = (id) => {
    // 用函数式 setState 基于前一个状态过滤，保证连续删除也正确
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  render() {
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;

    return (
      <div className="watchlist">
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
        />

        {/* Movie list */}
        {/* 列表为空时显示提示文字 */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

        {/* 遍历渲染电影，并把 id 和删除函数传给每个 Movie */}
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
