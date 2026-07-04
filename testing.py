# name = [{"student": "developer"}, {"student": "designer"}]

# for key in name:
#     print(key["student"])


# l = []

# for index, value in enumerate(s):
    
#     l.append(s[(len(s)) - (index + 1)])

# print("".join(l))

# # second method

# for index, value in enumerate(s):
    
#     l.append(s[-(index + 1)])

# print("".join(l))

s = "django"

result = ""

for ch in s:
    result = ch + result

print(result)