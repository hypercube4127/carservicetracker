#!/bin/bash
CONFIG_FILE="/opt/project/assets/config.json"
RUN_AS_DAEMON="false"
SLEEP_SECONDS=1
TEMP_FILE="/tmp/config.json.bak"

ENV_VARS=("production" "backendUrl" "defaultLocale")

while getopts "f:s:d:h" opt; do
  case $opt in
    f)
      CONFIG_FILE=$OPTARG
      ;;
    d)
      RUN_AS_DAEMON=$OPTARG
      ;;
    s)
      SLEEP_SECONDS=$OPTARG
      ;;
    h)
      echo "Usage: envtoconfig.sh -f <config_file> -s"
      echo "  -f  Path to the config file. Default is /opt/project/assets/config.json."
      echo "  -d  Run as a daemon. Default is false."
      echo "  -s  Sleep time in seconds. Default is 1."
      echo "  -h  Display this help."
      echo "Processable environment variables are: ${ENV_VARS[@]^^}"
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done


if [ -z "$CONFIG_FILE" ]; then
  echo "Config file does not exists $CONFIG_FILE."
  exit 1
fi

cp $CONFIG_FILE $TEMP_FILE

LAST_HASH=""

if [ "$RUN_AS_DAEMON" == "true" ]; then
  echo "Processing environment variables to $CONFIG_FILE started as a service. Refreshing every $SLEEP_SECONDS seconds."
else
  echo "Processing environment variables to $CONFIG_FILE."
fi


while true; do
  CURRENT_HASH=""
  for VAR in "${ENV_VARS[@]}"; do
    VALUE=$(printenv ${VAR^^})
    if [ -n "$VALUE" ]; then
      CURRENT_HASH="$CURRENT_HASH$VALUE"
    fi
  done

  if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file $CONFIG_FILE does not exists. Please check the path."
  elif [ -z "$CURRENT_HASH" ] ; then
    if ! cmp -s "$TEMP_FILE" "$CONFIG_FILE"; then
      echo "Environment variables are empty. Restoring $CONFIG_FILE from backup."
      cp $TEMP_FILE $CONFIG_FILE
    fi
  elif [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
    for VAR in "${ENV_VARS[@]}"; do
      VALUE=$(printenv ${VAR^^})
      if [ -n "$VALUE" ]; then
        jq --indent 2 --arg val "$VALUE" --arg variable "$VAR" '.[$variable] = $val' $CONFIG_FILE > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" $CONFIG_FILE
      fi
    done
    echo "$CONFIG_FILE has been updated with environment variables. New content:"
    cat $CONFIG_FILE

    LAST_HASH=$CURRENT_HASH
  fi

  if [ "$RUN_AS_DAEMON" == "true" ]; then
    sleep $SLEEP_SECONDS
  else
    break
  fi
done
