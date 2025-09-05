import sys
import requests

month = sys.argv[1]          
department = sys.argv[2]     
kind = sys.argv[3] if len(sys.argv) > 3 else "birthdays"  

url = f"http://localhost:5000/{kind}"
params = {"month": month, "department": department}

r = requests.get(url, params = params)
data = r.json()

print(f"Report for {department} department for {month.capitalize()} fetched.")
print(f"Total: {data.get('total', 0)}")
print("Employees:")
for e in data.get("employees", []):
    field = "birthday" if kind == "birthdays" else "anniversary"
    print(f"- {e.get(field)}, {e.get('name')}")