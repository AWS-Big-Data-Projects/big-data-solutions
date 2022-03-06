#!/bin/bash
while true; do
NODEPROVISIONSTATE=` sed -n '/localInstance [{]/,/[}]/{
/nodeProvisionCheckinRecord [{]/,/[}]/ {
/status: / { p }
/[}]/a
}
/[}]/a
}' /emr/instance-controller/lib/info/job-flow-state.txt | awk ' { print $2 }'`

if [ "$NODEPROVISIONSTATE" == "SUCCESSFUL" ]; then
sleep 10;
echo "Running my post provision bootstrap"
# your code here

sudo docker exec jupyterhub bash -c "pip install tensorflow"

exit;
fi

sleep 10;
done
