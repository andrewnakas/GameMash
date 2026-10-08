#!/usr/bin/env bash
# Builds both web variants of one game and the auto-selecting loader into dist/<bin>/.
#   dist/<bin>/gpu/  WebGPU, high quality      dist/<bin>/gl/  WebGL2 fallback
# usage: scripts/build-web.sh [bin]   (default: gamemash; see src/bin/ for the others)
set -euo pipefail
cd "$(dirname "$0")/.."
bin="${1:-gamemash}"
export PATH="$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:$PATH"
export CARGO_BUILD_JOBS="${CARGO_BUILD_JOBS:-4}"
for v in gl gpu; do
  page=$(python3 scripts/web_html.py "$bin" "$v")
  trunk build --release --dist "dist/$bin/$v" --public-url ./ "$page"
  mv "dist/$bin/$v/$page" "dist/$bin/$v/index.html"
done
sed "s|<title>.*</title>|<title>$(grep -o '<title>[^<]*' "dist/$bin/gl/index.html" | cut -c8-)</title>|" web/loader.html > "dist/$bin/index.html"
echo "built dist/$bin/{gl,gpu,index.html}"
