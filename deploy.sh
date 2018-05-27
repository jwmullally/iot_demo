#!/bin/sh
set -ex

echo "Creating test stack in current OpenShift project..."

oc apply -f kubeobjs
(cd device_endpoint && oc start-build device-endpoint --from-dir .)
(cd test_device && oc start-build test-device --from-dir .)
