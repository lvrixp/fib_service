## Performance test ##

#### Concurrency 100, requests 10000, N: 100
    This is ApacheBench, Version 2.3 <$Revision: 1604373 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        Apache/2.4.10
    Server Hostname:        127.0.0.1
    Server Port:            80
    
    Document Path:          /fib/100
    Document Length:        1180 bytes
    
    Concurrency Level:      100
    Time taken for tests:   11.416 seconds
    Complete requests:      10000
    Failed requests:        1
       (Connect: 0, Receive: 0, Length: 1, Exceptions: 0)
    Total transferred:      13408659 bytes
    HTML transferred:       11798820 bytes
    Requests per second:    875.93 [#/sec] (mean)
    Time per request:       114.165 [ms] (mean)
    Time per request:       1.142 [ms] (mean, across all concurrent requests)
    Transfer rate:          1146.97 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.7      0       8
    Processing:    35  108 545.3     55    9158
    Waiting:        0   99 536.8     54    8652
    Total:         35  108 545.4     55    9158
    
    Percentage of the requests served within a certain time (ms)
      50%     55
      66%     60
      75%     76
      80%     81
      90%    107
      95%    125
      98%    163
      99%    502
     100%   9158 (longest request)
    
    
#### Concurrency 100, requests 10000, N: 1000
    This is ApacheBench, Version 2.3 <$Revision: 1604373 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        Apache/2.4.10
    Server Hostname:        127.0.0.1
    Server Port:            80
    
    Document Path:          /fib/1000
    Document Length:        105572 bytes
    
    Concurrency Level:      100
    Time taken for tests:   13.651 seconds
    Complete requests:      10000
    Failed requests:        8
       (Connect: 0, Receive: 0, Length: 8, Exceptions: 0)
    Non-2xx responses:      5
    Total transferred:      1056506435 bytes
    HTML transferred:       1054876879 bytes
    Requests per second:    732.54 [#/sec] (mean)
    Time per request:       136.511 [ms] (mean)
    Time per request:       1.365 [ms] (mean, across all concurrent requests)
    Transfer rate:          75579.78 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.8      0       9
    Processing:     0  132 579.0     76    9543
    Waiting:        0   89 548.2     12    9381
    Total:          1  132 579.0     76    9543
    
    Percentage of the requests served within a certain time (ms)
      50%     76
      66%    101
      75%    113
      80%    121
      90%    163
      95%    205
      98%    281
      99%   2936
     100%   9543 (longest request)

    
#### Concurrency 200, requests 10000, N: 10
    This is ApacheBench, Version 2.3 <$Revision: 1604373 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        Apache/2.4.10
    Server Hostname:        127.0.0.1
    Server Port:            80
    
    Document Path:          /fib/10
    Document Length:        51 bytes
    
    Concurrency Level:      200
    Time taken for tests:   13.138 seconds
    Complete requests:      10000
    Failed requests:        0
    Total transferred:      2100000 bytes
    HTML transferred:       510000 bytes
    Requests per second:    761.14 [#/sec] (mean)
    Time per request:       262.764 [ms] (mean)
    Time per request:       1.314 [ms] (mean, across all concurrent requests)
    Transfer rate:          156.09 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   15 121.8      0    3005
    Processing:     7  206 929.1    136   13122
    Waiting:        7  205 929.1    136   13122
    Total:         16  220 937.2    136   13134
    
    Percentage of the requests served within a certain time (ms)
      50%    136
      66%    137
      75%    138
      80%    139
      90%    142
      95%    145
      98%    966
      99%   1137
     100%  13134 (longest request)
    
    
