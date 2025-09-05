from flask import Flask, request, jsonify
import csv
from datetime import date
import calendar

app = Flask(__name__)

EMPLOYEES = []

def load_csv(path = "database.csv"):
    with open(path, newline = "") as file:
        r = csv.DictReader(file)
        for i, row in enumerate(r, start = 1):
            EMPLOYEES.append({
                "name": row["name"],
                "department": row["department"],
                "birthday": row["birthday"],       
                "hiring_date": row["hiring_date"] 
            })

def format_month(m):
    s = (m or "").strip().lower()
    names = {x.lower(): i for i, x in enumerate(calendar.month_name) if i}   
    return names.get(s)

def format_date(d):
    return date.fromisoformat(d).strftime("%b %d").replace(" 0", " ")

@app.route("/birthdays")
def birthdays():
    mon = format_month(request.args.get("month"))
    dept = (request.args.get("department") or "")
    items = [
        {"name": empl["name"], "birthday": format_date(empl["birthday"])}
        for empl in EMPLOYEES
        if empl["department"].lower() == dept.lower()
        and date.fromisoformat(empl["birthday"]).month == mon
    ]
    return jsonify({"total": len(items), "employees": items})

@app.route("/anniversaries")
def anniversaries():
    mon = format_month(request.args.get("month"))
    dept = (request.args.get("department") or "")
    items = [
        {"name": empl["name"], "anniversary": format_date(empl["hiring_date"])}
        for empl in EMPLOYEES
        if empl["department"].lower() == dept.lower()
        and date.fromisoformat(empl["hiring_date"]).month == mon
    ]
    return jsonify({"total": len(items), "employees": items})

load_csv("database.csv")

if __name__ == "__main__": 
    app.run()