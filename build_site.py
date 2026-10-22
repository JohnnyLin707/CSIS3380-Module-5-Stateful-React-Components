#!/usr/bin/env python3
# 作用：生成 CSIS3380 Module 5 展示网站的分页面
# 解释：读取三个项目中已添加中文注释的源代码，HTML 转义后嵌入页面模板，
#       生成主页与 counter/planets/movie-night 三个子页面；
#       项目源代码更新后，重新运行 `python3 build_site.py` 即可同步网站
# 参考：生成的页面依赖 assets/css/style.css 与 assets/js/main.js

import html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

GH_REPO = "https://github.com/JohnnyLin707/CSIS3380-Module-5-Stateful-React-Components.git"


# 作用：把文本中的 < > & 转义成 HTML 实体，防止代码内容被浏览器当作标签解析
# 解释：代码里全是 <div>、{ } 这类字符，直接插入 HTML 会破坏页面结构，
#       必须转义后再放进 <code> 元素
def esc(text):
    return html.escape(text, quote=False)


# 作用：生成一个代码面板——左侧行号列 + 右侧带语言标记的高亮代码
# 解释：行号由 Python 预生成（1 到 N 的竖排数字），与代码行一一对应；
#       语言标记（javascript/css/xml）供 highlight.js 选择语法规则；
#       行数按换行符统计，文件末尾无换行时补最后一行
def code_panel(panel_id, filename, source, lang, active=False):
    lines = source.count("\n") + (0 if source.endswith("\n") else 1)
    gutter = "\n".join(str(i) for i in range(1, lines + 1))
    cls = "code-panel" + (" active" if active else "")
    return (
        '<div class="{cls}" id="{pid}">\n'
        '  <div class="code-block">\n'
        '    <div class="code-gutter">{gutter}</div>\n'
        '    <pre><code class="language-{lang}">{code}</code></pre>\n'
        "  </div>\n"
        "</div>\n"
    ).format(cls=cls, pid=panel_id, gutter=esc(gutter), lang=lang, code=esc(source))


# 作用：生成一个文件标签页按钮
# 解释：data-target 指向对应面板的 id，点击切换逻辑在 main.js；
#       按钮文字是文件名，等宽字体显示更贴近代码语境
def tab_button(target, filename, active=False):
    cls = "code-tab" + (" active" if active else "")
    return (
        '<button class="{cls}" data-target="{target}">{name}</button>\n'
    ).format(cls=cls, target=target, name=html.escape(filename))


# 作用：按路径片段读取项目源文件（相对仓库根目录）
# 解释：统一用 UTF-8 读取，保证中文注释不乱码；
#       所有被展示的源码都通过这个函数读取
def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------------ 主页

LANDING = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<!-- 作用：设置视口，让页面在手机等小屏设备上正确缩放 -->
<!-- 解释：移动浏览器默认按桌面宽度渲染再整体缩小，会导致字太小；
        参考：HTML5 响应式页面标准写法（MDN viewport 文档） -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Module 5 · Stateful React Components | CSIS3380</title>
<!-- 作用：页面描述——供搜索引擎和分享预览使用 -->
<meta name="description" content="CSIS3380 Module 5 有状态 React 组件课程项目展示：Counter App、Planet Card App、Movie Night">
<!-- 作用：内联 SVG favicon——渐变圆角方块加 ⚛ 符号 -->
<!-- 解释：data URI 内联避免额外请求和 404；与子页面使用同一图标 -->
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%236366f1'/><stop offset='1' stop-color='%2322d3ee'/></linearGradient></defs><rect width='100' height='100' rx='22' fill='url(%23g)'/><text x='50' y='70' font-size='55' text-anchor='middle' fill='white'>⚛</text></svg>">
<!-- 作用：引入全站样式表与字体 -->
<!-- 解释：主页在仓库根目录，资源路径无需 ../；字体加载失败时
        有系统字体兜底，不影响阅读 -->
<link rel="stylesheet" href="assets/css/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>

<!-- 作用：顶部导航栏——站点品牌 + 课程名 + GitHub 链接 -->
<!-- 解释：主页导航没有"返回"按钮（已在首页），品牌图标点击回到自身；
        SVG 是 GitHub 官方 logo 路径，fill="currentColor" 继承文字颜色 -->
