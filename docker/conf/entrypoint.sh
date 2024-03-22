#!/bin/bash
set -e

export DOLLAR="$" # this way envsubst won't break nginx' variables that begins with $ in nginx.conf (e.g., $host)

function create_conf_file {
  SET_BIOBANK_ID=$2
  echo "Server conf $1"
  # Check if SSL is enabled and certs presents. It creates the template file name accordingli (i.e., it adds the .ssl string if enabled
  if [ -n  "$SSL_ENABLED" ] && [ "$SSL_ENABLED" == "true" ]; then
    if [ -f "$SSL_KEY_FILE" ] && [ -f "$SSL_CERT_FILE" ]; then
      SSL_FILE_SUBSTRING=".ssl"
    else
      echo "Missing key and or cert file"
      echo "Mount files at ${SSL_KEY_FILE} and ${SSL_CERT_FILE}"
      exit 0
    fi
  else
    SSL_FILE_SUBSTRING=""
  fi

  # split biobank into id and port
  IFS=":" read -a biobank <<< "$1"
  if [ "$SET_BIOBANK_ID" == "true" ]; then
    TEMPLATE_FILE=/beacon/nginx/service/server.biobank"$SSL_FILE_SUBSTRING".conf.template
  else
    TEMPLATE_FILE=/beacon/nginx/service/server"$SSL_FILE_SUBSTRING".conf.template
  fi

  export BIOBANK_ID="${biobank[0]}"
#  export SERVER_NAME="${biobank[0]}"
  export PORT="${biobank[1]}"
  echo "Configuring server $BIOBANK_ID at port $PORT"

  envsubst < $TEMPLATE_FILE > /beacon/nginx/service/server."$BIOBANK_ID".conf
}

if [ -n "$BIOBANKS" ]; then
  # transform the biobanks string into an array
  IFS=";" read -a biobanks <<< "$BIOBANKS"
  NUM_BIOBANKS="${#biobanks[@]}"
  echo "Number of biobanks: $NUM_BIOBANKS"
  echo "First biobank is ${biobanks[0]}"
  if [ "$NUM_BIOBANKS" == "1" ]; then
    # If there is only one biobank it's not necessary to specify it in the Header
    create_conf_file "$BIOBANKS" false
  else
    # It creates a file for each biobank
    for b in "${biobanks[@]}"; do
      b=$(echo $b | sed 's/ *$//g') # don't doublequote $b, it would break trimming
      echo "Processing biobank ${b}"
      create_conf_file "${b}" true
    done
  fi
else
  create_conf_file "$SERVER_NAME:$PORT" false
fi

supervisord -c /beacon/supervisord.conf -n
