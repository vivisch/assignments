def palindromPartitioning(s):
  result = []
  substring=""
  for letter in s:
    substring += letter
    if substring == substring[::-1]:
      result.append(substring)
  return result

print(palindromPartitioning("aab"))
print(palindromPartitioning("a"))