<header class="topbar">
  <a class="brand" href="index.html">
    <span class="logo">⚛</span>
    <span>CSIS3380 · Module 5</span>
  </a>
  <span class="crumb">Full Stack Development With JavaScript</span>
  <div class="spacer"></div>
  <a class="gh-link" href="__GH__" target="_blank" rel="noopener">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
    GitHub
  </a>
</header>

<main class="wrap">

  <!-- 作用：英雄区——徽章、主标题、简介、学生信息标签 -->
  <!-- 解释：标题第二行用 .grad 类做渐变文字；meta 里的 chip 展示
          学生姓名、学号、技术栈等关键信息；
          参考：style.css 中 .hero 相关样式 -->
  <section class="hero">
    <span class="badge"><span class="dot"></span>CSIS 3380 · 2026 · React State</span>
    <h1>Module 5<br><span class="grad">Stateful React Components</span></h1>
    <p class="lead">
      本页面汇总展示 Module 5 的三个 React 项目：双计数器计算器、行星卡片应用，
      以及分 13 步教学的 Movie Night 观影清单。每个项目均可在线实时体验，
      并附带逐行中文注释的完整源码。
    </p>
    <div class="meta">
      <span class="chip">👤 学生：Jinran Lin</span>
      <span class="chip">🆔 学号：300395016</span>
      <span class="chip">⚛ React 18 + Babel</span>
      <span class="chip">📚 共 3 个项目 · 12 个教学步骤</span>
    </div>
  </section>

  <!-- 作用：项目卡片区——三个项目的入口卡片 -->
  <!-- 解释：每张卡片是 <a> 整张可点，链接到 counter/planets/movie-night
          子页面；reveal 类让卡片滚动进入视口时淡入；
          参考：style.css 中 .card 悬停光斑效果（由 main.js 驱动） -->
  <section class="cards">
    <a class="card reveal" href="counter/index.html">
      <span class="icon">🧮</span>
      <h3>Counter App With React</h3>
      <p>双计数器（Counter A / B）加减与重置，实时展示两数之和、差、积、商的四则运算结果，并用 useState 管理组件状态。</p>
      <div class="tags">
        <span class="tag">useState</span>
        <span class="tag">组件通信</span>
        <span class="tag">四则运算</span>
      </div>
      <span class="go">打开项目 <span class="arrow">→</span></span>
    </a>

    <a class="card reveal" href="planets/index.html">
      <span class="icon">🪐</span>
      <h3>Planet Card App</h3>
      <p>八大行星卡片画廊：响应式网格布局、行星档案展示，支持删除单颗行星与一键重置，状态由容器组件统一管理。</p>
      <div class="tags">
        <span class="tag">列表渲染</span>
        <span class="tag">条件渲染</span>
        <span class="tag">CSS Grid</span>
      </div>
      <span class="go">打开项目 <span class="arrow">→</span></span>
    </a>

    <a class="card reveal" href="movie-night/index.html">
      <span class="icon">🎬</span>
      <h3>Movie Night Part 2</h3>
      <p>观影清单应用：从普通变量、类组件 state、事件处理、this 绑定，到状态提升与 useState Hook，共 12 个递进步骤完整掌握 React 状态管理。</p>
      <div class="tags">
        <span class="tag">Class State</span>
        <span class="tag">状态提升</span>
        <span class="tag">Hooks</span>
      </div>
      <span class="go">打开项目 <span class="arrow">→</span></span>
    </a>
  </section>

</main>

<!-- 作用：页脚——课程信息与作者署名 -->
<!-- 解释：与三个子页面的页脚保持相同结构，仅链接指向不同 -->
<footer class="footer">
  <p><span class="atom">⚛</span> CSIS3380 Full Stack Development With JavaScript · Module 5</p>
  <p>Jinran Lin (300395016) · Built with React 18 · Hosted on GitHub Pages</p>
</footer>

<!-- 作用：引入全站交互脚本 -->
<!-- 解释：主页只用其中的卡片光斑与滚动显现两个功能；
        标签页/iframe 控制等逻辑在子页面才会触发（脚本内有存在性判断） -->
<script src="assets/js/main.js"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ 子页面通用模板

