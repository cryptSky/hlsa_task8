### Setup

1. Install docker
2. Install siege

## Steps to run

1. `docker-compose up --build` 
2. Data initiallization: connect to server container `docker exec -it server /bin/bash` and run `python generator.py`

## Results


#### No index and innodb_flush_log_at_trx_commit = 1
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`
```console
Transactions:                   8404 hits
Availability:                 100.00 %
Elapsed time:                  59.34 secs
Data transferred:               0.19 MB
Response time:                  0.70 secs
Transaction rate:             141.62 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.38
Successful transactions:        8404
Failed transactions:               0
Longest transaction:            0.78
Shortest transaction:           0.08
```

#### No index and innodb_flush_log_at_trx_commit = 0
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                   8708 hits
Availability:                 100.00 %
Elapsed time:                  59.11 secs
Data transferred:               0.20 MB
Response time:                  0.67 secs
Transaction rate:             147.32 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.38
Successful transactions:        8708
Failed transactions:               0
Longest transaction:            0.81
Shortest transaction:           0.17
```

#### No index and innodb_flush_log_at_trx_commit = 2
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9000 hits
Availability:                 100.00 %
Elapsed time:                  59.26 secs
Data transferred:               0.21 MB
Response time:                  0.65 secs
Transaction rate:             151.87 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.43
Successful transactions:        9000
Failed transactions:               0
Longest transaction:            0.75
Shortest transaction:           0.15
```

#### BTREE index on birthdate and innodb_flush_log_at_trx_commit = 2
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9171 hits
Availability:                 100.00 %
Elapsed time:                  59.24 secs
Data transferred:               0.21 MB
Response time:                  0.64 secs
Transaction rate:             154.81 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.42
Successful transactions:        9171
Failed transactions:               0
Longest transaction:            0.77
Shortest transaction:           0.04
```

#### BTREE index on birthdate and innodb_flush_log_at_trx_commit = 1
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9091 hits
Availability:                 100.00 %
Elapsed time:                  59.33 secs
Data transferred:               0.21 MB
Response time:                  0.65 secs
Transaction rate:             153.23 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.42
Successful transactions:        9091
Failed transactions:               0
Longest transaction:            0.98
Shortest transaction:           0.31
```

#### BTREE index on birthdate and innodb_flush_log_at_trx_commit = 0
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9413 hits
Availability:                 100.00 %
Elapsed time:                  59.63 secs
Data transferred:               0.22 MB
Response time:                  0.63 secs
Transaction rate:             157.86 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.43
Successful transactions:        9413
Failed transactions:               0
Longest transaction:            0.94
Shortest transaction:           0.22
```

#### HASH index on birthdate and innodb_flush_log_at_trx_commit = 0
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9377 hits
Availability:                 100.00 %
Elapsed time:                  59.42 secs
Data transferred:               0.21 MB
Response time:                  0.63 secs
Transaction rate:             157.81 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.44
Successful transactions:        9377
Failed transactions:               0
Longest transaction:            0.97
Shortest transaction:           0.30
```

#### HASH index on birthdate and innodb_flush_log_at_trx_commit = 1
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   8849 hits
Availability:                 100.00 %
Elapsed time:                  59.46 secs
Data transferred:               0.20 MB
Response time:                  0.67 secs
Transaction rate:             148.82 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.36
Successful transactions:        8849
Failed transactions:               0
Longest transaction:            1.20
Shortest transaction:           0.27
```

#### HASH index on birthdate and innodb_flush_log_at_trx_commit = 2
`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}`

```console
Transactions:                   9107 hits
Availability:                 100.00 %
Elapsed time:                  59.90 secs
Data transferred:               0.21 MB
Response time:                  0.65 secs
Transaction rate:             152.04 trans/sec
Throughput:                     0.00 MB/sec
Concurrency:                   99.47
Successful transactions:        9107
Failed transactions:               0
Longest transaction:            0.77
Shortest transaction:           0.17
```

### EXPLAIN

#### No index 

```console
mysql> explain select count(*) from user where birthdate < "1990-05-05";
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+
|  1 | SIMPLE      | user  | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 7498505 |    33.33 | Using where |
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+
1 row in set, 1 warning (0.00 sec)

mysql> select count(*) from user where birthdate < "1990-05-05";
+----------+
| count(*) |
+----------+
|  3308886 |
+----------+
1 row in set (4.47 sec)

```

#### BTREE

```console
mysql> explain select count(*) from user where birthdate < "1990-05-05";
+----+-------------+-------+------------+-------+---------------+-------------+---------+------+---------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys | key         | key_len | ref  | rows    | filtered | Extra                    |
+----+-------------+-------+------------+-------+---------------+-------------+---------+------+---------+----------+--------------------------+
|  1 | SIMPLE      | user  | NULL       | range | btree_index   | btree_index | 3       | NULL | 3749252 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+-------------+---------+------+---------+----------+--------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> select count(*) from user where birthdate < "1990-05-05";
+----------+
| count(*) |
+----------+
|  3308886 |
+----------+
1 row in set (0.80 sec)
```

#### HASH

```console
mysql> explain select count(*) from user where birthdate < "1990-05-05";
+----+-------------+-------+------------+-------+---------------+---------------+---------+------+---------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys | key           | key_len | ref  | rows    | filtered | Extra                    |
+----+-------------+-------+------------+-------+---------------+---------------+---------+------+---------+----------+--------------------------+
|  1 | SIMPLE      | user  | NULL       | range | bd_index_hash | bd_index_hash | 3       | NULL | 3753856 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+---------------+---------+------+---------+----------+--------------------------+
1 row in set, 2 warnings (0.00 sec)

mysql> select count(*) from user where birthdate < "1990-05-05";
+----------+
| count(*) |
+----------+
|  3308886 |
+----------+
1 row in set (0.63 sec)
```


