from itertools import permutations 

def isValidCombination(pars):
  open_counter = 0
  close_counter = 0
  for p in pars:
    if p == "(":
      open_counter+=1
    elif p == ")":
      close_counter+=1
    if open_counter < close_counter:
      return False
  return True

   
def parenthesesCombination(n):
  result=[]
  parentheses = ( "(" + ")" )*n
  combinations = permutations(parentheses)
  for c in combinations:
    c = ''.join(c)
    if isValidCombination(c) and c not in result:
      result.append(c)
  return result

print(parenthesesCombination(3))
print(parenthesesCombination(1))