def project_page(kicker, title, desc, tags_html, demo_src, demo_label,
                 notes_html, code_html, extra_head=""):
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<!-- 作用：设置视口，让页面在手机等小屏设备上正确缩放 -->
<!-- 解释：没有这行移动浏览器会按桌面宽度渲染再缩小，导致字太小；
        参考：HTML5 响应式页面标准写法（MDN viewport 文档） -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Module 5 · CSIS3380</title>
<!-- 作用：内联 SVG favicon——渐变圆角方块加 ⚛ 符号 -->
<!-- 解释：用 data URI 内联，省一次 favicon.ico 请求，也不会有 404；
        参考：三个项目页面均使用同一图标保持整站一致 -->
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%236366f1'/><stop offset='1' stop-color='%2322d3ee'/></linearGradient></defs><rect width='100' height='100' rx='22' fill='url(%23g)'/><text x='50' y='70' font-size='55' text-anchor='middle' fill='white'>⚛</text></svg>">
<!-- 作用：引入全站样式表 -->
<!-- 解释：子页面在 assets/css/ 的上一级，所以路径是 ../assets/；
        参考：assets/css/style.css 文件顶部的样式说明 -->
<link rel="stylesheet" href="../assets/css/style.css">
<!-- 作用：预连接并加载 Google Fonts（Inter + JetBrains Mono） -->
<!-- 解释：preconnect 提前建立连接加快字体加载；等宽字体专门给代码区用；
        本地已设系统字体兜底，加载失败也不影响阅读 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<!-- 作用：引入 highlight.js——为代码区提供语法高亮 -->
<!-- 解释：从 CDN 加载后，在 DOMContentLoaded 时调用 hljs.highlightAll()
        自动着色页面中所有 <code>；配色主题在 style.css 中自定义 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>document.addEventListener("DOMContentLoaded", function () {{ if (window.hljs) {{ hljs.highlightAll(); }} }});</script>
{extra_head}
</head>
<body>

<!-- 作用：顶部导航栏——返回首页按钮 + 当前项目名 + GitHub 链接 -->
<!-- 解释：三个子页面共用此结构；返回链接指向上级目录的主页；
        参考：style.css 中 .topbar 相关样式 -->
<header class="topbar">
  <a class="back-link" href="../index.html">← 返回首页</a>
  <span class="crumb">{crumb}</span>
  <div class="spacer"></div>
  <a class="gh-link" href="{gh}" target="_blank" rel="noopener">GitHub</a>
</header>

<main class="wrap">

  <!-- 作用：项目标题区——分类标签、标题、描述、技术标签 -->
  <!-- 解释：内容由 build_site.py 的各 build_xxx() 函数参数填入；
          参考：counter/index.html 等同名页面实际效果 -->
  <section class="page-hero">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p>{desc}</p>
    <div class="tags">{tags}</div>
  </section>

  <!-- 作用：实时演示区——浏览器模拟框内嵌运行中的项目 -->
  <!-- 解释：iframe 的 src 指向真实项目目录的 index.html，
          学生可以直接在框里点击按钮体验；重载/新窗口按钮由 main.js 实现；
          参考：../assets/js/main.js 中演示 iframe 相关代码 -->
  <section class="section reveal">
    <h2 class="section-title">实时演示</h2>
    <p class="section-sub">下方嵌入运行中的项目（需联网加载 React CDN）。可直接在iframe中操作，或在新窗口中打开。</p>
    <div class="browser-frame">
      <div class="browser-bar">
        <div class="dots"><span></span><span></span><span></span></div>
        <div class="url" id="demo-url">{demo_label}</div>
        <div class="actions">
          <button class="mini-btn" id="btn-reload" type="button">↻ 重载</button>
          <button class="mini-btn" id="btn-open" type="button">↗ 新窗口</button>
        </div>
      </div>
      <div class="browser-body">
        <iframe id="demo-frame" src="{demo_src}" title="{title} live demo" loading="lazy"></iframe>
      </div>
    </div>
  </section>

  <!-- 作用：项目说明区——若干技术要点小卡片 -->
  <!-- 解释：notes_html 由 build_counter/build_planets/build_movie_night
          各自生成，说明本项目的核心知识点；
          参考：style.css 中 .note 卡片样式 -->
  <section class="section reveal">
    <h2 class="section-title">项目说明</h2>
    <div class="notes">{notes}</div>
  </section>

  <!-- 作用：源码区——带行号和语法高亮的代码浏览器 -->
  <!-- 解释：code_html 由 code_panel()/tab_button() 生成：
          每个文件一个面板，面板内含行号列和高亮代码；
          Movie Night 页面此处是 12 个步骤的代码容器；
          参考：build_site.py 顶部的 code_panel() 函数 -->
  <section class="section reveal">
    <h2 class="section-title">源码（含中文注释）</h2>
    <p class="section-sub">老师原有英文注释后附中文翻译，代码补全部分以中文注释说明作用。点击标签页切换文件。</p>
    {code}
  </section>

