#!/usr/bin/env python3
"""Write one folder per Part 2 step, each holding the finished code for that step.

Students keep building the movie-night/ folder from Part 1. These checkpoint folders are
what the instructor opens to catch a student up, or to show the finished state of a step.
The starter (code/starter/) is Part 1's finished app plus the Part 2 CSS additions.
Re-run this script after editing any step below.
"""

# 为 Part 2 的每一步生成一个文件夹，每个文件夹保存该步骤完成后的代码。
# 学生从 Part 1 的 movie-night/ 文件夹继续开发；这些 checkpoint 文件夹供老师
# 用于帮学生跟进进度，或展示某个步骤的完成状态。
# starter（code/starter/）是 Part 1 完成的应用加上 Part 2 新增的 CSS。
# 修改下面任何步骤后，请重新运行本脚本。

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
STARTER = os.path.join(HERE, "starter")

# ------------------------------------------------------------------ shared pieces

MOVIES = '''// 电影数据源数组：每部电影包含标题、年份、类型、评分、是否看过、是否编辑推荐和唯一 id
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
'''

HEADER_1 = '''
// 页头组件：显示应用标题和电影总数
const Header = (props) => {
  return (
    <header>
      <h1>{ props.title }</h1>
      <span className="stats">Movies: { props.totalMovies }</span>
    </header>
  );
};
'''

HEADER_2 = '''
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
'''

DETAILS_1 = '''
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
'''

DETAILS_2 = '''
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
      {/* 年份与类型；“看过/未看”徽章改为按钮，点击调用父组件的 toggleWatched 切换状态 */}
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
'''

MOVIE_1 = '''
// 单部电影条目组件：左侧为电影信息，右侧为评分组件
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

      {/* 评分组件，显示该电影的评分 */}
      <Rating score={props.rating} />
    </div>
  );
};
'''

MOVIE_2 = '''
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
'''

MOVIE_3 = '''
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
'''

MOVIE_4 = '''
// 单部电影条目组件：删除按钮 + 电影信息（可切换看过状态）+ 受控评分组件
const Movie = (props) => {
  return (
    <div className="movie">
      <button className="remove-movie" onClick={() => props.removeMovie(props.id)}>✖</button>
      <div className="movie-info">
        {/* 把 id 和 toggleWatched 传给 MovieDetails，实现“看过/未看”切换 */}
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

      {/* 受控评分组件：评分值来自 props，点击时通知父组件修改 */}
      <Rating
        score={props.rating}
        id={props.id}
        changeRating={props.changeRating}
      />
    </div>
  );
};
'''

RATING_LET = '''
// An experiment: can an ordinary variable remember the score?
// 一个实验：普通变量能记住评分吗？（答案：不能，渲染之后修改变量不会更新界面）
const Rating = (props) => {
  // 把 props.score 复制到普通局部变量 score
  let score = props.score;

  // 点击“+”时把 score 加 1，并在控制台打印；但界面不会更新
  const increment = () => {
    score = score + 1;
    console.log('score is now', score);
  };

  return (
    <div className="rating">
      <button className="rating-action decrement"> - </button>
      <span className="rating-score">{ score }</span>
      <button className="rating-action increment" onClick={increment}> + </button>
    </div>
  );
};
'''

RATING_CLASS = '''
// Rating as a class component
// 用类组件的方式重写 Rating 组件（还没有任何交互）
class Rating extends React.Component {
  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        {/* 类组件中通过 this.props 访问 props */}
        <span className="rating-score">{ this.props.score }</span>
        <button className="rating-action increment"> + </button>
      </div>
    );
  }
}
'''

RATING_STATE = '''
// Rating owns its score in state
// Rating 组件把评分保存在自己的 state 中（组件自己的记忆）
class Rating extends React.Component {
  // 初始化状态：用传入的 props.score 作为初始评分
  state = {
    score: this.props.score
  };

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        {/* 类组件中通过 this.state 访问状态，界面显示的是状态值 */}
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment"> + </button>
      </div>
    );
  }
}
'''

RATING_EVENT = '''
// handling a click
// 处理一次点击事件：给“+”按钮绑定 onClick 事件处理器
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  // 点击“+”时触发的事件处理方法（暂时只在控制台打印）
  incrementScore() {
    console.log('Hi, from inside incrementScore!');
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        {/* 把 incrementScore 绑定到“+”按钮的点击事件 */}
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}
'''

