/* ==========================================================================
   HEIMDALL — Live Atomic Background
   Asymmetrical orbit system + exact electron paths + animated nucleus
   ========================================================================== */

(function () {
  function initHeimdallBackground() {
    const mount = document.getElementById("heimdall-bg");
    if (!mount) return;

    /* =========================
       CREATE CANVAS
    ========================= */

    const canvas = document.createElement("canvas");
    canvas.className = "bg-canvas";
    mount.appendChild(canvas);

    const ambient = document.createElement("div");
    ambient.className = "bg-ambient";
    mount.insertBefore(ambient, canvas);

    const vignette = document.createElement("div");
    vignette.className = "bg-vignette";
    mount.appendChild(vignette);

    const ctx = canvas.getContext("2d");

    let width;
    let height;
    let dpr;

    let stars = [];
    let particles = [];
    let raf = null;
    let paused = false;

    const energySaving = () =>
      localStorage.getItem("heimdall_energy_saving") === "on";


    /* =========================
       ORBIT CONFIGURATION

       IMPORTANT:
       offsetX / offsetY makes
       rings slightly irregular
       instead of perfectly stacked.
    ========================= */

    const orbits = [
      {
        radiusX: 0.14,
        radiusY: 0.085,
        offsetX: -0.012,
        offsetY: -0.008,
        speed: 0.00058,
        phase: 0.2,
        tilt: -0.32,
        size: 4.2,
        color: "orange",
        trail: true
      },

      {
        radiusX: 0.19,
        radiusY: 0.12,
        offsetX: 0.016,
        offsetY: 0.010,
        speed: -0.00045,
        phase: 2.1,
        tilt: 0.28,
        size: 3.8,
        color: "orange",
        trail: true
      },

      {
        radiusX: 0.24,
        radiusY: 0.17,
        offsetX: -0.020,
        offsetY: 0.018,
        speed: 0.00034,
        phase: 4.0,
        tilt: -0.12,
        size: 3.5,
        color: "blue",
        trail: false
      },

      {
        radiusX: 0.30,
        radiusY: 0.105,
        offsetX: 0.028,
        offsetY: -0.022,
        speed: -0.00025,
        phase: 1.3,
        tilt: 0.48,
        size: 3.2,
        color: "orange",
        trail: true
      },

      {
        radiusX: 0.36,
        radiusY: 0.20,
        offsetX: -0.035,
        offsetY: 0.026,
        speed: 0.00018,
        phase: 3.7,
        tilt: -0.40,
        size: 3.0,
        color: "blue",
        trail: false
      }
    ];


    /* =========================
       RESIZE
    ========================= */

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);

      width = window.innerWidth;
      height = window.innerHeight;

      canvas.width = width * dpr;
      canvas.height = height * dpr;

      canvas.style.width = width + "px";
      canvas.style.height = height + "px";

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);


      /* ---------- STARS ---------- */

      const starCount = Math.floor((width * height) / 9000);

      stars = new Array(starCount).fill(0).map(() => ({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 1.15 + 0.2,
        baseAlpha: Math.random() * 0.5 + 0.15,
        twinkleSpeed: Math.random() * 0.0016 + 0.0004,
        twinklePhase: Math.random() * Math.PI * 2,
        drift: (Math.random() - 0.5) * 0.008
      }));


      /* ---------- SPACE PARTICLES ---------- */

      const dustCount = Math.floor((width * height) / 60000);

      particles = new Array(dustCount).fill(0).map(() => ({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 1.6 + 0.6,
        hue: Math.random() > 0.5 ? "cyan" : "orange",
        alpha: Math.random() * 0.18 + 0.04,
        vy: -(Math.random() * 0.06 + 0.02),
        vx: (Math.random() - 0.5) * 0.04
      }));
    }


    /* =========================
       DRAW STARS
    ========================= */

    function drawStars(t) {
      for (const s of stars) {
        s.x += s.drift;

        if (s.x < 0) s.x = width;
        if (s.x > width) s.x = 0;

        const twinkle =
          Math.sin(t * s.twinkleSpeed + s.twinklePhase) * 0.5 + 0.5;

        const alpha =
          s.baseAlpha * (0.5 + twinkle * 0.5);

        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);

        ctx.fillStyle =
          `rgba(210, 230, 255, ${alpha})`;

        ctx.fill();
      }
    }


    /* =========================
       DRAW SPACE PARTICLES
    ========================= */

    function drawParticles() {
      for (const p of particles) {
        p.y += p.vy;
        p.x += p.vx;

        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }

        const color =
          p.hue === "cyan"
            ? "79,216,255"
            : "255,154,77";

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);

        ctx.fillStyle =
          `rgba(${color}, ${p.alpha})`;

        ctx.fill();
      }
    }


    /* =========================
       GET ORBIT CENTER

       Every orbit has its own
       slightly shifted center.
    ========================= */

    function getOrbitCenter(cx, cy, orbit) {
      const base = Math.min(width, height);

      return {
        x: cx + orbit.offsetX * base,
        y: cy + orbit.offsetY * base
      };
    }


    /* =========================
       GET EXACT POINT ON ORBIT

       THIS FUNCTION IS USED FOR
       BOTH THE LINE AND ELECTRON.

       So electrons will always
       move EXACTLY on the ring.
    ========================= */

    function getOrbitPoint(cx, cy, orbit, angle) {
      const base = Math.min(width, height) * 2.1;

      const rx = orbit.radiusX * base;
      const ry = orbit.radiusY * base;

      const center = getOrbitCenter(cx, cy, orbit);

      const localX = Math.cos(angle) * rx;
      const localY = Math.sin(angle) * ry;

      const x =
        center.x +
        localX * Math.cos(orbit.tilt) -
        localY * Math.sin(orbit.tilt);

      const y =
        center.y +
        localX * Math.sin(orbit.tilt) +
        localY * Math.cos(orbit.tilt);

      return { x, y };
    }


    /* =========================
       DRAW ORBIT PATH
    ========================= */

    function drawOrbitPath(cx, cy, orbit) {
      const base = Math.min(width, height) * 2.1;

      const rx = orbit.radiusX * base;
      const ry = orbit.radiusY * base;

      const center = getOrbitCenter(cx, cy, orbit);

      ctx.save();

      ctx.translate(center.x, center.y);
      ctx.rotate(orbit.tilt);

      ctx.beginPath();

      ctx.ellipse(
        0,
        0,
        rx,
        ry,
        0,
        0,
        Math.PI * 2
      );

      /* subtle blue orbit */

      ctx.strokeStyle =
        "rgba(100, 185, 255, 0.10)";

      ctx.lineWidth = 1;

      ctx.stroke();

      /* faint outer glow */

      ctx.strokeStyle =
        "rgba(79, 216, 255, 0.025)";

      ctx.lineWidth = 3;

      ctx.stroke();

      ctx.restore();
    }


    /* =========================
       DRAW ENERGY WAVES

       Expanding waves produced
       continuously by nucleus.
    ========================= */

    function drawEnergyWaves(cx, cy, t, nucleusR) {
      const cycle = 3800;

      for (let i = 0; i < 3; i++) {
        const progress =
          ((t + i * (cycle / 3)) % cycle) / cycle;

        const radius =
          nucleusR * 1.2 +
          progress * Math.min(width, height) * 0.16;

        const alpha =
          (1 - progress) * 0.14;

        ctx.beginPath();

        ctx.arc(
          cx,
          cy,
          radius,
          0,
          Math.PI * 2
        );

        ctx.strokeStyle =
          `rgba(79, 216, 255, ${alpha})`;

        ctx.lineWidth =
          1.4 - progress * 0.8;

        ctx.stroke();
      }
    }


    /* =========================
       DRAW INTERNAL NUCLEUS
       PARTICLES

       These visibly revolve
       INSIDE the nucleus.
    ========================= */

    function drawNucleusParticles(cx, cy, t, r) {
      const internalParticles = [
        {
          radius: 0.34,
          speed: 0.0018,
          phase: 0,
          size: 3.4,
          color: "255,255,255"
        },

        {
          radius: 0.50,
          speed: -0.00125,
          phase: 1.8,
          size: 2.8,
          color: "120,225,255"
        },

        {
          radius: 0.67,
          speed: 0.00092,
          phase: 3.7,
          size: 2.4,
          color: "79,216,255"
        },

        {
          radius: 0.42,
          speed: -0.00155,
          phase: 5.0,
          size: 2.2,
          color: "180,240,255"
        }
      ];

      for (const p of internalParticles) {
        const angle =
          t * p.speed + p.phase;

        const orbitR =
          r * p.radius;

        const x =
          cx + Math.cos(angle) * orbitR;

        const y =
          cy + Math.sin(angle) * orbitR * 0.65;


        /* small internal orbit trail */

        ctx.beginPath();

        ctx.ellipse(
          cx,
          cy,
          orbitR,
          orbitR * 0.65,
          0,
          0,
          Math.PI * 2
        );

        ctx.strokeStyle =
          "rgba(180, 235, 255, 0.055)";

        ctx.lineWidth = 0.7;

        ctx.stroke();


        /* particle glow */

        const glow =
          ctx.createRadialGradient(
            x,
            y,
            0,
            x,
            y,
            p.size * 4
          );

        glow.addColorStop(
          0,
          `rgba(${p.color}, 0.85)`
        );

        glow.addColorStop(
          1,
          `rgba(${p.color}, 0)`
        );

        ctx.beginPath();

        ctx.arc(
          x,
          y,
          p.size * 4,
          0,
          Math.PI * 2
        );

        ctx.fillStyle = glow;

        ctx.fill();


        /* actual particle */

        ctx.beginPath();

        ctx.arc(
          x,
          y,
          p.size,
          0,
          Math.PI * 2
        );

        ctx.fillStyle =
          `rgb(${p.color})`;

        ctx.fill();
      }
    }


    /* =========================
       DRAW NUCLEUS
    ========================= */

    function drawNucleus(cx, cy, t) {
      const pulse =
        Math.sin(t * 0.0012) * 0.5 + 0.5;

      /* BIGGER NUCLEUS */

      const baseR =
        Math.min(width, height) * 0.072;

      const r =
        baseR * (0.96 + pulse * 0.06);


      /* ---------- ENERGY WAVES ---------- */

      drawEnergyWaves(cx, cy, t, r);


      /* ---------- OUTER MASSIVE GLOW ---------- */

      const outerGlow =
        ctx.createRadialGradient(
          cx,
          cy,
          0,
          cx,
          cy,
          r * 6.5
        );

      outerGlow.addColorStop(
        0,
        "rgba(110, 225, 255, 0.24)"
      );

      outerGlow.addColorStop(
        0.22,
        "rgba(60, 160, 255, 0.15)"
      );

      outerGlow.addColorStop(
        0.55,
        "rgba(40, 100, 230, 0.055)"
      );

      outerGlow.addColorStop(
        1,
        "rgba(20, 60, 150, 0)"
      );

      ctx.beginPath();

      ctx.arc(
        cx,
        cy,
        r * 6.5,
        0,
        Math.PI * 2
      );

      ctx.fillStyle = outerGlow;

      ctx.fill();


      /* ---------- ELECTRIC ENERGY RING ---------- */

      ctx.save();

      ctx.translate(cx, cy);

      ctx.rotate(t * 0.00008);

      ctx.beginPath();

      for (let i = 0; i <= 90; i++) {
        const angle =
          (i / 90) * Math.PI * 2;

        const distortion =
          Math.sin(angle * 6 + t * 0.002) * r * 0.09 +
          Math.sin(angle * 11 - t * 0.0015) * r * 0.05;

        const rr =
          r * 1.18 + distortion;

        const x =
          Math.cos(angle) * rr;

        const y =
          Math.sin(angle) * rr;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();

      ctx.strokeStyle =
        "rgba(70, 190, 255, 0.38)";

      ctx.lineWidth = 1.2;

      ctx.stroke();

      ctx.restore();


      /* ---------- MAIN NUCLEUS ---------- */

      const core =
        ctx.createRadialGradient(
          cx - r * 0.28,
          cy - r * 0.28,
          r * 0.04,
          cx,
          cy,
          r
        );

      core.addColorStop(
        0,
        "#ffffff"
      );

      core.addColorStop(
        0.16,
        "#d9f8ff"
      );

      core.addColorStop(
        0.42,
        "#69d8ff"
      );

      core.addColorStop(
        0.72,
        "#2586d2"
      );

      core.addColorStop(
        1,
        "#102c5a"
      );

      ctx.beginPath();

      ctx.arc(
        cx,
        cy,
        r,
        0,
        Math.PI * 2
      );

      ctx.fillStyle = core;

      ctx.fill();


      /* ---------- INNER ROTATING PARTICLES ---------- */

      ctx.save();

      ctx.beginPath();

      ctx.arc(
        cx,
        cy,
        r * 0.98,
        0,
        Math.PI * 2
      );

      ctx.clip();

      drawNucleusParticles(
        cx,
        cy,
        t,
        r
      );

      ctx.restore();


      /* ---------- CENTER CORE ---------- */

      const centerPulse =
        Math.sin(t * 0.002) * 0.5 + 0.5;

      const centerR =
        r * (0.20 + centerPulse * 0.035);

      const centerGlow =
        ctx.createRadialGradient(
          cx,
          cy,
          0,
          cx,
          cy,
          centerR * 3
        );

      centerGlow.addColorStop(
        0,
        "rgba(255,255,255,0.95)"
      );

      centerGlow.addColorStop(
        0.3,
        "rgba(150,235,255,0.8)"
      );

      centerGlow.addColorStop(
        1,
        "rgba(80,180,255,0)"
      );

      ctx.beginPath();

      ctx.arc(
        cx,
        cy,
        centerR * 3,
        0,
        Math.PI * 2
      );

      ctx.fillStyle = centerGlow;

      ctx.fill();

      ctx.beginPath();

      ctx.arc(
        cx,
        cy,
        centerR,
        0,
        Math.PI * 2
      );

      ctx.fillStyle =
        "rgba(225, 250, 255, 0.92)";

      ctx.fill();
    }


    /* =========================
       DRAW ELECTRON
    ========================= */

    function drawElectron(cx, cy, orbit, t) {
      const angle =
        t * orbit.speed + orbit.phase;


      /* EXACT POSITION ON ORBIT */

      const position =
        getOrbitPoint(
          cx,
          cy,
          orbit,
          angle
        );

      const x = position.x;
      const y = position.y;


      /* ---------- TRAIL ---------- */

      if (orbit.trail) {
        const trailLength = 12;

        for (
          let i = 1;
          i <= trailLength;
          i++
        ) {
          const trailAngle =
            angle -
            i *
              0.055 *
              Math.sign(
                orbit.speed || 1
              );

          const trailPos =
            getOrbitPoint(
              cx,
              cy,
              orbit,
              trailAngle
            );

          const alpha =
            (1 - i / trailLength) *
            0.16;

          ctx.beginPath();

          ctx.arc(
            trailPos.x,
            trailPos.y,
            orbit.size *
              (1 -
                (i / trailLength) *
                  0.65),
            0,
            Math.PI * 2
          );

          const trailColor =
            orbit.color === "blue"
              ? "79,216,255"
              : "255,154,77";

          ctx.fillStyle =
            `rgba(${trailColor}, ${alpha})`;

          ctx.fill();
        }
      }


      /* ---------- ELECTRON GLOW ---------- */

      const electronColor =
        orbit.color === "blue"
          ? "79,216,255"
          : "255,154,77";

      const glow =
        ctx.createRadialGradient(
          x,
          y,
          0,
          x,
          y,
          orbit.size * 5.5
        );

      glow.addColorStop(
        0,
        `rgba(${electronColor}, 0.72)`
      );

      glow.addColorStop(
        0.35,
        `rgba(${electronColor}, 0.28)`
      );

      glow.addColorStop(
        1,
        `rgba(${electronColor}, 0)`
      );

      ctx.beginPath();

      ctx.arc(
        x,
        y,
        orbit.size * 5.5,
        0,
        Math.PI * 2
      );

      ctx.fillStyle = glow;

      ctx.fill();


      /* ---------- ACTUAL ELECTRON ---------- */

      ctx.beginPath();

      ctx.arc(
        x,
        y,
        orbit.size,
        0,
        Math.PI * 2
      );

      ctx.fillStyle =
        orbit.color === "blue"
          ? "#d9f8ff"
          : "#ffe0c2";

      ctx.fill();
    }


    /* =========================
       ANIMATION FRAME
    ========================= */

    function frame(t) {
      if (paused) return;

      ctx.clearRect(
        0,
        0,
        width,
        height
      );


      /* Main atomic center */

      const cx =
        width * 0.50;

      const cy =
        height * 0.46;


      drawStars(t);

      drawParticles();


      /* DRAW RINGS */

      for (const orbit of orbits) {
        drawOrbitPath(
          cx,
          cy,
          orbit
        );
      }


      /* DRAW NUCLEUS */

      drawNucleus(
        cx,
        cy,
        t
      );


      /* DRAW ELECTRONS */

      for (const orbit of orbits) {
        drawElectron(
          cx,
          cy,
          orbit,
          t
        );
      }


      raf =
        requestAnimationFrame(frame);
    }


    /* =========================
       START / STOP
    ========================= */

    function start() {
      if (raf) {
        cancelAnimationFrame(raf);
      }

      paused = false;

      raf =
        requestAnimationFrame(frame);
    }


    function stop() {
      paused = true;

      if (raf) {
        cancelAnimationFrame(raf);
      }

      ctx.clearRect(
        0,
        0,
        width,
        height
      );
    }


    /* =========================
       INITIALIZE
    ========================= */

    resize();

    window.addEventListener(
      "resize",
      resize
    );


    const prefersReduced =
      window.matchMedia(
        "(prefers-reduced-motion: reduce)"
      ).matches;


    function applyEnergyMode() {
      if (
        energySaving() ||
        prefersReduced
      ) {
        stop();

        canvas.style.opacity = "0";
      } else {
        canvas.style.opacity = "1";

        start();
      }
    }


    applyEnergyMode();


    window.addEventListener(
      "heimdall:settings-changed",
      applyEnergyMode
    );


    document.addEventListener(
      "visibilitychange",
      () => {
        if (document.hidden) {
          if (raf) {
            cancelAnimationFrame(raf);
          }
        } else if (
          !energySaving() &&
          !prefersReduced
        ) {
          start();
        }
      }
    );
  }


  /* =========================
     START BACKGROUND
  ========================= */

  if (
    document.readyState ===
    "loading"
  ) {
    document.addEventListener(
      "DOMContentLoaded",
      initHeimdallBackground
    );
  } else {
    initHeimdallBackground();
  }
})();