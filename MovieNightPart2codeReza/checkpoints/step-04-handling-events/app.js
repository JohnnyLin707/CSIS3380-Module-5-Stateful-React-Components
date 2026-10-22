// Step 04 - handling a click
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

// 页脚组件：显示已看电影数和电影总数
const Footer = (props) => {
  return (
    <footer>
      Watched { props.watchedCount } of { props.totalMovies } · Made with React
    </footer>
  );
};

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

// 把 App 组件渲染到 id 为 root 的 DOM 节点，并传入电影初始数据
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App initialMovies={movies} />);
