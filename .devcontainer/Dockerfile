FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Python 3.12 + venv + pip
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.12 python3.12-venv python3-pip \
        ca-certificates curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

# uv (fast Python package manager) — installed system-wide for the vscode user
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# Node (needed to install Claude Code CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Playwright system dependencies for headless Chromium.
# The python `playwright` package + `playwright install --with-deps chromium`
# is run at container-create time via postCreateCommand once the project's
# venv exists. We pre-install the OS-level deps here so that step is fast.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 \
        libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
        libasound2t64 libxshmfence1 libcups2t64 libatspi2.0-0 \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

# Container-only Claude Code settings — broader permissions that NEVER touch
# the host's ~/.claude/settings.json. The container is sandboxed, so allowing
# any Bash command and any directory is acceptable here even though it would
# not be on the host.
USER vscode
RUN mkdir -p /home/vscode/.claude && cat > /home/vscode/.claude/settings.json <<'JSON'
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(/**)", "Write(/**)", "Edit(/**)",
      "Read(/home/vscode/.claude/plugins/**)"
    ],
    "additionalDirectories": ["/"]
  },
  "extraKnownMarketplaces": {
    "agile-dev": {
      "source": { "source": "github", "repo": "mateuszgruszczynski/agile-dev-pipeline" }
    }
  },
  "enabledPlugins": {
    "agile-dev@agile-dev": true
  }
}
JSON
USER root
