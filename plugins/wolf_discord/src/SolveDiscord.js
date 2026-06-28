export const install = (attemptEndpoint) => (discordEndpoint) => () => {
  const originalFetch = window.fetch;

  window.fetch = async (...args) => {
    const response = await originalFetch(...args);

    try {
      const requestUrl = String(args[0]);

      if (requestUrl.includes(attemptEndpoint)) {
        const body = await response.clone().json();

        if (body?.data?.status === "correct") {
          showDiscordLink(originalFetch, discordEndpoint);
        }
      }
    } catch (_) {
      // Keep CTFd's normal submission flow working if the plugin fails.
    }

    return response;
  };
};

async function showDiscordLink(originalFetch, discordEndpoint) {
  try {
    const response = await originalFetch(discordEndpoint, {
      credentials: "same-origin",
    });

    if (!response.ok) {
      return;
    }

    const body = await response.json();

    if (!body.success || !body.url) {
      return;
    }

    const existing = document.querySelector("#wolf-discord-link");
    if (existing) {
      existing.remove();
    }

    const message = document.createElement("div");
    message.id = "wolf-discord-link";
    message.className = "alert alert-success mt-3";
    message.innerHTML = `
      <strong>Correct!</strong>
      Discord:
      <a href="${body.url}" target="_blank" rel="noopener noreferrer">
        ${body.url}
      </a>
    `;

    const target =
      document.querySelector(".modal-body") ||
      document.querySelector("#challenge-window .modal-body") ||
      document.body;

    target.appendChild(message);
  } catch (_) {
    // Do not interrupt CTFd's normal UI if the Discord endpoint is unavailable.
  }
}
