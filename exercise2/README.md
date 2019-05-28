

### Specification:
Create two Service Unit files to start a Redis and Memcached docker container on an AWS ECS or EKS cluster

Even though the brief requested a Redis and Memcache setup using ECS or EKS I took the decision
to use a managed AWS elasticache solution. These in my opinion are a much simpler and neater solution. Amazon spend a great deal of time and 
resource developing and fine tuning managed services for customers to consume.

N.B should the customer require an ECS or EKS solution for reasons that aren't clear from the brief then this of course 
can be achieved.

Should this be required and persistent storage be required you'd need to setup and configure ECS outside of AWS fargate. 
_Fargate Task storage is ephemeral_. Further documentation can be seen
[here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-volumes.html)


### Solutions:

Below you an see the 2 AWS cli commands i used to spin up each cache. These cluster can then be fully managed using 
automation and built in to pipeline should you wish.

Please note these are very simple setups, should you require these cluster to be access from outside the VPC then numerous
other steps and security considerations will be involved:

### AWS managed Redis Cache:
Lets spin up a single node replication redis cluster in AWS Elasticache:

`aws elasticache create-replication-group \
                            --replication-group-id my-redis-cluster \
                            --replication-group-description "Demo cluster" \
                            --num-cache-clusters 1 \
                            --cache-node-type cache.t2.small \
                            --cache-parameter-group default.redis3.2 \
                            --engine redis \
                            --engine-version 3.2.4`
                            
### AWS managed Memcached Cache:  
Lets spin up a single node replication memcache cluster in AWS Elasticache:
                    
`aws elasticache create-cache-cluster \
                            --cache-cluster-id my-memcached \
                            --cache-node-type cache.t2.small \
                            --engine memcached \
                            --engine-version 1.4.24 \
                            --cache-parameter-group default.memcached1.4 \
                            --num-cache-nodes 1`
                            
## Populating Data:
Please see `redis_dummydata.py` this is a simple python script to add a key/value set to the local running redis cache.

It requires the python redis module to be installed (best practice please use python virtual environments
to install)

This script will connect to a localhost on port 6379 and will write a key "hello" and a value of "World" <date time stamp>

Example Entry:

```
127.0.0.1:6379> GET Hello

"World 2019-05-28 16:45:49.031447"
```