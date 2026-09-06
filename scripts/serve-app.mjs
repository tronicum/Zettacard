#!/usr/bin/env node
/**
 * DN-96: minimal static server for app/ (the Netlify publish root).
 *
 * Exists because Playwright's `webServer` needs a command that reliably binds
 * and stays in the foreground. `python3 -m http.server` was tried first and
 * silently failed to start under the test runner's environment, leaving the
 * runner waiting forever with no output. Node is already required to run the
 * tests, so this removes the Python dependency from the test path entirely.
 *
 *   node scripts/serve-app.mjs [port]        (default 8802)
 */
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'app');
const PORT = Number(process.argv[2] || process.env.PORT || 8802);
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon',
  '.webmanifest': 'application/manifest+json', '.woff2': 'font/woff2', '.txt': 'text/plain; charset=utf-8',
};

http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel === '/') rel = '/app.html';
  const file = path.join(ROOT, rel);
  // never serve outside app/
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    return res.end('not found');
  }
  res.writeHead(200, { 'content-type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`serving app/ on http://localhost:${PORT}/app.html`));
