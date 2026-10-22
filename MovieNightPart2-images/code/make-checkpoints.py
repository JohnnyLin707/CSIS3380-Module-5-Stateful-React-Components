#!/usr/bin/env python3
"""Write one folder per Part 2 tutorial step, each holding the finished code for that step.

Students build a single movie-night project in starter/ as they follow the handout.
These checkpoint folders hold the finished state of each step in Part 2 (State & Events),
with Chinese comments explaining the student-authored parts.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(HERE, "starter", "app.css")

INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Movie Night</title>
    <link rel="stylesheet" href="./app.css" />
  </head>

  <body>
    <div id="root"></div>

    <script crossorigin src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
    <script type="text/babel" src="./app.js"></script>
  </body>
</html>
'''

MOVIES_FULL = '''const movies = [
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

'''

HEADER_BASIC = '''const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
    </header>
  );
};

'''

MOVIE_DETAILS_STATIC = '''// Returns two sibling spans with no wrapper element
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

'''

MOVIE_BASIC = '''const Movie = (props) => {
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

      <Rating score={props.rating} />
    </div>
  );
};

'''

FOOTER = '''const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};

'''

APP_FUNCTION_INITIAL = '''const App = (props) => {
  const watchedCount = props.initialMovies.filter(movie => movie.watched).length;

  return (
    <div className="watchlist">
      <Header
        title="Movie Night"
        totalMovies={props.initialMovies.length}
      />

      {/* Movie list */}
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

      <Footer
        watchedCount={watchedCount}
        totalMovies={props.initialMovies.length}
      />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
'''

STEPS = {}

# Step 01
STEPS["step-01-broken-button"] = (
    "// Step 01 - Why a plain variable is not enough\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 01】尝试用普通局部变量保存分数：
// 控制台里 score 会增加，但页面不会更新，因为 React 不追踪普通变量且不会触发重新渲染
const Rating = (props) => {
  let score = props.score;

  const incrementScore = () => {
    score = score + 1;
    console.log('score is now:', score);
  };

  return (
    <div className="rating">
      <button className="rating-action decrement"> - </button>
      <span className="rating-score">{ score }</span>
      <button className="rating-action increment" onClick={incrementScore}> + </button>
    </div>
  );
};

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 02
STEPS["step-02-class-component"] = (
    "// Step 02 - Convert Rating to a class component\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 02】将 Rating 从函数组件改写为继承自 React.Component 的类组件，
// 在 render() 方法中通过 this.props.score 读取父组件传入的评分
class Rating extends React.Component {
  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.props.score }</span>
        <button className="rating-action increment"> + </button>
      </div>
    );
  }
}

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 03
STEPS["step-03-initial-state"] = (
    "// Step 03 - Give Rating its own state\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 03】使用类属性语法初始化组件自身状态 state，
// 以 this.props.score 作为初始值，并在渲染时读取 this.state.score
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment"> + </button>
      </div>
    );
  }
}

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 04
STEPS["step-04-click-handler"] = (
    "// Step 04 - Handle the click event\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 04】定义点击事件处理方法 incrementScore，
// 并把函数引用 this.incrementScore（不带括号）传给 + 按钮的 onClick 属性
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  incrementScore() {
    console.log('From incrementScore!');
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 05
STEPS["step-05-set-state"] = (
    "// Step 05 - Update state with this.setState() (and fix this)\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 05】将 incrementScore 改写为箭头函数类属性以自动绑定当前组件实例 this，
// 并调用 this.setState() 更新分数并触发组件重新渲染
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  incrementScore = () => {
    this.setState({
      score: this.state.score + 1
    });
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 06
STEPS["step-06-prev-state"] = (
    "// Step 06 - Update state from previous state (prevState)\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + '''// 【作答部分 - Step 06】向 this.setState() 传入回调函数 prevState => ({ ... })，
// 确保基于最新的前一个状态计算新分数，避免多次更新合并时读取陈旧的 this.state
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  incrementScore = () => {
    this.setState( prevState => ({
      score: prevState.score + 1
    }));
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}

''' + FOOTER + APP_FUNCTION_INITIAL
)

# Step 07
RATING_STEP_07 = '''// 【作答部分 - Step 07】完善加减分逻辑与 0~5 分边界限制：
// 1. incrementScore 使用 Math.min(..., 5) 限制最高 5 分
// 2. decrementScore 使用 Math.max(..., 0) 限制最低 0 分
// 3. 在按钮上绑定 onClick，并在到达边界（0 或 5）时设置 disabled 属性
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  incrementScore = () => {
    this.setState( prevState => ({
      score: Math.min(prevState.score + 1, 5)
    }));
  }

  decrementScore = () => {
    this.setState( prevState => ({
      score: Math.max(prevState.score - 1, 0)
    }));
  }

  render() {
    return (
      <div className="rating">
        <button
          className="rating-action decrement"
          onClick={this.decrementScore}
          disabled={this.state.score === 0}
        > - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button
          className="rating-action increment"
          onClick={this.incrementScore}
          disabled={this.state.score === 5}
        > + </button>
      </div>
    );
  }
}

'''

STEPS["step-07-decrement-bounds"] = (
    "// Step 07 - Complete Rating: decrement and 0-5 bounds\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + RATING_STEP_07 + FOOTER + APP_FUNCTION_INITIAL
)

# Step 09
STEPS["step-09-app-state"] = (
    "// Step 09 - Move the movies array into App state\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + MOVIE_BASIC + RATING_STEP_07 + FOOTER + '''// 【作答部分 - Step 09】将 App 改写为类组件，把电影数组存入 this.state.movies，
// 并将 render() 中原先读取 props.initialMovies 的三处全部改为读取 this.state.movies
class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  render() {
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;

    return (
      <div className="watchlist">
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
        />

        {/* Movie list */}
        {this.state.movies.map( movie =>
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
'''
)

# Step 10
STEPS["step-10-remove-items"] = (
    "// Step 10 - Remove a movie: passing a function down as a prop\n"
    + MOVIES_FULL + HEADER_BASIC + MOVIE_DETAILS_STATIC + '''const Movie = (props) => {
  return (
    <div className="movie">
      {/* 【作答部分 - Step 10】添加删除按钮，点击时通过箭头函数调用父组件传入的 props.removeMovie(props.id) */}
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

''' + RATING_STEP_07 + FOOTER + '''class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  // 【作答部分 - Step 10】使用 filter() 过滤掉被删除的电影 id，返回新数组更新 state
  handleRemoveMovie = (id) => {
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
        {/* 【作答部分 - Step 10】当列表为空时渲染提示信息 */}
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
'''
)

# Step 11
HEADER_WITH_AVG = '''const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
      {/* 【作答部分 - Step 11】显示平均评分胶囊标签 */}
      <span className="stats">Avg rating: { props.averageRating }</span>
    </header>
  );
};

'''

RATING_STATELESS = '''// 【作答部分 - Step 11】状态提升后，Rating 改回无状态函数组件：
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

'''

STEPS["step-11-lift-state-up"] = (
    "// Step 11 - Lift state up: one source of truth for ratings\n"
    + MOVIES_FULL + HEADER_WITH_AVG + MOVIE_DETAILS_STATIC + '''const Movie = (props) => {
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

''' + RATING_STATELESS + FOOTER + '''class App extends React.Component {
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
'''
)

# Step 12
MOVIE_DETAILS_INTERACTIVE = '''// Returns two sibling spans with no wrapper element
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
            将原本的 <span> 替换为 <button>，点击时调用 props.toggleWatched(props.id) 切换已看状态 */}
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

'''

MOVIE_INTERACTIVE = '''const Movie = (props) => {
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
          /* 【作答部分 - Step 12】向 MovieDetails 传递 id 和 toggleWatched 回调 */
          id={props.id}
          toggleWatched={props.toggleWatched}
        />
      </div>

      <Rating
        score={props.rating}
        id={props.id}
        changeRating={props.changeRating}
      />
    </div>
  );
};

'''

STEPS["step-12-toggle-watched"] = (
    "// Step 12 - Your turn: toggle WATCHED\n"
    + MOVIES_FULL + HEADER_WITH_AVG + MOVIE_DETAILS_INTERACTIVE + MOVIE_INTERACTIVE + RATING_STATELESS + FOOTER + '''class App extends React.Component {
  state = {
    movies: this.props.initialMovies
  };

  handleRemoveMovie = (id) => {
    this.setState( prevState => ({
      movies: prevState.movies.filter( movie => movie.id !== id )
    }));
  }

  handleRatingChange = (delta, id) => {
    this.setState( prevState => ({
      movies: prevState.movies.map( movie =>
        movie.id === id
          ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
          : movie
      )
    }));
  }

  // 【作答部分 - Step 12 (Your turn)】切换匹配 id 电影的 watched 布尔值（!movie.watched）
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
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;
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
            toggleWatched={this.handleToggleWatched}
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
'''
)

# Step 13 (Final)
with open(os.path.join(HERE, "starter", "app.js"), "r", encoding="utf-8") as f:
    STEPS["step-13-use-state-final"] = f.read()


def main():
    checkpoints_root = os.path.join(HERE, "checkpoints")
    if os.path.exists(checkpoints_root):
        shutil.rmtree(checkpoints_root)
    os.makedirs(checkpoints_root, exist_ok=True)

    for name, js in STEPS.items():
        d = os.path.join(checkpoints_root, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(INDEX_HTML)
        with open(os.path.join(d, "app.js"), "w", encoding="utf-8") as f:
            f.write(js)
        shutil.copy(CSS, os.path.join(d, "app.css"))
    print("wrote", len(STEPS), "Part 2 checkpoints")


if __name__ == "__main__":
    main()
