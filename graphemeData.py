import re;
import rulesTokenizer;
import pprint;

ifile_rules = open("data/char.txt", "r");
ifile_values = open("data/GraphemeBreakProperty.txt", "r");

ofile_output = open("data/GraphemeBreakRules.js", "wb");

patterns = {         #Regex patterns found in the data files
     "declaration" : re.compile(r"\s*\$(?P<key>.+?)\s*=\s*\[\\p\{Grapheme_Cluster_Break\s*=\s*(?P<property>.+?)\}\];"),
     "ruleType"    : re.compile(r"\!\!(?P<type>.+?);"),
     "skipLine"    : re.compile(r"^\s*(#.*)?$"),
     "properties"  : re.compile(r"(?P<start>[\dA-F]{4,5})(\.\.(?P<end>[\dA-F]{4,5}))?\s*;\s*(?P<key>[A-Za-z_]+)")
};

values   = {};       #Values from GraphemeBreakProperty.txt
mappings = {};       #Mappings for keys in rules to keys in values. Usually will be equal
rules    = {};       #Break rules

currentRuleType = "Unknown";

#Read all the properties in GraphemeBreakProperty.txt
for line in ifile_values:
   prop = patterns["properties"].match(line);
   if prop:                           #If line is a property, save it, otherwise skip line
      (key, start, end) = prop.group("key", "start", "end");
      result = "\u" + start;
      if end:
         result += "-\u" + end;

      if not values.has_key(key):     #If key does not exist already, create new
         values[key] = "";

      values[key] += result;          #Append result to existing value for this key


#Now we can read the rules
for line in ifile_rules:
   decl     = patterns["declaration"].match(line);
   ruleType = patterns["ruleType"].match(line);

   if patterns["skipLine"].match(line):    #Skip empty or comment lines
      continue;

   elif decl:                         #Declaration. Save mapping
      mappings[decl.group("key")] = decl.group("property");

   elif ruleType:                     #Rule type. forward/backward. Change direction
      if ruleType.group(1) == "chain":         #Not really sure what this keyword does, skipping it
         continue;
      
      if not rules.has_key(ruleType.group(1)):
         rules[ruleType.group(1)] = [];

      currentRuleType = ruleType.group(1);         #Change type being processed

   else:                              #Ok, we are reading a rule now, add this rule
      rules[currentRuleType].append(rulesTokenizer.getRule(line, mappings, values));


ifile_values.close();
ifile_rules.close();

#print "GraphemeBreakRules = {";
#print "\n    forward: ";
#pprint.pprint(rules["forward"][1:]);
#print "\n}";

ofile_output.truncate();
print >>ofile_output, "GraphemeBreakRules = {";
print >>ofile_output, "    forward: " + `rules["forward"]`;
#print >>ofile_output, ",\n    reverse: " + `rules["reverse"]`;    #Reverse is not currently required. May be needed in the future
print >>ofile_output, "};";
ofile_output.close();
