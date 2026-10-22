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

MOVIES = '''// 作用：电影数据源数组——每部电影包含标题、年份、类型、评分、是否看过、是否编辑推荐和唯一 id
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
'''

HEADER_1 = '''
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
'''

HEADER_2 = '''
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
'''

DETAILS_1 = '''
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
'''

DETAILS_2 = '''
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
'''

MOVIE_1 = '''
// 单部电影条目组件：左侧为电影信息，右侧为评分组件
// 作用：Movie 组件——一部电影在列表中的一行，左边是信息，右边是评分
// 解释：把一行电影拆成"信息 + 评分"两个子组件，各自负责一块 UI；
//       数据从 props 流入，组件本身无状态（Part 1 阶段）
//       参考：Movie Night Part 1 的 Movie 组件代码
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

      {/* 作用：评分组件，显示该电影的评分 */}
      {/* 解释：Rating 只接收一个 score 数值，完全依赖父组件传入；
              参考：下方 Rating 组件的定义 */}
      <Rating score={props.rating} />
    </div>
  );
};
'''

MOVIE_2 = '''
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
'''

MOVIE_3 = '''
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
'''

MOVIE_4 = '''
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
'''

RATING_LET = '''
// An experiment: can an ordinary variable remember the score?
// 一个实验：普通变量能记住评分吗？（答案：不能，渲染之后修改变量不会更新界面）
// 作用：实验组件——把 props.score 复制到普通局部变量 score，点击"+"时把它加一
// 解释：这是为了证明"普通变量不能驱动界面"：点击后控制台数字会变，
//       但页面上的分数毫无反应，因为 React 不知道这个变量变了、不会重新渲染
//       参考：Movie-Night-Part-2-State-Tutorial.pdf 教程第二章的实验
const Rating = (props) => {
  // 作用：把 props.score 复制到普通局部变量 score
  // 解释：每次渲染都会重新执行这个赋值，score 只是当次渲染的临时副本，
  //       渲染结束后它就"死"了，这正是问题所在
  //       参考：教程中对"渲染"概念的讲解
  let score = props.score;

  // 作用：点击"+"时把 score 加 1，并在控制台打印；但界面不会更新
  // 解释：普通赋值不会通知 React，所以不会触发重新渲染；
  //       解决方法从下一步开始引入——把 score 搬进组件的 state
  //       参考：下一步（Step 02）把 Rating 改写为类组件
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
// 作用：把 Rating 从函数组件改写为类组件，通过 this.props 读取传入的评分
// 解释：类组件是"有状态组件"的载体——下一步就要把 score 存进 this.state；
//       注意此时评分仍然只读，点击还没有效果
//       参考：教程第三章；对比本目录中函数组件写法的区别
class Rating extends React.Component {
  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        {/* 作用：显示评分——类组件中通过 this.props.score 访问 props */}
        {/* 解释：类组件里 props 挂在 this 上，写法是 this.props.xxx，
                与函数组件的 props.xxx 相比只是多一个 this
                参考：Movie Night Part 1 中函数组件 props 的用法 */}
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
// 作用：给类组件加 state——用 state = { score: this.props.score } 让组件拥有自己的记忆
// 解释：放进 state 的数据变化时，React 会自动重新渲染界面；
//       初始值取自 props.score，之后就不再跟随 props（组件自己说了算）
//       参考：教程第四章；React 官方文档 State and Lifecycle
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式，
  //       等效于在 constructor 里写 this.state = {...}
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        {/* 作用：显示评分——类组件中通过 this.state.score 读取状态 */}
        {/* 解释：界面显示的是 this.state.score 而不是 props.score，
                从此组件的分数由自己管理
                参考：上方 state 的初始化代码 */}
        <span className="rating-score">{ this.state.score }</span>
        <button className="rating-action increment"> + </button>
      </div>
    );
  }
}
'''

