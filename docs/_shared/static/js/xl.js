/* XLeRobot docs: price calculator, scroll-in fade, full-screen buttons and the simulator's theme.
   Pages work without it. */
(function () {
  "use strict";

  function initPricing(root) {
    var symbols = JSON.parse(root.getAttribute("data-symbols") || "{}");
    var included = root.getAttribute("data-included") || "Included";
    var sum = root.querySelector(".xl-pricing__sum");

    function currency() {
      var checked = root.querySelector("input[data-currency]:checked");
      return checked ? checked.value : Object.keys(symbols)[0];
    }
    function prices(el) {
      try {
        return JSON.parse(el.getAttribute("data-prices") || "{}");
      } catch (e) {
        return {};
      }
    }
    function format(code, n) {
      return (symbols[code] || "") + Number(n).toLocaleString("en-US");
    }
    function update() {
      var code = currency();
      var base = root.querySelector(".xl-pricing__base [data-prices]");
      var total = base ? prices(base)[code] || 0 : 0;
      root.querySelectorAll("input[data-prices]:checked").forEach(function (input) {
        total += prices(input)[code] || 0;
      });
      root.querySelectorAll(".xl-price[data-prices]").forEach(function (el) {
        var value = prices(el)[code] || 0;
        if (el.getAttribute("data-mode") === "base") {
          el.textContent = "~" + format(code, value);
        } else {
          el.textContent = value ? "+" + format(code, value) : included;
        }
      });
      if (sum) sum.textContent = "~" + format(code, total);
    }
    root.addEventListener("change", update);
    update();
  }

  function initReveal() {
    if (!("IntersectionObserver" in window)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var targets = document.querySelectorAll(
      ".xl-home .bd-article > section > section > h2, .xl-lead, .xl-compose, .xl-flow, " +
        ".xl-pricing, .xl-timeline, .xl-cards, .xl-home .sd-row, .xl-film, .xl-stats"
    );
    var fold = window.innerHeight;
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px" }
    );
    targets.forEach(function (el) {
      // Only hide what the reader has not seen yet, so nothing flickers.
      if (el.getBoundingClientRect().top > fold) {
        el.classList.add("xl-reveal");
        observer.observe(el);
      }
    });
    window.addEventListener("beforeprint", function () {
      targets.forEach(function (el) {
        el.classList.add("is-visible");
      });
    });
  }

  /* <button data-xl-fullscreen="id" hidden>: shown where the browser can put that element full screen. */
  function initFullscreen() {
    if (!document.fullscreenEnabled) return;
    document.querySelectorAll("[data-xl-fullscreen]").forEach(function (button) {
      var target = document.getElementById(button.getAttribute("data-xl-fullscreen"));
      if (!target) return;
      button.hidden = false;
      button.addEventListener("click", function () {
        if (document.fullscreenElement) document.exitFullscreen();
        else target.requestFullscreen();
      });
    });
  }

  /* The framed simulator takes the site's light or dark theme: it asks for it when it starts
     ("xlerobot-sim:hello"), and is told again when the reader switches. */
  function initSimTheme() {
    var frame = document.querySelector(".xl-sim-stage iframe");
    if (!frame) return;
    var origin = new URL(frame.src, location.href).origin;
    function send() {
      var theme = document.documentElement.getAttribute("data-theme");
      if (frame.contentWindow) frame.contentWindow.postMessage({ type: "xlerobot-sim:theme", theme: theme }, origin);
    }
    window.addEventListener("message", function (event) {
      if (event.source === frame.contentWindow && event.data && event.data.type === "xlerobot-sim:hello") send();
    });
    new MutationObserver(send).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    frame.addEventListener("load", send);
  }

  function init() {
    document.querySelectorAll("[data-xl-pricing]").forEach(initPricing);
    initReveal();
    initFullscreen();
    initSimTheme();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
