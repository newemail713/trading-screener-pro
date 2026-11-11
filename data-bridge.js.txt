(function () {
  "use strict";
  const origFetch = window.fetch;
  window.fetch = async function (input, init) {
    const url = typeof input === "string" ? input : (input && input.url) || "";
    if (url.includes("/api/feed")) {
      const u = new URL(url, location.origin);
      const t = u.searchParams.get("t");
      const id = u.searchParams.get("id");
      let file = null;
      if (t === "scanner_data" && id === "latest") file = "data/scanner.json";
      else if (t === "market_snapshot" && id === "latest") file = "data/market.json";
      else if (t === "market_snapshot" && id === "prices") file = "data/prices.json";
      else if (t === "market_snapshot" && id === "breadth") file = "data/breadth.json";
      else if (t === "market_snapshot" && id === "news") file = "data/news.json";
      if (file) {
        try {
          const res = await origFetch(file + "?_t=" + Math.floor(Date.now() / 60000));
          if (res.ok) {
            const data = await res.json();
            return new Response(JSON.stringify([{ data: data }]), {
              status: 200,
              headers: { "Content-Type": "application/json" }
            });
          }
        } catch (e) {}
      }
      return new Response("[]", { status: 200, headers: { "Content-Type": "application/json" } });
    }
    return origFetch.apply(this, arguments);
  };
})();
