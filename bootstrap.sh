sudo docker run --net=host -d -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana grafana/grafana
sudo docker run -d -p 8086:8086 --privileged -v $PWD:/var/lib/influxdb influxdb
