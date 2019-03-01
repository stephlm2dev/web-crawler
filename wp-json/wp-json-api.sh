#!/usr/bin/env bash

if [ $# -ne 2 ]
then
  echo "Usage: ./wp-json-api.sh <ROUTE> <WEBSITE>"
  echo "ROUTE can be 'posts', 'categories', 'tags', 'pages'"
  exit 1
fi

# Main variables
ROUTE=$1
WEBSITE=$2
OUTPUT_FILE="${ROUTE}.csv"
PER_PAGE=100

echo "[${ROUTE}] Task started"

# First call
rm -fr $TMPDIR/headers
http -h ${WEBSITE}/wp-json/wp/v2/${ROUTE} per_page==${PER_PAGE} page==1 > $TMPDIR/headers
MAX_POSTS=$(cat $TMPDIR/headers | grep 'X-WP-Total:' | awk -F ":" {'print int($2)'})
MAX_PAGES=$(cat $TMPDIR/headers | grep 'X-WP-TotalPages:' | awk -F ":" {'print int($2)'})

echo "Found ${MAX_POSTS} ${ROUTE}"
echo 'url,title' > ${OUTPUT_FILE}

for i in $(seq 1 $MAX_PAGES)
do
  echo "${i}/${MAX_PAGES}"
  http ${WEBSITE}/wp-json/wp/v2/${ROUTE} per_page==${PER_PAGE} page==${i} | jq '.[] | [.link, if has("name") then .name else .title.rendered end] | @csv' --raw-output >> ${OUTPUT_FILE}
done

echo "[${ROUTE}] Task finished !"
