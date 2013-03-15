import re;

scanner = re.Scanner([
    (r"\$[A-Za-z_]\w*", lambda scanner, token: ("VARIABLE", token[1:])),
    (r"\(", lambda scanner, token: ("GROUP_OPEN", token)),
    (r"\)", lambda scanner, token: ("GROUP_CLOSE", token)),
    (r"\[", lambda scanner, token: ("SQ_GROUP_OPEN", token)),
    (r"\]", lambda scanner, token: ("SQ_GROUP_CLOSE", token)),
    (r"\|", lambda scanner, token: ("PIPE", token)),
    (r"\^", lambda scanner, token: ("NEGATE_NEXT", token)),
    (r";", lambda scanner, token: ("SEMI_COLON", token)),
    (r"\s+", None),   #Ignore whitespace
]);

def getRule(line, mappings, values):
   results   = scanner.scan(line) [0];
   numTokens = len(results);
   rule = "";

   inSqGroup = False;
   
   for i in range(numTokens):
      tokenType, token = results[i];

      next = None; prev = None;      #Look ahead/behind
      if i != 0: 
          prev  = results[i-1][0];

      if i < numTokens-1:
          next = results[i+1][0];

      if tokenType == "SQ_GROUP_OPEN":
         rule += token;
         inSqGroup = True;

      elif tokenType == "SQ_GROUP_CLOSE":
         rule += token;
         inSqGroup = False;

      elif tokenType == "GROUP_OPEN" or tokenType == "GROUP_CLOSE" or tokenType == "PIPE" or tokenType == "NEGATE_NEXT":
         rule += token;

      elif tokenType == "VARIABLE":
         key = mappings[token];
         value = values[key];

         if prev != "PIPE" and not inSqGroup:
            value = "[" + value;

         if next != "PIPE" and not inSqGroup:
            value = value + "]";

         rule += value;

      elif tokenType == "SEMI_COLON":
         #End of rule. Do nothing
         continue;

      else:
         #Error. We have a problem
         raise Exception("Syntax error. Invalid tokens", tokenType, token);

   return rule;
