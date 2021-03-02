BUILD=$ANYQ_HOME/build  # build folder for anyq project

source /etc/profile

pushd $BUILD
bash solr_script/solr_deply.sh start solr-4.10.3-anyq 8900
nohup ./run_server > run_server.log 2>&1 &
popd

export PYTHONPATH="$PYTHONPATH:./src"
python3 src/solr_server.py