RATING_BROKEN = '''
// setState() inside a method: BROKEN on purpose ('this' is undefined)
// 在方法里调用 setState()：故意写错（'this' 是 undefined，点击会报错）
// 因为普通方法作为回调时 this 会丢失，这是为了演示问题所在
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  // 这里 this 在点击时会变成 undefined，访问 this.state / this.setState 会报错
  incrementScore() {
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
'''

RATING_BOUND = '''
// arrow-function class fields keep 'this'
// 使用箭头函数类属性可以绑定 this，解决上一步 this 丢失的问题
class Rating extends React.Component {
  state = {
    score: this.props.score
  };

  // 箭头函数写法：自动继承定义处的 this，点击时 this 指向组件实例
  incrementScore = () => {
    // 调用 setState 更新评分：当前评分 +1
    this.setState({
      score: this.state.score + 1
    });
  }

  // 箭头函数写法：评分 -1
  decrementScore = () => {
    this.setState({
      score: this.state.score - 1
    });
  }

  render() {
    return (
      <div className="rating">
        {/* 两个按钮分别绑定加/减分方法 */}
        <button className="rating-action decrement" onClick={this.decrementScore}> - </button>
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment" onClick={this.incrementScore}> + </button>
      </div>
    );
  }
}
'''

RATING_PREV = '''
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
'''

RATING_LIFTED = '''
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
'''

FOOTER = '''
// 页脚组件：显示已看电影数和电影总数
const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};
'''

APP_FUNC = '''
// 应用根组件（函数组件版本）：从 props.initialMovies 读取电影列表
const App = (props) => {
  // 统计已看过的电影数量
  const watchedCount = props.initialMovies.filter(movie => movie.watched).length;

  return (
    <div className="watchlist">
      {/* 页头：标题 + 电影总数 */}
      <Header
        title="Movie Night"
        totalMovies={props.initialMovies.length}
      />

      {/* Movie list */}
      {/* 电影列表：遍历数组，为每部电影渲染一个 Movie 组件；key 用电影 id 保证高效更新 */}
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

      {/* 页脚：已看数量与总数 */}
      <Footer
        watchedCount={watchedCount}
        totalMovies={props.initialMovies.length}
      />
    </div>
  );
};
'''

APP_STATE = '''
// The movie list moves into App's state
// 电影列表移入 App 组件的 state 中管理（应用级状态的起点）
class App extends React.Component {
  // 用传入的初始电影数组初始化 state
  state = {
    movies: this.props.initialMovies
  };

  render() {
    // 每次渲染都从 state 统计已看电影数
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;

    return (
      <div className="watchlist">
        {/* 页头数据全部来自 state */}
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
        />

        {/* Movie list */}
        {/* 电影列表：遍历 state 中的电影数组渲染 Movie 组件 */}
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
'''

APP_REMOVE = '''
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
'''

APP_LIFT = '''
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
'''

APP_TOGGLE = '''
// toggling watched
// 切换“看过”状态：点击徽章时反转该电影的 watched 值
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

  // 修改评分：delta 为 +1 或 -1；限制在 0~5
  handleRatingChange = (delta, id) => {
    this.setState( prevState => ({
      movies: prevState.movies.map( movie =>
        movie.id === id
          ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
          : movie
      )
    }));
  }

  // 切换看过状态：用展开运算符复制该电影对象并反转 watched
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
    // 总分与平均评分
    const totalStars = this.state.movies.reduce((sum, movie) => sum + movie.rating, 0);
    const averageRating = this.state.movies.length > 0
      ? (totalStars / this.state.movies.length).toFixed(1)
      : '–';

    return (
      <div className="watchlist">
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
          averageRating={averageRating}
        />

        {/* Movie list */}
        {/* 列表为空时显示提示文字 */}
        {this.state.movies.length === 0 &&
          <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

        {/* 遍历渲染电影，把删除、改评分、切换看过三个函数传给每个 Movie */}
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
'''

