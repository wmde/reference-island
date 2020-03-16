import json
with open('ext_idef_check_result.json', 'r') as f:
    data = json.loads(f.read())
print('Total: ', len(data))
goods = []
schemas = []
for i in data:
    if data[i][1] > 5:
        goods.append(i)
    if data[i][2] > 5:
        schemas.append(i)
print('Good: ', len(goods))
print('Schemas: ', len(schemas))

print(schemas)
