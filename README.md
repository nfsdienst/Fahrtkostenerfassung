# Fahrtkostenerfassung – Kirchenkreis

Eine moderne, DSGVO-konforme Webanwendung zur digitalen Erfassung von Fahrtkosten für Veranstaltungen eines Kirchenkreises.

---

## Inhaltsverzeichnis

1. [Überblick](#überblick)
2. [Technologie-Stack](#technologie-stack)
3. [Projektstruktur](#projektstruktur)
4. [Schritt-für-Schritt: Firebase einrichten](#firebase-einrichten)
5. [Schritt-für-Schritt: Netlify Deployment](#netlify-deployment)
6. [Lokale Entwicklung](#lokale-entwicklung)
7. [Admin-Benutzerkonto anlegen](#admin-benutzerkonto-anlegen)
8. [QR-Code generieren](#qr-code-generieren)
9. [Bedienungsanleitung Admin](#bedienungsanleitung-admin)
10. [DSGVO & Datenschutz](#dsgvo--datenschutz)
11. [Firestore Security Rules](#firestore-security-rules)
12. [Wartung & Troubleshooting](#wartung--troubleshooting)

---

## Überblick

### Für Teilnehmende (öffentlich)

1. QR-Code scannen → Landingpage öffnet sich
2. 4-stellige Veranstaltungs-PIN eingeben
3. Formular ausfüllen (Name, Kilometer, IBAN, Datenschutz-Zustimmung)
4. Absenden → Bestätigungsmeldung

### Für Admins (geschützt)

- Login mit E-Mail + Passwort (Firebase Auth)
- Veranstaltungen erstellen, bearbeiten, löschen
- Alle Einträge einsehen (IBAN standardmäßig maskiert)
- Export als Excel (.xlsx) oder PDF

---

## Technologie-Stack

| Schicht       | Technologie                    |
|---------------|-------------------------------|
| Frontend      | React 18 + Vite                |
| Routing       | React Router v6                |
| Datenbank     | Google Firestore (NoSQL)       |
| Auth          | Firebase Authentication        |
| Hosting       | Netlify (CDN, HTTPS automatisch)|
| Export        | jsPDF + jspdf-autotable, SheetJS|
| Fonts         | DM Serif Display + DM Sans     |

---

## Projektstruktur

```
fahrtkostenerfassung/
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   └── index.jsx          # ProtectedRoute, CrossIcon, AdminNav, PageFooter
│   ├── contexts/
│   │   └── AuthContext.jsx    # Firebase Auth State Management
│   ├── pages/
│   │   ├── LandingPage.jsx    # PIN-Eingabe (öffentlich)
│   │   ├── EventForm.jsx      # Teilnehmer-Formular
│   │   ├── SuccessPage.jsx    # Erfolgsmeldung
│   │   ├── Datenschutz.jsx    # DSGVO-Seite
│   │   └── admin/
│   │       ├── AdminLogin.jsx
│   │       ├── AdminDashboard.jsx
│   │       └── AdminEventDetail.jsx
│   ├── utils/
│   │   ├── ibanValidator.js   # IBAN-Prüfung (Mod-97), Maskierung, Formatierung
│   │   └── exportUtils.js     # Excel- und PDF-Export
│   ├── styles/
│   │   └── global.css         # Design System (CSS Custom Properties)
│   ├── firebase.js            # Firebase-Initialisierung
│   ├── App.jsx                # Router-Konfiguration
│   └── main.jsx               # Einstiegspunkt
├── firestore.rules            # Security Rules (in Firebase deployen!)
├── netlify.toml               # Netlify Build & Security Headers
├── .env.example               # Vorlage für Umgebungsvariablen
├── vite.config.js
└── package.json
```

---

## Firebase einrichten

### Schritt 1: Firebase-Projekt erstellen

1. Gehen Sie zu https://console.firebase.google.com
2. Klicken Sie auf **„Projekt hinzufügen"**
3. Projektname: z. B. `kirchenkreis-fahrtkosten`
4. Google Analytics: optional (kann deaktiviert werden)
5. Auf **„Projekt erstellen"** klicken

### Schritt 2: Web-App registrieren

1. Im Firebase-Dashboard: Zahnrad-Symbol → **„Projekteinstellungen"**
2. Unter **„Ihre Apps"** → **„Web"** (</> Symbol) klicken
3. App-Nickname: `Fahrtkostenerfassung`
4. **„App registrieren"** → Firebase SDK-Konfiguration kopieren:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "kirchenkreis-fahrtkosten.firebaseapp.com",
  projectId: "kirchenkreis-fahrtkosten",
  storageBucket: "kirchenkreis-fahrtkosten.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};
```

### Schritt 3: Firestore Datenbank aktivieren

1. Im linken Menü: **„Firestore Database"** → **„Datenbank erstellen"**
2. Modus: **„Im Produktionsmodus starten"** (wichtig für Sicherheit)
3. Region: **`europe-west3` (Frankfurt)** ← DSGVO-konform!
4. Fertig

### Schritt 4: Security Rules deployen

> ⚠️ Wichtig: Ohne korrekte Rules sind die Daten nicht sicher geschützt!

**Option A – Firebase CLI (empfohlen):**
```bash
npm install -g firebase-tools
firebase login
firebase init firestore          # Projekt auswählen
# firestore.rules ist bereits vorhanden → bestehende Datei verwenden
firebase deploy --only firestore:rules
```

**Option B – Firebase Console:**
1. Firestore → **„Regeln"** Tab
2. Inhalt von `firestore.rules` einfügen
3. **„Veröffentlichen"** klicken

### Schritt 5: Firebase Authentication aktivieren

1. Im linken Menü: **„Authentication"** → **„Jetzt loslegen"**
2. Tab **„Anmeldemethoden"** → **„E-Mail/Passwort"** → Aktivieren
3. **„Speichern"**

### Schritt 6: Admin-Benutzer anlegen

1. Authentication → **„Benutzer"** Tab → **„Benutzer hinzufügen"**
2. E-Mail: z. B. `admin@kirchenkreis-musterstadt.de`
3. Passwort: sicheres Passwort wählen (min. 12 Zeichen, Groß/Kleinbuchstaben, Zahlen, Sonderzeichen)
4. **„Benutzer hinzufügen"**

> 💡 Mehrere Admins möglich: Schritt 6 für jede Person wiederholen.

---

## Netlify Deployment

### Schritt 1: Repository erstellen

```bash
git init
git add .
git commit -m "Initial commit: Fahrtkostenerfassung"
```

Erstellen Sie ein neues Repository auf GitHub/GitLab und pushen Sie den Code.

### Schritt 2: Netlify-Konto und neues Projekt

1. https://www.netlify.com → Konto erstellen (kostenlos)
2. **„Add new site"** → **„Import an existing project"**
3. Git-Provider auswählen → Repository auswählen
4. Build-Einstellungen werden automatisch aus `netlify.toml` gelesen:
   - Build command: `npm run build`
   - Publish directory: `dist`

### Schritt 3: Umgebungsvariablen in Netlify setzen

In Netlify: **Site settings → Environment variables → Add variable**

| Variable                           | Wert (aus Firebase-Konfiguration) |
|------------------------------------|-----------------------------------|
| `VITE_FIREBASE_API_KEY`            | `AIza...`                         |
| `VITE_FIREBASE_AUTH_DOMAIN`        | `ihr-projekt.firebaseapp.com`     |
| `VITE_FIREBASE_PROJECT_ID`         | `ihr-projekt-id`                  |
| `VITE_FIREBASE_STORAGE_BUCKET`     | `ihr-projekt.appspot.com`         |
| `VITE_FIREBASE_MESSAGING_SENDER_ID`| `123456789`                       |
| `VITE_FIREBASE_APP_ID`             | `1:123456789:web:...`             |

> ⚠️ **Niemals** die `.env`-Datei mit echten Werten ins Git-Repository committen!

### Schritt 4: Deployment auslösen

1. **„Deploy site"** klicken
2. Nach ca. 1–2 Minuten ist die Seite live
3. Netlify vergibt automatisch eine URL: `https://random-name.netlify.app`

### Schritt 5: Eigene Domain (optional)

1. Netlify: **Domain settings → Add custom domain**
2. DNS-Einträge beim Domain-Anbieter setzen
3. Netlify aktiviert automatisch HTTPS (Let's Encrypt)

### Schritt 6: Firebase Authorized Domains aktualisieren

1. Firebase Console → Authentication → **„Einstellungen"** → **„Autorisierte Domains"**
2. Ihre Netlify-URL hinzufügen: `ihre-domain.netlify.app` oder eigene Domain
3. **„Speichern"**

---

## Lokale Entwicklung

```bash
# 1. Abhängigkeiten installieren
npm install

# 2. .env-Datei erstellen
cp .env.example .env
# → Datei öffnen und Firebase-Werte eintragen

# 3. Entwicklungsserver starten
npm run dev
# → http://localhost:5173

# 4. Production-Build testen
npm run build
npm run preview
```

---

## QR-Code generieren

Der QR-Code zeigt immer auf die **Haupt-URL** (Landing Page), z. B.:
```
https://ihre-domain.netlify.app/
```

### QR-Code erstellen:

**Kostenlos online:**
- https://www.qr-code-generator.com
- https://qrcode.tec-it.com/de

**Empfohlene Einstellungen:**
- Format: PNG, min. 1000×1000 px für Drucke
- Fehlerkorrektur: **Level H** (30%) – für Logos im QR-Code
- Quiet Zone: 4 Module Rand

**Druckempfehlung:**
- Mindestgröße auf Papier: 3 × 3 cm
- Testen Sie den QR-Code vor dem Druck mit mehreren Geräten

---

## Bedienungsanleitung Admin

### Admin-Bereich aufrufen
URL: `https://ihre-domain.netlify.app/admin/login`

### Neue Veranstaltung anlegen
1. Admin-Dashboard öffnen
2. **„Neue Veranstaltung"** klicken
3. Name eingeben (z. B. „Kreissynode Frühjahr 2025")
4. Datum wählen
5. PIN wird automatisch generiert (kann manuell geändert werden)
6. **„Speichern"**

### PIN an Teilnehmende weitergeben
Die 4-stellige PIN ist im Dashboard bei jeder Veranstaltung sichtbar.
Weitergabe per:
- Ankündigung im Gottesdienst/Meeting
- E-Mail an Teilnehmende
- Auf dem Veranstaltungsflyer

### Einentries einsehen
1. Auf **„Einträge"** bei der gewünschten Veranstaltung klicken
2. Alle eingegangenen Datensätze werden tabellarisch angezeigt
3. IBAN standardmäßig maskiert → Augen-Symbol zum Aufdecken
4. Suchfunktion nach Name oder IBAN
5. Sortierung nach Name, Kilometer oder Eingabedatum

### Daten exportieren
Im Eintragsbereich:
- **„Excel (.xlsx)"** → tabellarische Auswertung
- **„PDF"** → formatiertes Dokument für Ablage/Druck

### Eintrag löschen (DSGVO-Anfrage)
Im Eintragsbereich → Papierkorb-Symbol neben dem Eintrag → Bestätigen

### Veranstaltung löschen
Im Dashboard → **„Löschen"** → Bestätigen
> ⚠️ Dabei werden **alle zugehörigen Einträge** unwiderruflich gelöscht!

---

## DSGVO & Datenschutz

### Maßnahmen in dieser Anwendung

| Maßnahme | Umsetzung |
|----------|-----------|
| Verschlüsselte Übertragung | HTTPS/TLS (Netlify + Let's Encrypt) |
| Datenzugriff | Nur für authentifizierte Admins |
| Keine öffentliche Datensicht | Firestore Security Rules |
| IBAN-Maskierung | Standardmäßig im Admin-Bereich |
| Datenschutzerklärung | Eigene Seite + Pflicht-Checkbox |
| Einwilligung | Checkbox vor Formularabsenden |
| EU-Datenspeicherung | Firebase Region europe-west3 (Frankfurt) |
| Löschfunktion | Admin kann einzelne Einträge + Veranstaltungen löschen |
| Security Headers | X-Frame-Options, CSP, etc. (netlify.toml) |

### Datenschutzerklärung anpassen

Die Datenschutzerklärung befindet sich in `src/pages/Datenschutz.jsx`.

**Folgende Platzhalter müssen angepasst werden:**
- `[Name des Kirchenkreises]`
- `[Straße und Hausnummer]`
- `[PLZ und Ort]`
- `[datenschutz@kirchenkreis-xy.de]`
- `[Bundesland]` und `[Name und Adresse der Aufsichtsbehörde]`

### Auftragsverarbeitungsvertrag (AVV)

Mit Google/Firebase muss ein AVV geschlossen werden:
→ https://firebase.google.com/terms/data-processing-terms

### Empfohlene weitere Maßnahmen

- **Verzeichnis von Verarbeitungstätigkeiten** (VVT) anlegen
- **Datenschutz-Folgenabschätzung (DSFA)** prüfen (bei sensiblen Bankdaten empfohlen)
- Regelmäßige Überprüfung der gespeicherten Daten
- Aufbewahrungsfristen dokumentieren und einhalten

---

## Firestore Security Rules

Die Regeln in `firestore.rules` stellen sicher:

- **Teilnehmende** können nur neue Einentries **anlegen** (create), nicht lesen
- **Admins** (authentifiziert) können alle Daten lesen, bearbeiten und löschen
- **Eingabevalidierung** serverseitig (Feldtypen, Längen)
- Alle anderen Zugriffe werden **verweigert**

Regeln müssen nach Änderungen erneut deployed werden:
```bash
firebase deploy --only firestore:rules
```

---

## Wartung & Troubleshooting

### Problem: „Veranstaltungsnummer unbekannt"
- Prüfen Sie, ob die PIN korrekt eingegeben wurde
- Im Admin-Dashboard: PIN der Veranstaltung kontrollieren
- Firestore-Konsole: Collection `events` prüfen

### Problem: Admin-Login schlägt fehl
- E-Mail und Passwort prüfen
- Firebase Console → Authentication → Benutzer prüfen
- „Zu viele Anmeldeversuche": 5 Minuten warten

### Problem: Daten erscheinen nicht im Admin
- Browser-Cache leeren (Strg+Shift+R)
- Firestore Security Rules überprüfen
- Firebase Console → Firestore → Collection `entries` direkt prüfen

### Problem: Export funktioniert nicht
- Pop-up-Blocker deaktivieren (Downloads werden blockiert)
- Anderen Browser verwenden

### Sicherheitsupdate
```bash
# Abhängigkeiten auf Sicherheitslücken prüfen
npm audit

# Updates installieren
npm update

# Major Updates (mit Vorsicht)
npx npm-check-updates -u && npm install
```

### Firebase-Kosten
Die kostenlose Firebase Spark-Plan-Grenze:
- Firestore: 1 GB Speicher, 50.000 Lesevorgänge/Tag
- Authentication: unbegrenzt
- Für einen Kirchenkreis mit wenigen Veranstaltungen/Jahr: **kostenlos**

---

## Kontakt & Support

Bei Fragen zur Einrichtung oder technischen Problemen:
→ Dokumentation: https://firebase.google.com/docs
→ Netlify Docs: https://docs.netlify.com

---

*Erstellt für den Kirchenkreis · DSGVO-konform · Stand: 2025*
