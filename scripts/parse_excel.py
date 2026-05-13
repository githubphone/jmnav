import openpyxl
import json

wb = openpyxl.load_workbook('系统跳转.xlsx')
ws = wb['Sheet1']

data = []
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 2:
        continue
    if row[0] is None and row[1] is None:
        continue
    data.append({
        'id': row[0],
        'name': row[1],
        'department': row[2],
        'description': row[3]
    })

with open('systems.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Total: {len(data)} systems')
for d in data:
    name = (d['name'] or '').replace('\n', ' ')
    dept = (d['department'] or '').replace('\n', ' ')
    print(f'{d["id"]}. {name} | {dept}')
