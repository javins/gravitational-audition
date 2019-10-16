#  be nice when asked to stop SIGTERM
cleanup() {
    echo "Terminated. Bye!"
    trap - SIGTERM SIGINT # clear the trap
    kill -s SIGTERM $$ # Forward SIGTERM to children
    exit 0
}

trap cleanup SIGTERM SIGINT

echo "Hello Gravitational!"
echo "Counting the seconds:"
while true
do
	date
	sleep 1
done
