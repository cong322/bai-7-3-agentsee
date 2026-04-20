const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const projectDir = __dirname;
const htmlPath = path.join(projectDir, "index.html");
const serverPath = path.join(projectDir, "server.js");
const startPath = path.join(projectDir, "start.ps1");

function read(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

test("index.html loads Leaflet and has a map container", () => {
  const html = read(htmlPath);

  assert.match(html, /leaflet\.css/i);
  assert.match(html, /leaflet\.js/i);
  assert.match(html, /id="map"/i);
});

test("index.html hardcodes an inland US location and uses the Vietnam flag icon at 150x150", () => {
  const html = read(htmlPath);

  assert.match(html, /const\s+markerLat\s*=\s*32\.78306\s*;/);
  assert.match(html, /const\s+markerLng\s*=\s*-96\.80667\s*;/);
  assert.match(html, /iconUrl:\s*"flag-vn-150\.png"/);
  assert.match(html, /iconSize:\s*\[\s*150\s*,\s*150\s*\]/);
});

test("index.html auto focuses the map on the marker", () => {
  const html = read(htmlPath);

  assert.match(html, /L\.map\("map"\)/);
  assert.match(html, /setView\(\s*\[\s*markerLat\s*,\s*markerLng\s*\]\s*,\s*14\s*\)/);
  assert.match(html, /marker\.addTo\(map\)/);
});

test("server and start script exist for local verification", () => {
  const server = read(serverPath);
  const startScript = read(startPath);

  assert.match(server, /createServer/);
  assert.match(server, /127\.0\.0\.1/);
  assert.match(startScript, /server\.js/);
});
