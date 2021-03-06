#!/bin/bash -xe

# Clone test repo
git clone https://github.com/venicegeo/gwtest-integration.git

# Set maven paths
export M2_HOME=$PWD/apache-maven-3.2.2
export M2=$M2_HOME/bin
export PATH=$M2:$PATH

echo $PATH

geowave --version

which geowave

# Source env vars, before running test
source /mnt/geowave-env.sh

# Determine HBase vs. Accumulo
export db_type="hbase"

# Run tests
cd gwtest-integration/ci/Junit
mvn -B test
