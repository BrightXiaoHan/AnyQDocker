# Project configure script
BUILD=$ANYQ_HOME/build  # build folder for anyq project
CWD=$(dirname $(readlink -f "$0"))

cd $BUILD
# start solr engine
source /etc/profile
bash solr_script/solr_deply.sh start solr-4.10.3-anyq 8900

# clear schema
python solr_script/solr_api.py clear_doc localhost collection1 8900

# re-configure schema
# python solr_script/solr_api.py set_schema localhost collection1 $CWD/schema_format 8900
python solr_script/solr_api.py set_schema localhost collection1 $CWD/add_robot_id 8900
python solr_script/solr_api.py set_schema localhost collection1 $CWD/add_answer_id 8900

# update retrieval.conf
rm -rf example/conf/retrieval.conf
cp $CWD/retrieval.conf example/conf
rm -rf example/conf/rank.conf
cp $CWD/rank.conf example/conf

# sleep 10 seconds for ready
sleep 10