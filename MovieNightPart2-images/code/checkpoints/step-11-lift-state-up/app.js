// Step 11 - Lift state up: one source of truth for ratings
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
      {/* 【作答部分 - Step 11】显示平均评分胶囊标签 */}
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
        { props.watched
            ? <span className="badge badge-watched">WATCHED</span>
            : <span className="badge badge-unwatched">NOT YET</span> }
      </span>
    </>
  );
};

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

      {/* 【作答部分 - Step 11】将 score、id 和 changeRating 向下传给 Rating */}
      <Rating
        score={props.rating}
        id={props.id}
        changeRating={props.changeRating}
      />
    </div>
  );
};

// 【作答部分 - Step 11】状态提升后，Rating 改回无状态函数组件：
// 分数来自 App 传入的 props.score，点击事件通过 props.changeRating(delta, props.id) 向上汇报给 App
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

class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  handleRemoveMovie = (id) => {
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  // 【作答部分 - Step 11】在 App 中统一更新某部电影的评分（使用 map 与对象展开运算符返回新数组和新对象）
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
    // 【作答部分 - Step 11】使用 reduce() 计算总星数并求出平均分（列表为空时显示 '-'）
    const totalStars = this.state.movies.reduce((sum, movie) => sum + movie.rating, 0);
    const averageRating = this.state.movies.length > 0
      ? (totalStars / this.state.movies.length).toFixed(1)
      : '-';

    return (
      <div className="watchlist">
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
          averageRating={averageRating}
        />

        {/* Movie list */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

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

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
