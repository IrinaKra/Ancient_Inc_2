import csv
import calendar

from datetime import date
from flask import Flask, request, jsonify
from pathlib import Path
from typing import List, Dict, Optional


app = Flask(__name__)

DB_PATH = Path("database.csv")
FIELDS = ["name", "department", "birthday", "hiring_date"]


def check_db(path: Path = DB_PATH) -> bool:
    return path.exists() and path.is_file()


def create_db(path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents = True, exist_ok = True)
    with path.open("w", newline = "") as file:
        csv.DictWriter(file, fieldnames = FIELDS).writeheader()


def read_db(path: Path = DB_PATH) -> List[Dict[str, str]]:
    rows = []
    with path.open("r", newline = "") as file:
        reader = csv.DictReader(file)
        for i in reader:
            rows.append({
                "name": i.get("name", "").strip(),
                "department": i.get("department", "").strip(),
                "birthday": i.get("birthday", "").strip(),
                "hiring_date": i.get("hiring_date", "").strip(),
            })
    return rows


def write_db(record: dict, path: Path) -> None:
    with path.open("a", newline = "") as file:
        csv.DictWriter(file, fielnames = FIELDS).writerow


def format_month(m): 
    s = (m or "").strip().lower() 
    names = {x.lower(): i for i, x in enumerate(calendar.month_name) if i} 
    return names.get(s)


def format_date(d: str) -> str:
    return date.fromisoformat(d).strftime("%b %d").replace(" 0", " ")


def birthdays_report(employees, month, department):
    items = [
        {"name": empl["name"], "birthday": format_date(empl["birthday"])}
        for empl in employees
        if empl["department"].lower() == department.lower()
        and date.fromisoformat(empl["birthday"]).month == month
    ]
    return {"total": len(items), "employees": items}


def anniversaries_report(employees, month, department):
    items = [
        {"name": empl["name"], "anniversary": format_date(empl["hiring_date"])}
        for empl in employees
        if empl["department"].lower() == department.lower()
        and date.fromisoformat(empl["hiring_date"]).month == month
    ]
    return {"total": len(items), "employees": items}


@app.route("/birthdays")
def birthdays():
    mon = format_month(request.args.get("month"))
    dept = (request.args.get("department") or "").strip()
    if mon is None:
        return jsonify({"error": "Parameter 'month' is invalid."}), 400
    if not dept:
        return jsonify({"error": "Parameter 'department' is required."}), 400
    return jsonify(birthdays_report(read_db(), mon, dept))


@app.route("/anniversaries") 
def anniversaries(): 
    mon = format_month(request.args.get("month")) 
    dept = (request.args.get("department") or "") 
    if mon is None:
        return jsonify({"error": "Parameter 'month' is invalid."}), 400
    if not dept:
        return jsonify({"error": "Parameter 'department' is required."}), 400
    return jsonify(anniversaries_report(read_db(), mon, dept))


create_db(DB_PATH)


if __name__ == "__main__":
    app.run()