</main>

<!-- 作用：页脚——课程信息与作者署名 -->
<!-- 解释：与主页页脚结构一致，GitHub 链接指向本仓库 -->
<footer class="footer">
  <p><span class="atom">⚛</span> CSIS3380 Full Stack Development With JavaScript · Module 5</p>
  <p>Jinran Lin (300395016) · <a href="{gh}" target="_blank" rel="noopener">GitHub Repository</a></p>
</footer>

<!-- 作用：引入全站交互脚本 -->
<!-- 解释：放在 body 末尾，保证操作 DOM 时元素已渲染完成；
        参考：../assets/js/main.js 文件顶部的功能说明 -->
<script src="../assets/js/main.js"></script>
</body>
</html>
""".format(title=html.escape(title), crumb=html.escape(title),
           gh=GH_REPO, kicker=html.escape(kicker), desc=desc, tags=tags_html,
           demo_src=demo_src, demo_label=html.escape(demo_label),
           notes=notes_html, code=code_html, extra_head=extra_head)


# ------------------------------------------------------------------ Counter 子页面

def build_counter():
    base = "CounterAppWithReact-300395016-JinranLin"
    files = [
        ("index.html", "index.html", "xml"),
        ("statelab.js", "statelab.js", "javascript"),
        ("styles.css", "styles.css", "css"),
    ]
    tabs, panels = [], []
    for i, (label, fname, lang) in enumerate(files):
        pid = "panel-%s" % fname.replace(".", "-")
        tabs.append(tab_button("#" + pid, label, active=(i == 0)))
        panels.append(code_panel(pid, fname, read(base, fname), lang, active=(i == 0)))

    code = (
        '<div class="code-shell" data-tabs>\n'
        '  <div class="code-tabs">\n' + "".join(tabs) +
        '    <span class="spacer"></span>\n'
        '    <button class="copy-btn" type="button" data-copy="#panel-index-html">复制代码</button>\n'
        "  </div>\n" + "".join(panels) + "</div>\n"
    )

    notes = (
        '<div class="note"><h4>useState 状态管理</h4><p>Counter A 初始为 0、Counter B 初始为 1，'
        "分别用独立的 state 保存，互不影响。</p></div>"
        '<div class="note"><h4>组件化拆分</h4><p>CounterSection 负责单个计数器面板，'
        "Results 负责四则运算展示，App 负责状态与组合。</p></div>"
        '<div class="note"><h4>受控交互</h4><p>所有按钮通过 setCount 更新状态，'
        "界面随状态自动重新渲染，包括一键全部重置。</p></div>"
    )

    tags = ('<span class="tag">React 18</span><span class="tag">useState</span>'
            '<span class="tag">JSX</span><span class="tag">Props</span>')

    page = project_page(
        kicker="Project 01 · Counter",
        title="Counter App With React",
        desc="一个双计数器应用：Counter A 与 Counter B 均可递增、递减、重置，"
             "页面底部实时计算并展示两个数字的和、差、积、商（除数为零时给出提示）。"
             "通过本项目练习 useState 状态管理、组件拆分与 props 传递。",
        tags_html=tags,
        demo_src="../%s/index.html" % base,
        demo_label="../%s/index.html" % base,
        notes_html=notes,
        code_html=code,
    )
    out = os.path.join(ROOT, "counter")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


# ------------------------------------------------------------------ Planets 子页面

def build_planets():
    base = "PlanetCardApp-300395016-JinranLin"
    files = [
        ("index.html", "index.html", "xml"),
        ("app.js", "app.js", "javascript"),
        ("style.css", "style.css", "css"),
        ("html-template.html", "html-template.html", "xml"),
    ]
    tabs, panels = [], []
    for i, (label, fname, lang) in enumerate(files):
        pid = "panel-%s" % fname.replace(".", "-")
        tabs.append(tab_button("#" + pid, label, active=(i == 0)))
        panels.append(code_panel(pid, fname, read(base, fname), lang, active=(i == 0)))

    code = (
        '<div class="code-shell" data-tabs>\n'
        '  <div class="code-tabs">\n' + "".join(tabs) +
        '    <span class="spacer"></span>\n'
        '    <button class="copy-btn" type="button" data-copy="#panel-index-html">复制代码</button>\n'
        "  </div>\n" + "".join(panels) + "</div>\n"
    )

    notes = (
        '<div class="note"><h4>数据驱动视图</h4><p>8 颗行星的数据存于数组中，'
        "通过 map 遍历渲染成卡片，修改数据即更新界面。</p></div>"
        '<div class="note"><h4>删除与重置</h4><p>点击 Remove 用 filter 移除对应行星；'
        "Reset 一键恢复完整列表，标题实时显示剩余数量。</p></div>"
        '<div class="note"><h4>条件渲染</h4><p>列表为空时显示 "No planets left!" 提示，'
        "否则展示响应式 CSS Grid 卡片墙。</p></div>"
    )

    tags = ('<span class="tag">React 18</span><span class="tag">useState</span>'
            '<span class="tag">列表渲染</span><span class="tag">CSS Grid</span>')

    page = project_page(
        kicker="Project 02 · Planets",
        title="Planet Card App",
        desc="八大行星卡片应用：以响应式网格展示太阳系八大行星的图片、直径、卫星数量与简介，"
             "支持删除单颗行星和一键重置。本项目练习列表渲染、条件渲染与组件状态管理。",
        tags_html=tags,
        demo_src="../%s/index.html" % base,
        demo_label="../%s/index.html" % base,
        notes_html=notes,
        code_html=code,
    )
    out = os.path.join(ROOT, "planets")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


# ------------------------------------------------------------------ Movie Night 子页面

STEPS = [
    ("step-01-plain-variable", "Step 01 · 普通变量",
     "实验：把评分存到普通局部变量里，点击后控制台数字变了，界面却不变——说明普通变量无法驱动 UI。"),
    ("step-02-class-component", "Step 02 · 类组件",
     "把 Rating 改写为 class 组件，通过 this.props 读取传入的评分，暂时还没有交互。"),
    ("step-03-stateful-component", "Step 03 · 有状态组件",
     "用 state = { score: this.props.score } 让组件拥有自己的记忆，界面显示 this.state.score。"),
    ("step-04-handling-events", "Step 04 · 处理事件",
     "给“+”按钮绑定 onClick={this.incrementScore}，点击时在控制台打印，验证事件处理器已连接。"),
    ("step-05-broken-this", "Step 05 · this 丢失（故意写错）",
     "在普通方法里调用 this.setState 会报错——因为作为回调时 this 变成 undefined。此步用于演示问题。"),
    ("step-06-bind-handlers", "Step 06 · 绑定处理器",
     "改用箭头函数类属性 incrementScore = () => {...}，自动绑定 this，加减分按钮都能正常工作。"),
    ("step-07-previous-state", "Step 07 · 基于前一个状态更新",
     "用函数式 setState(prevState => ...) 基于前值更新，并用 Math.min/Math.max 把评分限制在 0~5，到边界禁用按钮。"),
    ("step-09-application-state", "Step 09 · 应用级状态",
     "把电影列表移入 App 组件的 state，页头的电影总数、页脚的已看数量都从 state 派生。"),
    ("step-10-remove-items", "Step 10 · 删除条目",
     "新增删除按钮：handleRemoveMovie 用 filter 生成不含该电影的新数组，列表为空时显示提示文案。"),
    ("step-11-lift-state-up", "Step 11 · 状态提升",
     "评分状态从 Rating 提升到 App：Rating 变为纯展示组件，加减时调用 changeRating 通知 App 修改数据；Header 新增平均评分。"),
    ("step-12-toggle-watched", "Step 12 · 切换看过",
     "点击 WATCHED/NOT YET 徽章切换观看状态：用展开运算符复制电影对象并反转 watched 字段。"),
    ("step-13-use-state-final", "Step 13 · useState 最终版",
     "用函数组件 + useState Hook 重写整个应用，是 Part 2 的最终完成版，也是日常开发推荐写法。"),
]


def build_movie_night():
    base = "MovieNightPart2codeReza/checkpoints"
    demo_base = "../%s/" % base

    step_buttons, step_blocks = [], []
    for i, (step_id, step_title, step_desc) in enumerate(STEPS):
        active = step_id == "step-13-use-state-final"
        step_buttons.append(
            '<button class="step-btn{s}" type="button" data-step="{id}" '
            'data-title="{t}" data-desc="{d}">{t}</button>\n'.format(
                s=" active" if active else "",
                id=step_id, t=html.escape(step_title),
                d=html.escape(step_desc, quote=True),
            )
        )

        # 作用：每个步骤生成一组代码标签页——app.js / index.html / app.css
        # 解释：三个文件与 checkpoint 目录中的实际文件一一对应，
        #       默认激活第一个（app.js）；面板 id 带步骤名前缀防止冲突
        #       参考：下方 code_panel() 与 tab_button() 的生成逻辑
        files = [
            ("app.js", "app.js", "javascript"),
            ("index.html", "index.html", "xml"),
            ("app.css", "app.css", "css"),
        ]
        tabs, panels = [], []
        for j, (label, fname, lang) in enumerate(files):
            pid = "panel-%s-%s" % (step_id, fname.replace(".", "-"))
            tabs.append(tab_button("#" + pid, label, active=(j == 0)))
            panels.append(code_panel(pid, fname, read(base, step_id, fname), lang, active=(j == 0)))

        code = (
            '<div class="code-shell" data-tabs>\n'
            '  <div class="code-tabs">\n' + "".join(tabs) +
            '    <span class="spacer"></span>\n'
            '    <button class="copy-btn" type="button" data-copy="#panel-{sid}-app-js">复制代码</button>\n'
            "  </div>\n".format(sid=step_id) + "".join(panels) + "</div>\n"
        )

        step_blocks.append(
            '<div class="step-code{s}" data-step="{id}">\n{code}</div>\n'.format(
                s=" active" if active else "", id=step_id, code=code
            )
        )

    steps_html = (
        '<div id="steps-root" data-base="{base}">\n'
        '  <div class="steps-bar">\n{buttons}  </div>\n'
        '  <div class="step-desc"><strong id="step-title"></strong><br><span id="step-desc"></span></div>\n'
        "{blocks}</div>\n".format(
            base=html.escape(demo_base),
            buttons="".join(step_buttons),
            blocks="".join(step_blocks),
        )
    )

    notes = (
        '<div class="note"><h4>12 步递进教学</h4><p>从“普通变量为什么不能驱动界面”出发，'
        "逐步引入 state、事件、this 绑定、函数式更新、状态提升与 Hook。</p></div>"
        '<div class="note"><h4>最终版：useState</h4><p>Step 13 用函数组件 + useState 完成全部功能：'
        "删除电影、加减评分（0~5）、切换看过状态、平均评分统计。</p></div>"
        '<div class="note"><h4>状态提升思想</h4><p>多个组件需要共享的数据提升到最近公共父组件 App，'
        "子组件通过 props 收数据、通过回调汇报操作。</p></div>"
    )

    tags = ('<span class="tag">React 18</span><span class="tag">Class State</span>'
            '<span class="tag">useState Hook</span><span class="tag">状态提升</span>')

    page = project_page(
        kicker="Project 03 · Movie Night",
        title="Movie Night Part 2",
        desc="观影清单应用的 Part 2 状态管理教程，共 12 个递进步骤（Step 01 – 13）。"
             "选择下方步骤按钮，可实时运行对应版本的代码并查看带中文注释的源码；"
             "浏览器地址栏锚点（如 #step-06-bind-handlers）可直接分享某个步骤。",
        tags_html=tags,
        demo_src=demo_base + "step-13-use-state-final/index.html",
        demo_label=demo_base + "step-13-use-state-final/index.html",
        notes_html=notes,
        code_html=steps_html,
    )
    out = os.path.join(ROOT, "movie-night")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


# ------------------------------------------------------------------ main

def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(LANDING.replace("__GH__", GH_REPO))
    build_counter()
    build_planets()
    build_movie_night()
    print("site generated: index.html, counter/, planets/, movie-night/")


if __name__ == "__main__":
    main()
