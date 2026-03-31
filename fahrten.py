#!/usr/bin/env python3

import argparse
import csv
import datetime as _dt
import sqlite3


DB_PATH = "fahrten.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS fahrten (
  id INTEGER PRIMARY KEY,
  datum TEXT NOT NULL,
  start TEXT NOT NULL,
  ziel TEXT NOT NULL,
  kilometer REAL NOT NULL,
  euro_pro_km REAL NOT NULL,
  betrag REAL NOT NULL,
  zweck TEXT,
  projekt TEXT,
  notiz TEXT,
  erstellt_am TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fahrten_datum ON fahrten(datum);
"""


def _connect():
  con = sqlite3.connect(DB_PATH)
  con.execute("PRAGMA foreign_keys = ON")
  con.executescript(SCHEMA_SQL)
  con.commit()
  return con


def _parse_date(date_str: str) -> str:
  date_str = date_str.strip()
  if date_str.lower() in {"heute", "today"}:
    return _dt.date.today().isoformat()
  return _dt.date.fromisoformat(date_str).isoformat()


def add_fahrt(args) -> None:
  datum = _parse_date(args.datum)
  km = float(args.kilometer)
  euro_pro_km = float(args.euro_pro_km)
  betrag = km * euro_pro_km

  con = _connect()
  con.execute(
    """
    INSERT INTO fahrten (
      datum, start, ziel, kilometer, euro_pro_km, betrag,
      zweck, projekt, notiz, erstellt_am
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
      datum,
      args.start,
      args.ziel,
      km,
      euro_pro_km,
      betrag,
      args.zweck,
      args.projekt,
      args.notiz,
      _dt.datetime.now().isoformat(timespec="seconds"),
    ),
  )
  con.commit()
  print(f"Fahrt hinzugefügt: {datum} {args.start} -> {args.ziel} ({km:.1f} km)")


def list_fahrten(args) -> None:
  con = _connect()
  cur = con.cursor()

  where = []
  params: list[object] = []

  if args.von:
    where.append("datum >= ?")
    params.append(_parse_date(args.von))
  if args.bis:
    where.append("datum <= ?")
    params.append(_parse_date(args.bis))

  sql = "SELECT datum, start, ziel, kilometer, euro_pro_km, betrag, zweck, projekt, notiz FROM fahrten"
  if where:
    sql += " WHERE " + " AND ".join(where)
  sql += " ORDER BY datum"

  cur.execute(sql, params)

  rows = cur.fetchall()
  if not rows:
    print("Keine Fahrten gefunden")
    return

  print("Datum       Km   Euro/km   Betrag   Start -> Ziel")
  print("---------------------------------------------")
  total = 0.0
  for datum, start, ziel, km, euro_km, betrag, zweck, projekt, notiz in rows:
    total += betrag
    print(
      f"{datum}  {km:6.1f}  {euro_km:7.4f}  {betrag:7.2f}  {start} -> {ziel}"
      + (f"  [{zweck}]" if zweck else "")
      + (f" ({projekt})" if projekt else "")
      + (f" - {notiz}" if notiz else "")
    )
  print("---------------------------------------------")
  print(f"Summe: {total:.2f}")


def report(args) -> None:
  con = _connect()
  cur = con.cursor()

  if args.monat:
    # args.monat is expected YYYY-MM
    year, month = args.monat.split("-")
    where = "WHERE substr(datum, 1, 7) = ?"
    params = [f"{int(year):04d}-{int(month):02d}"]
    label = params[0]
  else:
    where = ""
    params = []
    label = "gesamt"

  cur.execute(
    f"SELECT COUNT(*), SUM(betrag), SUM(kilometer) FROM fahrten {where}",
    params,
  )
  count, sum_betrag, sum_km = cur.fetchone()
  sum_betrag = sum_betrag or 0.0
  sum_km = sum_km or 0.0

  print(f"Report {label}")
  print(f"Fahrten: {count}")
  print(f"Kilometer: {sum_km:.1f}")
  print(f"Betrag: {sum_betrag:.2f}")


def export_csv(args) -> None:
  con = _connect()
  cur = con.cursor()

  cur.execute(
    """
    SELECT datum, start, ziel, kilometer, euro_pro_km, betrag, zweck, projekt, notiz, erstellt_am
    FROM fahrten
    ORDER BY datum
    """
  )

  with open(args.out, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
      [
        "datum",
        "start",
        "ziel",
        "kilometer",
        "euro_pro_km",
        "betrag",
        "zweck",
        "projekt",
        "notiz",
        "erstellt_am",
      ]
    )
    writer.writerows(cur.fetchall())

  print(f"Exportiert nach {args.out}")


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(
    description="Fahrtkostenerfassung mit SQLite",
  )
  subparsers = parser.add_subparsers(dest="command", required=True)

  p_add = subparsers.add_parser("add", help="Fahrt hinzufügen")
  p_add.add_argument("datum", help="Datum im Format YYYY-MM-DD oder 'heute'")
  p_add.add_argument("start", help="Startort")
  p_add.add_argument("ziel", help="Zielort")
  p_add.add_argument("kilometer", help="Strecke in Kilometern")
  p_add.add_argument(
    "euro_pro_km",
    help="Kilometersatz in Euro, z.B. 0.30",
  )
  p_add.add_argument("--zweck", default="", help="Zweck der Fahrt")
  p_add.add_argument("--projekt", default="", help="Projekt/Kostenstelle")
  p_add.add_argument("--notiz", default="", help="Notiz")
  p_add.set_defaults(func=add_fahrt)

  p_list = subparsers.add_parser("list", help="Fahrten auflisten")
  p_list.add_argument("--von", help="Startdatum YYYY-MM-DD", default=None)
  p_list.add_argument("--bis", help="Enddatum YYYY-MM-DD", default=None)
  p_list.set_defaults(func=list_fahrten)

  p_report = subparsers.add_parser("report", help="Summen ausgeben")
  p_report.add_argument("--monat", help="Filter nach Monat YYYY-MM", default=None)
  p_report.set_defaults(func=report)

  p_export = subparsers.add_parser("export", help="CSV Export")
  p_export.add_argument("out", help="CSV Datei")
  p_export.set_defaults(func=export_csv)

  args = parser.parse_args(argv)
  args.func(args)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
