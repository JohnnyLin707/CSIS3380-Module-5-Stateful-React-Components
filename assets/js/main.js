/* ============================================================
   CSIS3380 Module 5 展示网站 —— 全站交互脚本
   功能：代码标签页切换 / 复制代码 / iframe 重载与打开 /
        Movie Night 步骤切换（支持 URL 锚点深链）/ 滚动显现动画
   ============================================================ */

(function () {
  "use strict";

  /* ---------- 代码文件标签页切换 ---------- */
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
  var stepsRoot = document.getElementById("steps-root");
  if (stepsRoot) {
    var stepButtons = stepsRoot.querySelectorAll(".step-btn");
    var stepBlocks = stepsRoot.querySelectorAll(".step-code");
    var stepTitle = document.getElementById("step-title");
    var stepDesc = document.getElementById("step-desc");
    var basePath = stepsRoot.getAttribute("data-base"); // ../MovieNightPart2codeReza/checkpoints/

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

    // 支持 URL 锚点深链，如 movie-night/index.html#step-06-bind-handlers
    var initial = location.hash ? location.hash.replace("#", "") : "";
    var exists = Array.prototype.some.call(stepButtons, function (b) {
      return b.getAttribute("data-step") === initial;
    });
    activateStep(exists ? initial : "step-13-use-state-final", false);

    // 页面已打开时 hash 变化（如浏览器前进/后退）也同步切换步骤
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
  document.querySelectorAll(".card").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- 滚动显现动画 ---------- */
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