RATING_EVENT = '''
// handling a click
// 处理一次点击事件：给"+"按钮绑定 onClick 事件处理器
// 作用：给"+"按钮绑定 onClick={this.incrementScore}，并定义对应的事件处理方法
// 解释：React 事件用驼峰命名（onClick 而不是 onclick），绑定的是函数引用；
//       此时方法里只打印一句话，先验证"点击确实触发了"
//       参考：教程第五章；React 官方文档 Handling Events
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  // 作用：点击"+"时触发的事件处理方法（暂时只在控制台打印）
  // 解释：先只打印不改状态，是为了确认事件链路（按钮→方法）已经通；
  //       下一步再在方法里调用 setState 真正改分
  //       参考：下一步（Step 05）在方法中调用 this.setState
  incrementScore() {
    console.log('Hi, from inside incrementScore!');
  }

  render() {
    return (
      <div className="rating">
        <button className="rating-action decrement"> - </button>
        <span className="rating-score">{ this.state.score }</span>
        {/* 作用：把 incrementScore 绑定到"+"按钮的点击事件 */}
        {/* 解释：onClick 后传函数引用（不带括号），点击时 React 自动调用；
                如果写成 onClick={this.incrementScore()} 会在渲染时立即执行
                参考：React 官方文档 Handling Events 中的注意事项 */}
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
// 作用：在普通方法里调用 this.setState——这一步是故意写错的，点击会报错
// 解释：普通方法作为事件回调时 this 会丢失（变成 undefined），
//       this.setState 就找不到，控制台会报 "Cannot read properties of undefined"
//       参考：教程第六章的问题演示；下一步用箭头函数修复
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  // 作用：加分逻辑本身是对的——把当前评分 +1 后写入 state
  // 解释：问题不在逻辑而在 this：这个方法被当作回调传给按钮时，
  //       this 不再是组件实例，this.state 和 this.setState 都会报错
  //       参考：下一步（Step 06）改用箭头函数类属性修复 this
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
// 作用：把事件处理方法改成箭头函数类属性，修复 this 丢失问题
// 解释：箭头函数没有自己的 this，会沿用定义处（组件实例）的 this，
//       这样无论方法被谁调用，this.setState 都能正确找到组件
//       参考：教程第七章；JavaScript 箭头函数 this 规则（MDN）
class Rating extends React.Component {
  // 作用：初始化状态——用传入的 props.score 作为初始评分
  // 解释：类属性写法 state = {...} 是构造 state 的简写形式
  //       参考：React 官方文档中 "Adding Local State to a Class" 一节
  state = {
    score: this.props.score
  };

  // 作用：箭头函数写法——评分 +1，自动绑定 this
  // 解释：= () => {} 的类属性写法让 this 永远指向组件实例，
  //       从此 onClick={this.incrementScore} 传引用也不会丢 this
  //       参考：上一步（Step 05）普通方法报错的对照
  incrementScore = () => {
    // 作用：调用 setState 更新评分：当前评分 +1
    // 解释：setState 是类组件更新状态的唯一入口，调用后 React 自动重新渲染
    //       参考：React 官方文档 setState 的说明
    this.setState({
      score: this.state.score + 1
    });
  }

  // 作用：箭头函数写法——评分 -1
  // 解释：与 incrementScore 完全对称的写法，一个加一个减
  //       参考：上方 incrementScore 的箭头函数写法
  decrementScore = () => {
    // 作用：调用 setState 更新评分：当前评分 -1
    // 解释：setState 接收一个对象，React 会把它合并进现有 state
    //       参考：上方 incrementScore 中的 setState 用法
    this.setState({
      score: this.state.score - 1
    });
  }

  render() {
    return (
      <div className="rating">
        {/* 作用：两个按钮分别绑定加/减分方法 */}
        {/* 解释：绑定的是箭头函数属性（引用），点击时 this 依然正确；
                参考：上方 incrementScore / decrementScore 的定义 */}
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
'''

RATING_LIFTED = '''
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
'''

FOOTER = '''
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
'''

