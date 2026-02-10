dict = []
for i in range(5):
    dict.append({f"{i}key": f"value{i}"})
print(dict)
for item in dict:
    print({k: v for k, v in item.items()})
dict.sort(key=lambda x: list(x.keys())[0], reverse=True)
print(dict)
for item in dict:
    print(item.values())
