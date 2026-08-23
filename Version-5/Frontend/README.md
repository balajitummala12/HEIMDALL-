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
