# Swarm Service Monitor

The monitor service querries Docker for status of swarm services. If a high rate of churn (specifically, several rejected tasks) is detected in a service within a monitoring interval, the service is scaled down to 0. The monitoring script will keep track of task history beyond that of swarm's task history limit based on repeated snapshots of the state of services with replicated tasks.

## Sample Usage

The below invocation will monitor services and scale down a service to 0 if more than 70 tasks are rejected during a 60 second sampling period:

```
docker run -v /var/run/docker.sock:/var/run/docker.sock ddebroy/svc-monitor -t 70 -i 60
```

## Sample Output

```
$ docker run -v /var/run/docker.sock:/var/run/docker.sock ddebroy/svc-monitor -t 90 -i 60
Analyzing service: 2qga8i95wy4jsa33y0rlzfunm tracking 0 rejected tasks
Analyzing service: 4ljfk0khpt0nvbwwlipfg6gsf tracking 0 rejected tasks
Analyzing service: 7sl8bv6764047yx0sly0f6nzf tracking 0 rejected tasks
Analyzing service: k76bsgemwkmdelh31km27icxb tracking 0 rejected tasks
     found rejected task: 2hud7zacfsontefzuda7ox5ur in service: k76bsgemwkmdelh31km27icxb
     rejected tasks within last 60 seconds: 0
Analyzing service: lb884np424liwsc1v30pf8clh tracking 0 rejected tasks
     found rejected task: 1h89uktszqfqrvtczmb7y5shy in service: lb884np424liwsc1v30pf8clh
     .
     .
     .
     found rejected task: ziq9x753cdvoqvtnhvzs1llvf in service: lb884np424liwsc1v30pf8clh
     rejected tasks within last 60 seconds: 50
Analyzing service: osltfitgebubl9j667apvpwy6 tracking 0 rejected tasks
Analyzing service: k76bsgemwkmdelh31km27icxb tracking 1 rejected tasks
     found rejected task: 2hud7zacfsontefzuda7ox5ur in service: k76bsgemwkmdelh31km27icxb
    rejected tasks within last 60 seconds: 0
Analyzing service: osltfitgebubl9j667apvpwy6 tracking 0 rejected tasks
Analyzing service: k76bsgemwkmdelh31km27icxb tracking 1 rejected tasks
     found rejected task: 2hud7zacfsontefzuda7ox5ur in service: k76bsgemwkmdelh31km27icxb
     rejected tasks within last 60 seconds: 0
Analyzing service: lb884np424liwsc1v30pf8clh tracking 70 rejected tasks
     found rejected task: 2205x3ttsbnb635ay697mcvxy in service: lb884np424liwsc1v30pf8clh
     .
     .
     .
     found rejected task: ziq9x753cdvoqvtnhvzs1llvf in service: lb884np424liwsc1v30pf8clh
     rejected tasks within last 60 seconds: 80
Analyzing service: osltfitgebubl9j667apvpwy6 tracking 0 rejected tasks
Analyzing service: k76bsgemwkmdelh31km27icxb tracking 1 rejected tasks
     found rejected task: 2hud7zacfsontefzuda7ox5ur in service: k76bsgemwkmdelh31km27icxb
    rejected tasks within last 60 seconds: 0
Analyzing service: lb884np424liwsc1v30pf8clh tracking 80 rejected tasks
     found rejected task: 2205x3ttsbnb635ay697mcvxy in service: lb884np424liwsc1v30pf8clh
     .
     .
     .
     found rejected task: ziq9x753cdvoqvtnhvzs1llvf in service: lb884np424liwsc1v30pf8clh
     rejected tasks within last 60 seconds: 90
Analyzing service: osltfitgebubl9j667apvpwy6 tracking 0 rejected tasks
Analyzing service: k76bsgemwkmdelh31km27icxb tracking 1 rejected tasks
     found rejected task: 2hud7zacfsontefzuda7ox5ur in service: k76bsgemwkmdelh31km27icxb
     rejected tasks within last 60 seconds: 0
Analyzing service: lb884np424liwsc1v30pf8clh tracking 90 rejected tasks
     found rejected task: 2205x3ttsbnb635ay697mcvxy in service: lb884np424liwsc1v30pf8clh
     .
     .
     .
     found rejected task: yv8dqpc3u8qg2x0lpz68qh5ry in service: lb884np424liwsc1v30pf8clh
     rejected tasks within last 60 seconds: 100
     scale down service to zero:  lb884np424liwsc1v30pf8clh . 90 rejected tasks detected
```
