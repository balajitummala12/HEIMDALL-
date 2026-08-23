# HEIMDALL

A premium, desktop-first web application UI with a live animated atomic background (glowing blue nucleus, orbiting orange electrons), five connected pages, and a working chat flow — all static HTML/CSS/JS, no build step, no framework.

## Run locally

From this folder:

```
python3 -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

(Opening `index.html` directly by double-clicking also works, since everything is plain static files with no server-side dependencies.)

## Deploy

This is a fully static site — drag the `heimdall` folder into Vercel, Netlify, GitHub Pages, or any static host. No config, build command, or environment variables needed.

## Structure

```
heimdall/
├── index.html          Home — hero, message input, capability grid
├── chat.html            Full desktop chat workspace
├── history.html          Searchable conversation log
├── capabilities.html     Six capability cards
├── settings.html          Appearance / opacity / energy saving / model / voice
├── css/
│   ├── style.css        Design system: tokens, nav, status indicator, background
│   └── pages.css         Page-specific layout
├── js/
│   ├── background.js    Canvas nucleus/electron/starfield animation
│   ├── main.js           Shared state: nav highlighting, settings, conversation store
│   ├── home.js            Home → Chat handoff
│   ├── chat.js             Chat page logic + simulated responses
│   ├── history.js          History page logic
│   └── settings.js          Settings page logic
└── assets/
    └── logo.png          Your uploaded HEIMDALL logo
```

## How the pieces connect

- **Home → Chat**: typing a message and hitting send stores it in `localStorage`, then navigates to `chat.html`, which picks it up as the first message and kicks off a simulated HEIMDALL reply (orange pulsing dot + "PROCESSING REQUEST...", no logo).
- **Conversations** are stored in `localStorage` under `heimdall_conversations` — shared by Home, Chat, and History, so anything you send is instantly visible in History and clickable back into Chat.
- **Settings** (opacity, energy saving, model, voice sync) persist in `localStorage` and take effect immediately — Energy Saving Mode pauses the animated background on every page.
- There is no real backend: the assistant replies in Chat are simulated for demonstration. Wire `respondTo()` in `js/chat.js` to your actual model/API when you're ready.

## Notes

- Fonts (Sora / Inter / JetBrains Mono) load from Google Fonts via CDN; everything else is self-contained.
- The background respects `prefers-reduced-motion` and the Energy Saving toggle.

## Mobile UI (`/mobile`)

A separate, mobile-first interface lives in `mobile/` — not a shrunk copy of desktop, but its own visual system built around an animated **HEIMDALL Energy Core** (concentric rotating rings, pulsing nucleus, scanning sweep). It reuses the same logo, `Heimdall` conversation/settings store, and localStorage data as desktop, so a chat started on one shows up in the other's History.

```
mobile/
├── index.html          Home — energy core centerpiece, input, quick chips
├── chat.html             Fixed header, scrolling messages, input locked above the tab bar
├── history.html           Searchable conversation list
├── capabilities.html      Capability list (stacked, thumb-friendly)
├── settings.html           Same settings, mobile layout
├── css/
│   ├── mobile-style.css  Tokens, energy core, header, bottom tab bar
│   └── mobile-pages.css  Page-specific layout
└── js/
    ├── mobile-main.js    Tab bar state, starfield, settings application
    ├── mobile-home.js     Home → Chat handoff
    ├── mobile-chat.js      Chat logic (same simulated reply engine as desktop — see note below)
    ├── mobile-history.js
    └── mobile-settings.js
```

Run/deploy the same way as desktop (static files, no build step) — just visit `/mobile/index.html` on a phone, or link to it from your existing site for mobile visitors.

**On "real API integration":** the existing desktop `chat.js` doesn't call a live backend yet — it simulates HEIMDALL's replies locally with canned responses and a delay. So mobile calls that same simulated engine (`generateReply()` in `mobile-chat.js`) rather than inventing a different placeholder, keeping desktop and mobile behavior identical. When you wire up a real API, update `generateReply()` there (and the equivalent in desktop's `chat.js`) to call it — everything else (storage, rendering, scroll behavior) stays as-is.

Layout notes: the chat header is `position: sticky`, the message list is the only scrolling element, and the input bar is `position: fixed` just above the bottom tab bar — so nothing shifts as messages are added, and the keyboard opening won't push the input off-screen. All fixed elements respect `env(safe-area-inset-bottom)` for notched phones.