APP_HOOKS = '''
// The same app with the useState hook. This is the finished Part 2 app.
// 用 useState Hook 重写同一个应用：这是 Part 2 的最终完成版
const App = (props) => {
  // 用 useState 管理电影列表状态，初始值为传入的 initialMovies
  const [movies, setMovies] = useState(props.initialMovies);

  // 删除指定 id 的电影：基于前一个状态过滤
  const handleRemoveMovie = (id) => {
    setMovies( prevMovies => prevMovies.filter( movie => movie.id !== id ) );
  };

  // 修改评分：delta 为 +1 或 -1；用 Math.min/Math.max 限制在 0~5
  const handleRatingChange = (delta, id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
        : movie
    ));
  };

  // 切换看过状态：反转该电影的 watched
  const handleToggleWatched = (id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, watched: !movie.watched }
        : movie
    ));
  };

  // 派生数据：已看电影数、总分、平均评分（列表为空显示占位符）
  const watchedCount = movies.filter(movie => movie.watched).length;
  const totalStars = movies.reduce((sum, movie) => sum + movie.rating, 0);
  const averageRating = movies.length > 0
    ? (totalStars / movies.length).toFixed(1)
    : '–';

  return (
    <div className="watchlist">
      {/* 页头：标题、电影总数、平均评分 */}
      <Header
        title="Movie Night"
        totalMovies={movies.length}
        averageRating={averageRating}
      />

      {/* Movie list */}
      {/* 列表为空时显示提示文字 */}
      {movies.length === 0 &&
        <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

      {/* 遍历渲染电影，把删除、改评分、切换看过三个函数传给每个 Movie */}
      {movies.map( movie =>
        <Movie
          title={movie.title}
          year={movie.year}
          genre={movie.genre}
          rating={movie.rating}
          watched={movie.watched}
          staffPick={movie.staffPick}
          id={movie.id}
          key={movie.id.toString()}
          removeMovie={handleRemoveMovie}
          changeRating={handleRatingChange}
          toggleWatched={handleToggleWatched}
        />
      )}

      {/* 页脚：已看数量与总数 */}
      <Footer
        watchedCount={watchedCount}
        totalMovies={movies.length}
      />
    </div>
  );
};
'''

RENDER = '''
// 把 App 组件渲染到 id 为 root 的 DOM 节点，并传入电影初始数据
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
'''


def build(comment, rating, movie=MOVIE_1, details=DETAILS_1, header=HEADER_1, app=APP_FUNC, top=""):
    return (f"// {comment}\n" + top + MOVIES + header + details + movie + rating + FOOTER + app + RENDER)


STEPS = {
    "step-01-plain-variable": build("Step 01 - an ordinary variable cannot drive the UI", RATING_LET),
    "step-02-class-component": build("Step 02 - Rating as a class component", RATING_CLASS),
    "step-03-stateful-component": build("Step 03 - Rating owns its score in state", RATING_STATE),
    "step-04-handling-events": build("Step 04 - handling a click", RATING_EVENT),
    "step-05-broken-this": build("Step 05 - setState() inside a method: BROKEN on purpose ('this' is undefined)",
                                 RATING_BROKEN),
    "step-06-bind-handlers": build("Step 06 - arrow-function class fields keep 'this'", RATING_BOUND),
    "step-07-previous-state": build("Step 07 - updating state from the previous state", RATING_PREV),
    "step-09-application-state": build("Step 09 - the movie list moves into App's state", RATING_PREV,
                                       app=APP_STATE),
    "step-10-remove-items": build("Step 10 - removing items from state", RATING_PREV, movie=MOVIE_2,
                                  app=APP_REMOVE),
    "step-11-lift-state-up": build("Step 11 - ratings lifted up into App's state", RATING_LIFTED,
                                   movie=MOVIE_3, header=HEADER_2, app=APP_LIFT),
    "step-12-toggle-watched": build("Step 12 - toggling watched", RATING_LIFTED, movie=MOVIE_4,
                                    details=DETAILS_2, header=HEADER_2, app=APP_TOGGLE),
    "step-13-use-state-final": build("Step 13 - the same app with the useState hook. This is the finished Part 2 app.",
                                     RATING_LIFTED, movie=MOVIE_4, details=DETAILS_2, header=HEADER_2,
                                     app=APP_HOOKS, top="const { useState } = React;\n\n"),
}


def main():
    for name, js in STEPS.items():
        d = os.path.join(HERE, "checkpoints", name)
        os.makedirs(d, exist_ok=True)
        for f in ("index.html", "app.css"):
            shutil.copy(os.path.join(STARTER, f), os.path.join(d, f))
        with open(os.path.join(d, "app.js"), "w") as f:
            f.write(js)
    print("wrote", len(STEPS), "checkpoints")


if __name__ == "__main__":
    main()
