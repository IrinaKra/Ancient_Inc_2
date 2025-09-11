import sys
import requests


BASE_URL = "http://localhost:5000"


def fetch_report(month: str, department: str, kind: str = "birthdays"):
    url = f"{BASE_URL}/{kind}"
    params = {"month": month, "department": department}
    resp = requests.get(url, params=params)
    return resp.json()


def print_report(data, month: str, department: str, kind: str):
    print(f"Report for {department} department for {month.capitalize()} fetched.")
    print(f"Total: {data.get('total', 0)}")
    print("Employees:")
    field = "birthday" if kind == "birthdays" else "anniversary"
    for e in data.get("employees", []):
        print(f"- {e.get(field)}, {e.get('name')}")


def main():
    month = sys.argv[1]
    department = sys.argv[2]
    kind = sys.argv[3] if len(sys.argv) > 3 else "birthdays"

    data = fetch_report(month, department, kind)
    print_report(data, month, department, kind)


if __name__ == "__main__":
    main()