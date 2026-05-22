# Sound Wave Runner — Build APK Guide

## Što trebaš instalirati (samo jednom)

1. **Node.js** — https://nodejs.org (klikni LTS verziju)
2. **Android Studio** — https://developer.android.com/studio

---

## KORAK 1 — Instaliraj Capacitor pakete

Otvori **Command Prompt** i ukucaj:

```
cd "C:\Users\Win10\Documents\Claude\Projects\Sound Wave Runner"
npm install
```

Čekaj da završi (par minuta, skida pakete).

---

## KORAK 2 — Dodaj Android projekat

```
npx cap add android
```

Ovo kreira `android/` folder (pravi Android projekat).

---

## KORAK 3 — Sinkroniziraj game fajlove

Svaki put kad promijeniš igru, pokreni ovo:

```
node sync.js
npx cap sync android
```

---

## KORAK 4 — Otvori u Android Studiju

```
npx cap open android
```

Android Studio se otvori automatski.

---

## KORAK 5 — Dodaj Mic permisiju (VAŽNO — jednom)

U Android Studiju:
1. Lijevo panel → `app` → `manifests` → dvokliks na `AndroidManifest.xml`
2. Nađi liniju `<uses-permission android:name="android.permission.INTERNET" />`
3. **Ispod** te linije dodaj:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
```

4. `Ctrl+S` da sačuvaš

---

## KORAK 6 — Build APK

U Android Studiju:
1. Gornji meni: **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. Čekaj (2-5 minuta prvi put)
3. Pojavi se notifikacija "APK(s) generated" → klikni **locate**

APK fajl je na:
```
android\app\build\outputs\apk\debug\app-debug.apk
```

---

## KORAK 7 — Instaliraj na telefon

**Opcija A — USB:**
1. Povezi telefon USB kablom
2. Na telefonu: Dozvoli prenos fajlova
3. Kopiraj `app-debug.apk` na telefon
4. Na telefonu otvori fajl i instaliraj

**Opcija B — WhatsApp/Telegram:**
1. Pošalji `app-debug.apk` sebi na WhatsApp/Telegram
2. Na telefonu: otvori fajl → Instaliraj
3. Ako traži "Allow from unknown sources" → dozvoli

---

## Kad izmijeniš igru — update APK

```
node sync.js
npx cap sync android
```
Pa u Android Studiju: **Build APK** ponovo.

---

## Problemi?

**"SDK not found"** → Android Studio → SDK Manager → instaliraj Android 14 (API 34)

**"Gradle sync failed"** → File → Sync Project with Gradle Files

**Mic ne radi na telefonu** → Provjeri da si dodao RECORD_AUDIO u manifest (Korak 5)
