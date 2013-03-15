python graphemeData.py
sed -e 's/\\\\u/\\u/g' data/GraphemeBreakRules.js > tmp
mv tmp data/GraphemeBreakRules.js
