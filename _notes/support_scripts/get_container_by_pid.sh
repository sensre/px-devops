docker ps -q | xargs docker inspect --format '{{.State.Pid}}, {{.Name}}' | grep "%PID%"
