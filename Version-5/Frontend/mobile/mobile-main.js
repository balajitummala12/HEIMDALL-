/* ==========================================================================
   HEIMDALL MOBILE — Shared System
   Stable navigation + animated live background
   ========================================================================== */

(function () {

  // =========================================================
  // TAB BAR
  // =========================================================

  function initTabbar() {

    const page =
      document.body.getAttribute("data-page");

    document.querySelectorAll(".mx-tab").forEach((tab) => {

      tab.classList.toggle(
        "active",
        tab.getAttribute("data-tab") === page
      );

    });

  }


  // =========================================================
  // LIVE STAR FIELD
  // =========================================================

  function createStars() {

    const layer =
      document.querySelector(".mx-stars");

    if (!layer) return;

    // Prevent duplicate stars
    layer.innerHTML = "";

    const count = Math.min(
      55,
      Math.max(
        32,
        Math.floor(
          (window.innerWidth * window.innerHeight) / 9000
        )
      )
    );


    for (let i = 0; i < count; i++) {

      const star =
        document.createElement("span");

      star.className =
        "mx-star";


      const size =
        Math.random() > 0.88
          ? Math.random() * 2 + 2
          : Math.random() * 1.5 + 1;


      star.style.width =
        size + "px";

      star.style.height =
        size + "px";


      star.style.left =
        Math.random() * 100 + "%";

      star.style.top =
        Math.random() * 100 + "%";


      star.style.opacity =
        (
          Math.random() * 0.65 + 0.15
        ).toFixed(2);


      const duration =
        2.5 + Math.random() * 4;


      star.style.animationDuration =
        duration + "s";

      star.style.animationDelay =
        (-Math.random() * duration) + "s";


      layer.appendChild(star);

    }

  }


  // =========================================================
  // STABLE LIVE BACKGROUND
  // =========================================================

  function initBackground() {

    const bg =
      document.querySelector(".mx-bg");

    if (!bg) return;


    // Set initial position
    bg.style.setProperty(
      "--mx-x",
      "50%"
    );

    bg.style.setProperty(
      "--mx-y",
      "50%"
    );


    // Lightweight background response
    // No infinite requestAnimationFrame loop
    window.addEventListener(
      "touchmove",
      (event) => {

        if (!event.touches.length) return;


        const touch =
          event.touches[0];


        const x =
          (
            touch.clientX /
            window.innerWidth
          ) * 100;


        const y =
          (
            touch.clientY /
            window.innerHeight
          ) * 100;


        bg.style.setProperty(
          "--mx-x",
          x.toFixed(1) + "%"
        );

        bg.style.setProperty(
          "--mx-y",
          y.toFixed(1) + "%"
        );

      },
      {
        passive: true
      }
    );

  }


  // =========================================================
  // MOBILE SETTINGS
  // =========================================================

  function applyMobileSettings() {

    if (
      typeof Heimdall === "undefined"
    ) {
      return;
    }


    const settings =
      Heimdall.getSettings();


    document.body.classList.toggle(
      "energy-saving",
      !!settings.energySaving
    );


    document.body.setAttribute(
      "data-theme",
      settings.appearance || "deep-space"
    );


    const shell =
      document.querySelector(".mx-app");


    if (shell) {

      shell.style.opacity =
        String(
          0.75 +
          (settings.opacity / 100) * 0.25
        );

    }

  }


  // =========================================================
  // INITIALIZE
  // =========================================================

  function init() {

    initTabbar();

    createStars();

    initBackground();

    applyMobileSettings();


    window.addEventListener(
      "heimdall:settings-changed",
      applyMobileSettings
    );

  }


  if (
    document.readyState === "loading"
  ) {

    document.addEventListener(
      "DOMContentLoaded",
      init
    );

  } else {

    init();

  }

})();