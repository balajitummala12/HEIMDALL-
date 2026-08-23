(function () {
  const isMobile = window.innerWidth <= 768;

  if (!isMobile) return;

  const path = window.location.pathname;

  // Don't redirect if already inside mobile pages
  if (path.startsWith("/mobile")) return;

  const routes = {
    "/": "/mobile/",
    "/index.html": "/mobile/",
    "/chat": "/mobile/chat",
    "/chat.html": "/mobile/chat",
    "/history": "/mobile/history",
    "/history.html": "/mobile/history",
    "/capabilities": "/mobile/capabilities",
    "/capabilities.html": "/mobile/capabilities",
    "/settings": "/mobile/settings",
    "/settings.html": "/mobile/settings"
  };

  const destination = routes[path];

  if (destination) {
    window.location.replace(destination);
  }
})();