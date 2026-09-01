#!/usr/bin/env python3
"""Render site/og-image.png from site/og-image.svg.

Why a browser is involved: the card contains real text, and there is no font
rasteriser in the standard library. tools/make_favicon.py can draw its icon
from shapes alone; a headline in a system typeface cannot be done that way,
and pulling in Pillow or cairosvg would break the repository's no-dependency
rule (NFR-001).

So the renderer is the one that is already guaranteed present: a browser. This
script serves the SVG plus a small page that draws it to a 1200x630 canvas and
POSTs the PNG straight back to disk. The bytes never pass through a clipboard,
a terminal, or a copy-paste step, which is the part that actually goes wrong.

Usage:

    python tools/make_og_image.py

then open the URL it prints (it will say so). The script writes
site/og-image.png and exits on its own once the browser has posted the image.
Pass --port to pick a port, --timeout to change the 120s wait.

og:image will not accept SVG on most platforms, which is the only reason this
PNG needs to exist. Edit site/og-image.svg, re-run this, commit both.
"""
from __future__ import annotations

import argparse
import struct
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
OUT = SITE / "og-image.png"
WIDTH, HEIGHT = 1200, 630

RENDER_PAGE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Rendering og-image.png</title>
<style>
  body{font:16px system-ui,sans-serif;background:#1e1a17;color:#fbf3e4;
       margin:0;min-height:100vh;display:grid;place-items:center;gap:20px;
       padding:24px;text-align:center}
  img{max-width:min(96vw,900px);height:auto;box-shadow:0 8px 40px #0009}
  #msg{font-weight:700}
</style></head>
<body>
  <p id="msg">Rendering&hellip;</p>
  <img id="preview" alt="og:image preview">
  <script>
  (async function () {
    const msg = document.getElementById('msg');
    try {
      const svg = await (await fetch('og-image.svg?t=' + Date.now())).text();
      const url = URL.createObjectURL(new Blob([svg], {type: 'image/svg+xml'}));
      const img = new Image();
      await new Promise((ok, bad) => { img.onload = ok; img.onerror = bad; img.src = url; });

      const canvas = document.createElement('canvas');
      canvas.width = %(w)d; canvas.height = %(h)d;
      const ctx = canvas.getContext('2d');
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      // The card is opaque by design; painting the paper colour first means a
      // transparent gap can never show through as black in a chat client.
      ctx.fillStyle = '#fbf3e4';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(url);

      document.getElementById('preview').src = canvas.toDataURL('image/png');
      const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
      const res = await fetch('_save', {method: 'POST', body: blob});
      msg.textContent = res.ok
        ? 'Saved site/og-image.png (' + blob.size + ' bytes). You can close this tab.'
        : 'Save failed: ' + res.status;
    } catch (e) {
      msg.textContent = 'Render failed: ' + e;
    }
  })();
  </script>
</body>
</html>
""" % {"w": WIDTH, "h": HEIGHT}


class Handler(SimpleHTTPRequestHandler):
    saved = threading.Event()

    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/_render"):
            body = RENDER_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/_save":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            self.send_error(400, "not a PNG")
            return
        OUT.write_bytes(data)
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()
        Handler.saved.set()

    def log_message(self, *args):
        pass  # keep the console to the messages this script actually prints


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8124)
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    if not (SITE / "og-image.svg").exists():
        print("site/og-image.svg not found", file=sys.stderr)
        return 2

    server = ThreadingHTTPServer(("127.0.0.1", args.port),
                                partial(Handler, directory=str(SITE)))
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print(f"  open http://127.0.0.1:{args.port}/_render to render the card")
    ok = Handler.saved.wait(timeout=args.timeout)
    server.shutdown()

    if not ok:
        print(f"  timed out after {args.timeout}s — nothing written", file=sys.stderr)
        return 1

    raw = OUT.read_bytes()
    w, h = struct.unpack(">II", raw[16:24])
    print(f"  wrote og-image.png  {w}x{h}  {len(raw)} bytes")
    if (w, h) != (WIDTH, HEIGHT):
        print(f"  WARNING: expected {WIDTH}x{HEIGHT}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
