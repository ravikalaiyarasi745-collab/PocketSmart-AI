async function api(url, options = {}) {
  const opts = {...options, credentials: "same-origin"};
  if (opts.body && typeof opts.body !== "string" && !(opts.body instanceof FormData)) {
    opts.headers = {...opts.headers, "Content-Type": "application/json"};
    opts.body = JSON.stringify(opts.body);
  }
  const response = await fetch(url, opts);
  let data = {};
  try { data = await response.json(); } catch {}
  return {ok: response.ok, status: response.status, data};
}

function showMessage(message, error=false) {
  const el = document.getElementById("form-message");
  if (!el) return;
  el.textContent = message;
  el.className = "form-message " + (error ? "error" : "success");
}

function setLoading(active) {
  const el = document.getElementById("loading");
  if (el) el.classList.toggle("hidden", !active);
}

async function logout() {
  await api("/api/auth/logout", {method:"POST"});
  location.href="/";
}