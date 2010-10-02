#!/bin/bash
#
# google.sh
# ---------
# Automatic Google search from the command line.
#
# Syntax : $ google {search terms}
#
if [ -z $1 ]
then
# If no keyword is entered echo try again
#
echo "You didnt tell me what to search....try again"
else
#url variable with the maximum search results (100) per page
#
url='http://google.com/search?num=100&hl=en&safe=off&q='
appended=0
for searchTerm in "$@"
do
# Replace white spaces in the search terms
#
searchTerm=`echo $searchTerm | sed 's/ /%20/g'`
url="$url%22$searchTerm%22"
if [ $appended -lt `expr $# - 1` ]
then
url="$url"\+
else
url="$url"\&btnG\=Google\+Search\&meta\=
fi
let "appended+=1"
done
wget --user-agent="Firefox" -O - $url --quiet > googleresult1
sed 's/http/\^http/g' googleresult1 | tr -s "^" "\n" | grep http| sed 's/\ .*//g' >> googleresults2 #this command extract only the urs
rm googleresult1
cat googleresults2
rm googleresults2
sed -e '/google/d' googleresults2 > urls.txt
fi

