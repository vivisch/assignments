def longest_sub(s):
  result_len = 0
  result=""
  substr = []
  for i in s:
    if i not in result:
      result+=i
    else:
      result = result.split(i)[1] + i
    substr.append(result)
    result_str = max(substr, key=len)
    result_len = len(result_str)
  print(f"The answer is '{result_str}', with the length of {result_len}.")
  
   
  
    

longest_sub("bbbbbabcdefgbbbabcdefghij")
longest_sub("abcabcabcbb")
longest_sub("bbbb")
longest_sub("pwwkew")
