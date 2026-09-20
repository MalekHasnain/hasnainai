// hasnainai — language (Roman Urdu default) + theme (light default) + mobile drawer
(function () {
  var RU = "ru", EN = "en";

  // ---- helpers ----
  function getLang() {
    var v = null;
    try { v = localStorage.getItem("hai-lang"); } catch (e) {}
    return v === EN ? EN : RU; // default Roman Urdu
  }
  function setLang(l) {
    try { localStorage.setItem("hai-lang", l); } catch (e) {}
    var root = document.documentElement;
    root.classList.add("lang-fading");
    setTimeout(function () {
      applyLang();
      root.classList.remove("lang-fading");
    }, 180); // fade out -> swap -> fade in
  }
  function getTheme() {
    var v = null;
    try { v = localStorage.getItem("hai-theme"); } catch (e) {}
    return v === "dark" ? "dark" : "light"; // default light
  }
  function setTheme(t) {
    try { localStorage.setItem("hai-theme", t); } catch (e) {}
    document.documentElement.setAttribute("data-theme", t);
  }

  // ---- language switching ----
  function applyLang() {
    var lang = getLang();
    document.documentElement.setAttribute("data-lang", lang);
    // toggle buttons
    document.querySelectorAll("[data-lang-btn]").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-lang-btn") === lang);
    });
    // hide/show language blocks
    document.querySelectorAll(".ru, .en").forEach(function (el) {
      el.style.display = "";
      var isRu = el.classList.contains("ru");
      el.hidden = isRu ? lang !== RU : lang !== EN;
    });
  }

  // ---- init ----
  setTheme(getTheme());
  document.addEventListener("DOMContentLoaded", function () {
    applyLang();

    // language buttons
    document.querySelectorAll("[data-lang-btn]").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang-btn")); });
    });

    // theme buttons
    document.querySelectorAll("[data-theme-btn]").forEach(function (b) {
      b.addEventListener("click", function () { setTheme(b.getAttribute("data-theme-btn")); });
      b.classList.toggle("on", getTheme() === b.getAttribute("data-theme-btn"));
    });

    // mobile drawer
    var sidebar = document.querySelector(".sidebar");
    var backdrop = document.querySelector(".backdrop");
    var menuBtn = document.querySelector(".tb-menu");
    if (sidebar && backdrop && menuBtn) {
      menuBtn.addEventListener("click", function () {
        sidebar.classList.add("open");
        backdrop.classList.add("show");
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { sidebar.classList.remove("open"); backdrop.classList.remove("show"); }
      });
      backdrop.addEventListener("click", function () {
        sidebar.classList.remove("open");
        backdrop.classList.remove("show");
      });
      // close drawer when a nav link is tapped
      sidebar.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () {
          sidebar.classList.remove("open");
          backdrop.classList.remove("show");
        });
      });
    }
  });
})();
