# Fahrtkostenerfassung

Ziel dieses Projekts ist die Erfassung von Fahrten und die Berechnung der Erstattungssumme.

## Annahmen
• Python ab 3.11
• SQLite als lokale Datei fahrten.db

## Datenmodell
Tabelle fahrten
• datum
• start
• ziel
• kilometer
• euro pro kilometer
• betrag
• zweck
• projekt oder kostenstelle
• notiz
• erstellt am

## Installation und Setup
1. Repository klonen
2. Virtuelle Umgebung erstellen
3. Abhängigkeiten installieren

Python hat keine externen Abhängigkeiten. Du kannst fahrten.py direkt mit Python ausführen.

## Nutzung
Kommandos
• add fügt eine Fahrt hinzu
• list listet Fahrten im Zeitraum
• report summiert Beträge und Kilometer
• export exportiert nach CSV

Beispiele
• python fahrten.py add heute Kassel Frankfurt 200 0.30 --zweck Kundentermin --projekt Kostenstelle 123
• python fahrten.py list --von 2026-03-01 --bis 2026-03-31
• python fahrten.py report --monat 2026-03
• python fahrten.py export fahrten.csv

## Roadmap
• Filtern nach Projekt oder Kostenstelle
• Reports je Projekt
• Export als Excel oder PDF
• Optional, kleine Weboberfläche
