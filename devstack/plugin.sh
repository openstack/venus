# plugin.sh - DevStack plugin.sh dispatch script venus

# Support potential entry-points console scripts in VENV or not
if [[ ${USE_VENV} == True ]]; then
  PROJECT_VENV["venus"]=${VENUS_DIR}.venv
  VENUS_BIN_DIR=${PROJECT_VENV["venus"]}/bin
else
  VENUS_BIN_DIR=$(get_python_exec_prefix)
fi

FILES=$VENUS_DIR/devstack/files

function install_venus() {
  setup_develop "$VENUS_DIR" openstack
  install_fluentd
  install_elastic_search
}

function init_venus() {
  venus_create_accounts

  recreate_database venus utf8
  sudo $VENUS_BIN_DIR/venus-manage --config-file=${VENUS_CONF} db sync
}

function configure_venus() {
  # Create venus conf directory
  sudo install -d -o $STACK_USER -m 755 $VENUS_CONF_DIR

  # Copy init conf file
  sudo cp -R $VENUS_DIR/etc/venus/* $VENUS_CONF_DIR

  iniset $VENUS_CONF keystone_authtoken memcached_servers localhost:11211
  iniset $VENUS_CONF keystone_authtoken username venus
  iniset $VENUS_CONF keystone_authtoken password "$ADMIN_PASSWORD"
  iniset $VENUS_CONF keystone_authtoken auth_url "http://$HOST_IP/identity"

  iniset $VENUS_CONF DEFAULT my_ip "$HOST_IP"
  iniset $VENUS_CONF DEFAULT osapi_venus_listen_port 10010

  iniset $VENUS_CONF database connection mysql+pymysql://root:"$DATABASE_PASSWORD"@localhost:3306/venus?charset=utf8

  iniset $VENUS_CONF elasticsearch url http://localhost:9200
}

function start_venus() {
  run_process venus-api "$VENUS_BIN_DIR/venus-api"
}

function install_elastic_search() {
  echo_summary "install elastic search"
  local FLUENTD_SERVICE="elasticsearch.service"
  if [[ is_ubuntu ]]; then
    install_package openjdk-8-jdk

    ES_VERSION=${ES_VERSION:-5.6.16}
    ES_DOWNLOAD_URL=${ES_DOWNLOAD_URL:-https://artifacts.elastic.co/downloads/elasticsearch}
    ES_DOWNLOAD_FILE="elasticsearch-$ES_VERSION.deb"

    if [[ ! -f $FILES/$ES_DOWNLOAD_FILE ]]; then
      sudo wget --progress=dot:giga -t 2 -c $ES_DOWNLOAD_URL/$ES_DOWNLOAD_FILE -O $FILES/$ES_DOWNLOAD_FILE
      if [[ $? -ne 0 ]]; then
        die "$ES_DOWNLOAD_FILE could not be downloaded"
      fi
    fi

    sudo dpkg -i $FILES/$ES_DOWNLOAD_FILE
    $SYSTEMCTL daemon-reload
    $SYSTEMCTL enable $FLUENTD_SERVICE
    $SYSTEMCTL start $FLUENTD_SERVICE
  else
    exit_distro_not_supported "install elastic search"
  fi
}

function install_fluentd() {
  echo_summary "install fluentd"
  if [[ is_ubuntu ]]; then
    FLUENTD_VERSION=${FLUENTD_VERSION:-4.1.0-1_amd64}
    FLUENTD_DOWNLOAD_URL=${FLUENTD_DOWNLOAD_URL:-http://packages.treasuredata.com.s3.amazonaws.com/4/ubuntu/bionic/pool/contrib/t/td-agent}
    FLUENTD_DOWNLOAD_FILE="td-agent_$FLUENTD_VERSION.deb"

    if [[ ! -f $FILES/$FLUENTD_DOWNLOAD_FILE ]]; then
      sudo wget --progress=dot:giga -t 2 -c $FLUENTD_DOWNLOAD_URL/$FLUENTD_DOWNLOAD_FILE -O $FILES/$FLUENTD_DOWNLOAD_FILE
      if [[ $? -ne 0 ]]; then
        die "$FLUENTD_DOWNLOAD_FILE could not be downloaded"
      fi
    fi

    sudo dpkg -i $FILES/$FLUENTD_DOWNLOAD_FILE
  else
    exit_distro_not_supported "install fluentd"
  fi

  # Create log dir
  VENUS_LOG_DIR="/var/log/kolla"
  sudo install -d -o $STACK_USER -m 777 $VENUS_LOG_DIR

  # Copy fluentd conf
  sudo cp -R $VENUS_DIR/devstack/fluentd-conf/* /etc/td-agent
  $SYSTEMCTL restart td-agent
}

function venus_create_accounts() {
  create_service_user "venus"
}

function uninstall_elastic_search() {
  local ELASTIC_SEARCH_SERVICE="elasticsearch.service"
  $SYSTEMCTL stop $ELASTIC_SEARCH_SERVICE
  $SYSTEMCTL disable $ELASTIC_SEARCH_SERVICE
  $SYSTEMCTL daemon-reload
  sudo dpkg -r elasticsearch
}

function uninstall_fluentd() {
  local FLUENTD_SERVICE="td-agent.service"
  $SYSTEMCTL stop $FLUENTD_SERVICE
  $SYSTEMCTL disable $FLUENTD_SERVICE
  $SYSTEMCTL daemon-reload
  sudo dpkg -r td-agent
}

# check for service enabled
if is_service_enabled venus-api; then

  if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
    # Set up system services
    echo_summary "Configuring system services venus"
    echo_summary "Welcome to Venus!"

  elif [[ "$1" == "stack" && "$2" == "install" ]]; then
    # Perform installation of service source
    echo_summary "Installing venus"
    install_venus

  elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    # Configure after the other layer 1 and 2 services have been configured
    echo_summary "Configuring venus"
    configure_venus

  elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
    # Initialize and start the venus service
    echo_summary "Initializing venus"
    init_venus
    start_venus
  fi

  if [[ "$1" == "unstack" ]]; then
    # Shut down venus services
    # no-op
    :
  fi

  if [[ "$1" == "clean" ]]; then
    # Remove state and transient data
    # Remember clean.sh first calls unstack.sh
    # no-op
    uninstall_elastic_search
    uninstall_fluentd
    sudo rm -rf $VENUS_CONF_DIR
  fi
fi
