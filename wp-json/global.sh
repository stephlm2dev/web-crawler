#!/usr/bin/env bash

if [ $# -ne 2 ]
then
  echo "Usage: ./global.sh <WEBSITE> <DIRECTORY>"
  exit 1
fi

# Main variables
WEBSITE=$1
DIRECTORY=$2
CURRENT_DIRECTORY=$(PWD)

rm -fr ${DIRECTORY}
mkdir ${DIRECTORY}
cd ${DIRECTORY}

${CURRENT_DIRECTORY}/wp-json-api.sh 'posts' ${WEBSITE}
printf "\n"

${CURRENT_DIRECTORY}/wp-json-api.sh 'pages' ${WEBSITE}
printf "\n"

${CURRENT_DIRECTORY}/wp-json-api.sh 'tags' ${WEBSITE}
printf "\n"

${CURRENT_DIRECTORY}/wp-json-api.sh 'categories' ${WEBSITE}
printf "\n"