APP_FUNC = '''
// 应用根组件（函数组件版本）：从 props.initialMovies 读取电影列表
// 作用：App 根组件——组合页头、电影列表、页脚，并计算已看电影数量
// 解释：这是"无状态"版本的 App：电影列表来自 props，无法修改；
//       Step 09 会把这个列表搬进 App 自己的 state
//       参考：Movie Night Part 1 的 App 组件代码；下一步 Step 09
const App = (props) => {
  // 作用：统计已看过的电影数量
  // 解释：filter 返回满足条件的数组，.length 就是数量——这种"从数据派生统计值"
  //       的写法在 Part 2 会反复出现（平均评分同理）
  //       参考：Step 11 中计算 averageRating 的 reduce 写法
  const watchedCount = props.initialMovies.filter(movie => movie.watched).length;

  return (
    <div className="watchlist">
      {/* 作用：页头——标题 + 电影总数 */}
      {/* 解释：标题写死，总数用数组长度动态算出；
              参考：上方 Header 组件对 props.title / props.totalMovies 的定义 */}
      <Header
        title="Movie Night"
        totalMovies={props.initialMovies.length}
      />

      {/* Movie list */}
      {/* 电影列表：遍历数组，为每部电影渲染一个 Movie 组件；key 用电影 id 保证高效更新 */}
      {/* 解释：map 把数组逐项变成 JSX；key 必须是稳定唯一的标识（这里用 id），
              React 靠它判断哪一行变了，用数组下标会在删除时出错
              参考：Movie Night Part 1 的列表渲染代码；React 官方文档 Lists and Keys */}
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

      {/* 作用：页脚——已看数量与总数 */}
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
// 作用：App 改写为类组件，电影列表搬进 this.state，界面数据全部来自 state
// 解释：列表放进 state 后才能增删改——这是整个 Part 2 的转折点；
//       派生数据（已看数量、总数）改为每次渲染时从 state 计算
//       参考：教程第九章；React 官方文档 State and Lifecycle
class App extends React.Component {
  // 作用：用传入的初始电影数组初始化 state
  // 解释：state = {...} 类属性写法，初始值来自 props.initialMovies；
  //       之后 this.state.movies 就是应用的电影数据唯一来源
  //       参考：本文件顶部 movies 数组通过 render 时传入 initialMovies
  state = {
    movies: this.props.initialMovies
  };

  render() {
    // 作用：每次渲染都从 state 统计已看电影数
    // 解释：统计值不存进 state——能从现有数据算出来的就不额外存，
    //       避免两处数据不同步；电影一变这里自动重算
    //       参考：Step 11 中平均评分的同样思路
    const watchedCount = this.state.movies.filter(movie => movie.watched).length;

    return (
      <div className="watchlist">
        {/* 作用：页头数据全部来自 state */}
        {/* 解释：state.movies.length 即当前电影总数，删除后会实时变小；
                参考：上方 state 初始化代码 */}
        <Header
          title="Movie Night"
          totalMovies={this.state.movies.length}
        />

        {/* Movie list */}
        {/* 电影列表：遍历 state 中的电影数组渲染 Movie 组件 */}
        {/* 解释：遍历的数据源从 props.initialMovies 换成 this.state.movies，
                从此列表内容由 state 决定
                参考：React 官方文档 Lists and Keys */}
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

        {/* 作用：页脚——已看数量与总数同样来自 state */}
        {/* 解释：两个数字都由 state.movies 派生，与页头保持同一数据源
                参考：上方 Footer 组件对 props 的定义 */}
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
'''

APP_LIFT = '''
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
'''

APP_TOGGLE = '''
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
'''

