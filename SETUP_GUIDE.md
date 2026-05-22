# 🎤 Sound Wave Runner — Setup Guide

## Why NOT GDevelop for this game?

GDevelop is great for many games, but **Sound Wave Runner's entire gameplay depends on detecting microphone volume levels** (whisper → slow-mo, normal → jump, scream → big jump). GDevelop cannot reliably do this on mobile. It would work poorly or not at all.

**The solution: HTML5 + JavaScript**
- Runs in any browser instantly — no install needed
- Web Audio API gives perfect, precise mic volume detection
- You can test changes in 1 second
- Package as Android APK later with ONE extra tool (Capacitor)
- VS Code (which you already have) is the perfect editor for this

---

## ✅ What You Need Right Now (To Play)

You already have everything you need for the prototype!

| What | Status |
|------|--------|
| VS Code | ✅ Already installed |
| Google Chrome | You need this (free) |
| The game file | ✅ Created for you |

**That's it.** No other installs needed to play the prototype.

---

## 🚀 How To Play Right Now (3 steps)

### Step 1 — Open the game folder
Open VS Code, then go to:
```
File → Open Folder → C:\Users\Win10\Documents\Claude\Projects\Sound Wave Runner
```

### Step 2 — Open the game in Chrome
Find `index.html` in the VS Code file explorer (left sidebar).  
Right-click it → **"Open with Live Server"**  

> ⚠️ If you don't see "Open with Live Server", do this first:
> 1. In VS Code, press `Ctrl+Shift+X` (opens Extensions)
> 2. Search for **"Live Server"** by Ritwick Dey
> 3. Click Install
> 4. Restart VS Code, then try again

### Step 3 — Allow microphone & play!
- Chrome will ask for microphone permission → click **Allow**
- Click the canvas to start
- **Whisper** = slow motion
- **Normal voice / "ahhh"** = small jump
- **SCREAM** = big jump / dash

---

## 🎮 How The Game Works (Simple Explanation)

```
Your Voice → Microphone → Web Audio API → Volume Number (0-100)
                                                    ↓
                                    0-15  = SLOW MOTION (blue tint)
                                   15-60  = SMALL JUMP
                                   60-100 = BIG JUMP / DASH
```

The character runs automatically from left to right.  
Obstacles come from the right side of the screen.  
You jump OVER them using your voice.  
The game speeds up the longer you survive.  
Die → big red screen → retry instantly.

---

## 📁 Project File Structure

```
Sound Wave Runner/
├── index.html        ← THE ENTIRE GAME (open this in Chrome)
├── SETUP_GUIDE.md    ← This file
└── (future files)
    ├── assets/       ← images, sounds (later)
    └── android/      ← Android build files (later)
```

The whole MVP is one file. Simple.

---

## 🔧 Making Changes (How To Edit)

1. Open `index.html` in VS Code
2. Find the `// GAME SETTINGS` section near the top of the `<script>`
3. Change numbers and save (`Ctrl+S`)
4. Chrome auto-refreshes (if using Live Server)

### Key settings you can tweak:
```javascript
const LOW_THRESHOLD = 15;    // How quiet is "whisper" (lower = more sensitive)
const HIGH_THRESHOLD = 55;   // How loud is "scream" (lower = easier to trigger)
const SMALL_JUMP_FORCE = -11; // How high small jump goes (more negative = higher)
const BIG_JUMP_FORCE = -17;   // How high big jump goes
const BASE_SPEED = 4;         // Starting game speed (higher = harder)
```

---

## 📱 Future: Package For Android (When Ready)

When you're happy with the game and want to put it on Android:

1. Install **Node.js** (free): https://nodejs.org
2. Run these commands in terminal:
```bash
npm install -g @capacitor/cli
npx cap init "Sound Wave Runner" "com.yourname.soundwaverunner"
npx cap add android
npx cap open android
```
3. Android Studio opens → click the Play button → builds your APK

*(We'll do this together step by step when you're ready)*

---

## 🆘 Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| "Microphone blocked" | Click the lock icon in Chrome's address bar → Allow microphone |
| Game is too fast | Lower `BASE_SPEED` in settings |
| Jumps won't trigger | Adjust `LOW_THRESHOLD` lower (try 10) |
| Scream jump not working | Lower `HIGH_THRESHOLD` (try 45) |
| Page not refreshing on save | Make sure Live Server is running (blue bar at bottom of VS Code) |
