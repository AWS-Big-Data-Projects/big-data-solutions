Kill all applications on YARN which are in ACCEPTED state:

for x in $(yarn application -list -appStates ACCEPTED | awk 'NR > 2 { print $1 }'); do yarn application -kill $x; done

Kill all applications on YARN which are in RUNNING state:

for x in $(yarn application -list -appStates RUNNING | awk 'NR > 2 { print $1 }'); do yarn application -kill $x; done

Kill all SPARK applications on YARN:

for x in $(yarn application -list -appTypes SPARK | awk 'NR > 2 { print $1 }'); do yarn application -kill $x; done
