# CSIS3380 Module 5 — Stateful React Components

> Full Stack Development With JavaScript · Douglas College · 2026
>
> Student: **Jinran Lin** (300395016)

---

## 📖 Overview

This repository contains the coursework for **Module 5: Stateful React Components**, including three React projects and a multi-page showcase website that presents them.

All project code carries **bilingual comments**: the instructor's original English comments are followed by Chinese translations, and the student-completed code sections are annotated in Chinese explaining what the code does.

**CSIS3380 Module 5：有状态 React 组件** 课程作业仓库，包含三个 React 项目以及一个展示这些项目的多页面网站。

所有项目代码均带有**中英双语注释**：老师原有英文注释后附中文翻译，学生补全的代码部分用中文注释说明其作用。

---

## 🗂 Repository Structure

```
├── index.html                      # Showcase website — home page (project overview)
├── counter/                        # Showcase page — Counter App
├── planets/                        # Showcase page — Planet Card App
├── movie-night/                    # Showcase page — Movie Night Part 2
├── assets/                         # Showcase website styles & scripts
│   ├── css/style.css
│   └── js/main.js
├── build_site.py                   # Script that regenerates the showcase pages
│
├── CounterAppWithReact-300395016-JinranLin/   # Project 1 — Counter App
├── PlanetCardApp-300395016-JinranLin/         # Project 2 — Planet Card App
├── MovieNightPart2codeReza/                   # Project 3 — Movie Night Part 2
│   ├── starter/                    # Part 1 finished app + Part 2 CSS
│   ├── checkpoints/                # 12 step-by-step checkpoints
│   └── make-checkpoints.py         # Script that regenerates the checkpoints
│
├── MovieNightPart2-images/         # Course material (tutorial copy with images)
└── *.pdf                           # Exercise lab instructions & tutorial PDFs
```

---

## 🚀 The Projects

### 1. Counter App With React — `CounterAppWithReact-300395016-JinranLin/`

A dual-counter app: **Counter A** and **Counter B** can each be incremented, decremented and reset, and the sum, difference, product and quotient of the two numbers are computed live (with a divide-by-zero notice).

双计数器应用：Counter A 与 Counter B 均可递增、递减、重置，页面底部实时计算并展示两数之和、差、积、商（除数为零时给出提示）。

- React 18 + in-browser Babel, `useState` state management, component composition

### 2. Planet Card App — `PlanetCardApp-300395016-JinranLin/`

A responsive card gallery of the eight planets with image, diameter, moon count and description. Individual planets can be removed and the list can be reset.

八大行星卡片画廊：响应式网格展示图片、直径、卫星数量与简介，支持删除单颗行星和一键重置。

- List rendering (`map`), conditional rendering, CSS Grid, `useState`

### 3. Movie Night Part 2 — `MovieNightPart2codeReza/`

A watchlist app taught in 12 progressive steps (Step 01–13), from "why an ordinary variable cannot drive the UI" through class-component `state`, event handling, `this` binding, functional `setState`, lifting state up, and finally the `useState` hook version.

观影清单应用的 Part 2 状态管理教程，共 12 个递进步骤（Step 01–13）：从普通变量、类组件 state、事件处理、this 绑定、函数式更新，到状态提升与 useState Hook。

| Step | Topic | 主题 |
| --- | --- | --- |
| 01 | Plain variable (experiment) | 普通变量实验 |
| 02 | Class component | 类组件 |
| 03 | Stateful component | 有状态组件 |
| 04 | Handling events | 处理事件 |
| 05 | Broken `this` (on purpose) | this 丢失（故意写错） |
| 06 | Arrow-function class fields | 箭头函数绑定 this |
| 07 | Update from previous state | 基于前状态更新 |
| 09 | Application state | 应用级状态 |
| 10 | Removing items | 删除条目 |
| 11 | Lifting state up | 状态提升 |
| 12 | Toggling watched | 切换看过 |
| 13 | `useState` final version | useState 最终版 |

---

## 🌐 The Showcase Website

The website at the repository root presents all three projects with live demos and fully commented source code.

仓库根目录的展示网站提供三个项目的实时演示与带中文注释的完整源码。

- **Live demos** embedded in browser-style frames (require internet access for the React CDN)
  **实时演示**：浏览器模拟框内嵌运行中的项目（需联网加载 React CDN）
- **Code viewer** with line numbers and syntax highlighting, switchable file tabs and a copy button
  **代码浏览器**：行号 + 语法高亮，可切换文件标签页并一键复制
- **Movie Night step switcher**: run and inspect any of the 12 steps, with URL hash deep-linking (e.g. `movie-night/index.html#step-06-bind-handlers`)
  **步骤切换器**：实时运行并查看任意步骤的代码，支持 URL 锚点深链分享
- **Responsive layout** for desktop and mobile
  **响应式布局**，适配桌面与移动端

### Run locally / 本地运行

```bash
# From the repository root
cd "Module 5 - Stateful React Components"
python3 -m http.server 8000
# Then open http://localhost:8000
```

> A local HTTP server is required for the embedded demos — opening `index.html` directly via `file://` will block the demo iframes in Chrome (the rest of the site still works).
>
> 演示 iframe 需要本地 HTTP 服务；直接用 `file://` 双击打开时 Chrome 会拦截演示（网站其他部分仍可正常浏览）。

### Deploy to GitHub Pages / 部署到 GitHub Pages

1. Push the repository to GitHub (already done).
2. In the repository, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Select branch `main` and folder `/ (root)`, then click **Save**.
5. After a few minutes the site is live at
   `https://<username>.github.io/<repository>/`

### Regenerate the showcase pages / 重新生成展示页面

After editing any project source code, re-run the build script and push again:

```bash
python3 build_site.py     # regenerates index.html, counter/, planets/, movie-night/
git add -A && git commit -m "update site" && git push
```

---

## 🛠 Tech Stack

- React 18 (UMD dev build) + Babel Standalone
- Vanilla JavaScript (ES5-compatible), CSS3
- highlight.js (CDN) for code highlighting
- Python 3 (build script only)

---

## 📝 Notes

- The `*.zip` archives and the nested `PracticeHub/` repository from the original workspace are excluded from version control (see `.gitignore`).
- 原始的 `*.zip` 压缩包与嵌套的 `PracticeHub/` 仓库未纳入版本管理（见 `.gitignore`）。
- Movie Night checkpoints are generated by `make-checkpoints.py`; edit the templates there and re-run the script instead of editing the checkpoint files directly.
- Movie Night 的 checkpoints 由 `make-checkpoints.py` 生成；如需修改请编辑脚本中的模板后重新运行，而非直接改动生成的文件。

---

## 👤 Author

**Jinran Lin** · Student ID 300395016 · CSIS 3380 — Full Stack Development With JavaScript

🔗 https://github.com/JohnnyLin707/CSIS3380-Module-5-Stateful-React-Components
