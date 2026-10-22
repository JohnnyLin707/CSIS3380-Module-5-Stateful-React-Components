/* ============================================================
   CSIS3380 Module 5 展示网站 —— 全站交互脚本
   作用：实现整站的交互功能——代码标签页切换、复制代码、
        iframe 重载与新窗口打开、Movie Night 步骤切换
        （支持 URL 锚点深链）、主页卡片光斑、滚动显现动画
   解释：用 IIFE（立即执行函数）包裹全部代码，避免变量泄漏到全局；
        每个功能块独立判断目标元素是否存在，因此同一个脚本
        可以安全地同时服务于主页和三个子页面
   参考：与本文件配合的 HTML 结构由 build_site.py 生成
   ============================================================ */

(function () {
  "use strict";

  /* ---------- 代码文件标签页切换 ---------- */
  /* 作用：点击文件名标签页时，切换显示对应的代码面板 */
  /* 解释：先移除所有标签和面板的 active 类，再给当前点击的标签
          和它对应的面板加上 active 类（CSS 控制显隐）；
          用 data-target 属性关联按钮与面板，不在 JS 里写死 id */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var tabs = group.querySelectorAll(".code-tab");
    var panels = group.querySelectorAll(".code-panel");
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var target = tab.getAttribute("data-target");
        tabs.forEach(function (t) { t.classList.remove("active"); });
        panels.forEach(function (p) { p.classList.remove("active"); });
        tab.classList.add("active");
        var panel = group.querySelector(target);
        if (panel) { panel.classList.add("active"); }
      });
    });
  });

  /* ---------- 复制代码按钮 ---------- */
  /* 作用：把当前激活代码面板的文本复制到剪贴板，并显示"已复制"反馈 */
  /* 解释：优先用现代 navigator.clipboard API（需要 HTTPS 或 localhost），
          失败时降级到传统的 textarea + execCommand 方案，保证兼容 */
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.querySelector(btn.getAttribute("data-copy"));
      if (!panel) { return; }
      var code = panel.querySelector("code");
      var text = code ? code.textContent : "";

      function done() {
        var old = btn.textContent;
        btn.textContent = "已复制 ✓";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.textContent = old;
          btn.classList.remove("copied");
        }, 1600);
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () { fallbackCopy(text); done(); });
      } else {
        fallbackCopy(text);
        done();
      }
    });
  });

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* 忽略 */ }
    document.body.removeChild(ta);
  }

  /* ---------- 演示 iframe：重载 / 新窗口打开 ---------- */
  /* 作用：给演示框标题栏的"重载"和"新窗口"两个按钮绑定行为 */
  /* 解释：重载通过重新赋值 iframe.src 实现（等价于刷新演示页面）；
          新窗口用 window.open 打开当前 src，方便放大仔细看 */
  var demoFrame = document.getElementById("demo-frame");
  var demoUrl = demoFrame ? demoFrame.getAttribute("src") : "";

  var reloadBtn = document.getElementById("btn-reload");
  if (reloadBtn && demoFrame) {
    reloadBtn.addEventListener("click", function () {
      demoFrame.src = demoFrame.src;
    });
  }

  var openBtn = document.getElementById("btn-open");
  if (openBtn) {
    openBtn.addEventListener("click", function () {
      var url = demoFrame ? demoFrame.getAttribute("src") : demoUrl;
      if (url) { window.open(url, "_blank", "noopener"); }
    });
  }

  /* ---------- Movie Night：步骤切换 ---------- */
  /* 作用：Movie Night 页面的核心交互——切换 12 个教学步骤 */
  /* 解释：切换一个步骤要同步三样东西：激活对应按钮、显示对应代码面板、
          把演示 iframe 指向该步骤的 index.html；
          data-base 属性由 build_site.py 写入，值为 checkpoints 目录的相对路径 */
  var stepsRoot = document.getElementById("steps-root");
  if (stepsRoot) {
    var stepButtons = stepsRoot.querySelectorAll(".step-btn");
    var stepBlocks = stepsRoot.querySelectorAll(".step-code");
    var stepTitle = document.getElementById("step-title");
    var stepDesc = document.getElementById("step-desc");
    var basePath = stepsRoot.getAttribute("data-base");

    function activateStep(stepId, updateHash) {
      stepButtons.forEach(function (b) {
        b.classList.toggle("active", b.getAttribute("data-step") === stepId);
      });
      stepBlocks.forEach(function (block) {
        block.classList.toggle("active", block.getAttribute("data-step") === stepId);
      });

      var activeBtn = stepsRoot.querySelector('.step-btn[data-step="' + stepId + '"]');
      if (activeBtn && stepTitle && stepDesc) {
        stepTitle.textContent = activeBtn.getAttribute("data-title");
        stepDesc.innerHTML = activeBtn.getAttribute("data-desc");
      }

      if (demoFrame && basePath) {
        demoFrame.src = basePath + stepId + "/index.html";
      }
      if (updateHash) {
        history.replaceState(null, "", "#" + stepId);
      }
    }

    stepButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activateStep(btn.getAttribute("data-step"), true);
      });
    });

    // 作用：读取 URL 锚点初始化步骤，支持深链（如 #step-06-bind-handlers）
    // 解释：从 location.hash 取出步骤 id，若与某个按钮匹配就激活它，
    //       否则回退到最终版 step-13；这样分享链接能直达某个步骤
    //       参考：movie-night/index.html 中步骤按钮的 data-step 属性
    var initial = location.hash ? location.hash.replace("#", "") : "";
    var exists = Array.prototype.some.call(stepButtons, function (b) {
      return b.getAttribute("data-step") === initial;
    });
    activateStep(exists ? initial : "step-13-use-state-final", false);

    // 作用：页面已打开时 hash 变化（浏览器前进/后退）也同步切换步骤
    // 解释：hashchange 事件在仅锚点变化时触发，此时页面不会重载，
    //       需要手动同步 UI 状态；updateHash 传 false 避免循环更新地址栏
    window.addEventListener("hashchange", function () {
      var id = location.hash ? location.hash.replace("#", "") : "";
      var ok = Array.prototype.some.call(stepButtons, function (b) {
        return b.getAttribute("data-step") === id;
      });
      if (ok && id !== document.querySelector(".step-code.active").getAttribute("data-step")) {
        activateStep(id, false);
      }
    });
  }

  /* ---------- 主页卡片：鼠标位置驱动光斑 ---------- */
  /* 作用：监听主页卡片内鼠标移动，把坐标写进 CSS 变量 --mx/--my */
  /* 解释：光斑位置由 CSS 的 radial-gradient at var(--mx) var(--my) 读取，
        JS 只算坐标不做样式，"逻辑与表现分离"；getBoundingClientRect
        把视口坐标转换成相对卡片的坐标 */
  document.querySelectorAll(".card").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- 滚动显现动画 ---------- */
  /* 作用：给 .reveal 元素加进入视口的淡入上移动画 */
  /* 解释：IntersectionObserver 观察元素是否进入视口，进入后加 .visible 类
        并取消观察（只播一次）；老浏览器不支持时直接显示全部元素兜底 */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("visible"); });
  }
})();