APP_HOOKS = '''
// The same app with the useState hook. This is the finished Part 2 app.
// 用 useState Hook 重写同一个应用：这是 Part 2 的最终完成版
// 作用：用函数组件 + useState 重写整个应用——Part 2 的最终完成版
// 解释：Hook 让函数组件也能拥有 state，不必写 class；三种操作
//       （删除/改分/切换看过）全部通过 setMovies 更新，代码更短更易读
//       参考：教程第十三章；React 官方文档 "Using the State Hook"
const App = (props) => {
  // 作用：用 useState 管理电影列表状态，初始值为传入的 initialMovies
  // 解释：useState 返回 [状态, 更新函数]，解构后分别命名；
  //       更新时传函数可拿到最新前值（与类组件函数式 setState 对应）
  //       参考：Step 09-11 类组件 state 的写法对比
  const [movies, setMovies] = useState(props.initialMovies);

  // 作用：删除指定 id 的电影——基于前一个状态过滤
  // 解释：setMovies(prev => ...) 的函数式更新保证连续操作也基于最新数据；
  //       filter 生成不含该电影的新数组（不可变更新）
  //       参考：Step 10 中 handleRemoveMovie 的 filter 写法
  const handleRemoveMovie = (id) => {
    setMovies( prevMovies => prevMovies.filter( movie => movie.id !== id ) );
  };

  // 作用：修改评分——delta 为 +1 或 -1；用 Math.min/Math.max 限制在 0~5
  // 解释：map 找到目标电影后用展开运算符复制并覆盖 rating，其余不动
  //       参考：Step 11 中 handleRatingChange 的写法
  const handleRatingChange = (delta, id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, rating: Math.min(Math.max(movie.rating + delta, 0), 5) }
        : movie
    ));
  };

  // 作用：切换看过状态——反转该电影的 watched
  // 解释：同样是 map + 展开运算符，只覆盖 watched 一个字段
  //       参考：Step 12 中 handleToggleWatched 的写法
  const handleToggleWatched = (id) => {
    setMovies( prevMovies => prevMovies.map( movie =>
      movie.id === id
        ? { ...movie, watched: !movie.watched }
        : movie
    ));
  };

  // 作用：派生数据——已看电影数、总分、平均评分（列表为空显示占位符）
  // 解释：普通变量即可：每次渲染都会重新计算，不需要放进 state；
  //       这也是 Hook 组件与类组件的区别——不是所有数据都要 state
  //       参考：Step 11 中 render 里计算派生数据的同样思路
  const watchedCount = movies.filter(movie => movie.watched).length;
  const totalStars = movies.reduce((sum, movie) => sum + movie.rating, 0);
  const averageRating = movies.length > 0
    ? (totalStars / movies.length).toFixed(1)
    : '–';

  return (
    <div className="watchlist">
      {/* 作用：页头——标题、电影总数、平均评分 */}
      {/* 解释：三个数字全部由 movies 数组派生，state 一变界面自动更新
              参考：Step 11 中 Header 的新增用法 */}
      <Header
        title="Movie Night"
        totalMovies={movies.length}
        averageRating={averageRating}
      />

      {/* Movie list */}
      {/* 作用：列表为空时显示提示文字 */}
      {/* 解释：删光所有电影后显示引导文案；
              参考：Step 10 中同样条件的写法 */}
      {movies.length === 0 &&
        <p className="empty">The watchlist is empty. Time to pick a movie!</p>}

      {/* 作用：遍历渲染电影，把删除、改评分、切换看过三个函数传给每个 Movie */}
      {/* 解释：函数组件里定义的三个 handler 直接作为 props 传下去；
              单一数据源原则不变——只有 App 能改 movies
              参考：Step 12 Movie 组件对三个回调的使用 */}
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

      {/* 作用：页脚——已看数量与总数 */}
      {/* 解释：与页头同源，全部由 movies 派生
              参考：上方 Footer 组件对 props 的定义 */}
      <Footer
        watchedCount={watchedCount}
        totalMovies={movies.length}
      />
    </div>
  );
};
'''

RENDER = '''
// 作用：渲染入口——创建 React 18 根节点，把 App 渲染进 #root，并传入电影数据
// 解释：createRoot 是 React 18 的入口 API；initialMovies 属性把数据交给 App，
//       Step 09 起这份数据会变成 App 内部的 state
//       参考：Movie Night Part 1 的渲染代码；React 官方文档 createRoot
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
                                     app=APP_HOOKS,
                                     top="// 作用：从全局 React 对象中解构出 useState Hook，供函数组件使用\n"
                                         "// 解释：本项目通过 CDN 引入 React，Hook 挂在全局 React 上；\n"
                                         "//       先解构出来，App 组件里直接写 useState 更简洁\n"
                                         "//       参考：React 官方文档 Hooks 一章中 useState 的用法示例\n"
                                         "const { useState } = React;\n\n"),
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
