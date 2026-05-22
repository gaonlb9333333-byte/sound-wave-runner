// sync.js — copies game files into www/ before Capacitor sync
// Run: node sync.js
const fs = require('fs');
const path = require('path');

const SRC = __dirname;
const DEST = path.join(__dirname, 'www');

// Create www/ if it doesn't exist
if (!fs.existsSync(DEST)) fs.mkdirSync(DEST);

// Copy index.html
fs.copyFileSync(path.join(SRC, 'index.html'), path.join(DEST, 'index.html'));
console.log('✓ Copied index.html');

// Copy assets/ folder recursively
function copyDir(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const file of fs.readdirSync(src)) {
    const s = path.join(src, file);
    const d = path.join(dest, file);
    if (fs.statSync(s).isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

const assetsDir = path.join(SRC, 'assets');
if (fs.existsSync(assetsDir)) {
  copyDir(assetsDir, path.join(DEST, 'assets'));
  console.log('✓ Copied assets/');
}

console.log('\n✅ www/ is ready! Now run: npx cap sync android');
