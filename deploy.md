### A1. Configure ECS profile, config
```buildoutcfg
$ ecs-cli configure profile --profile-name telle-ai-profile --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY

$ ecs-cli configure --cluster telle-ai-cluster --region us-east-1 --default-launch-type FARGATE --config-name telle-ai-config
```

### 1. Create an empty Cluster
```buildoutcfg
$ ecs-cli up --cluster-config telle-ai-config --ecs-profile telle-ai-profile
INFO[0000] Created cluster                               cluster=telle-ai region=us-east-1
INFO[0001] Waiting for your cluster resources to be created... 
INFO[0001] Cloudformation stack status                   stackStatus=CREATE_IN_PROGRESS
INFO[0062] Cloudformation stack status                   stackStatus=CREATE_IN_PROGRESS
VPC created: vpc-0d7147aac288cdf23
Subnet created: subnet-03290b95f9ce6223d
Subnet created: subnet-007797c8dd6f73f76
Cluster creation succeeded.
```

### 2. Create Security Group
```buildoutcfg
$ aws ec2 create-security-group --group-name "telle-ai-docker-group" --description "Telle AI FARGATE Docker Group" --vpc-id "vpc-0d7147aac288cdf23"
{
    "GroupId": "sg-08f475b7c1fdfbb75"
}

```


### 3. Create role 
```buildoutcfg
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
```


### 4. Create ecr repository
```buildoutcfg
$ aws ecr create-repository --repository-name telle-ai-daemon
```

### 5. Modify docker-compose.yml
```buildoutcfg
version: '3'
services:
  daemon:
    image: "548266678237.dkr.ecr.us-east-1.amazonaws.com/telle-ai-daemon"
    volumes:
      - /telle-ai-daemon
    networks:
      - telle-network
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
    networks:
      - telle-network
networks:
  telle-network:
    driver: bridge
```

### 6. Docker build image
```buildoutcfg
$ docker build -t telle-ai-daemon .
```

### 7. Attach tag
```buildoutcfg
$ docker tag telle-ai-daemon 548266678237.dkr.ecr.us-east-1.amazonaws.com/telle-ai-daemon

```

### 8. Login ECR
```buildoutcfg
$ $(aws ecr get-login --no-include-email --region us-east-1)WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /home/honglei/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

```

### 9. Docker push
```buildoutcfg
$ docker push 548266678237.dkr.ecr.us-east-1.amazonaws.com/telle-ai-daemon

The push refers to repository [548266678237.dkr.ecr.us-east-1.amazonaws.com/telle-ai-daemon]
a29b27a36563: Pushed 
e0ffb90e4063: Pushed 
404abaa59210: Pushed 
00fdcf218c5b: Pushed 
3cf4affcb0e1: Pushed 
739c456429ff: Pushed 
58785b7cbad4: Pushed 
020b9db2b86c: Pushed 
3cfaf6dad8b1: Pushed 
8b6dfe2e08a1: Pushed 
5133232c669f: Pushed 
30e8a3d88591: Pushed 
fd8fae5cd65a: Pushed 
6b68dfad3e66: Pushed 
cd7100a72410: Pushed 
latest: digest: sha256:afd9c88ce206c5d5a47e2e84f3cdb059ffae84d39b1a39e75aa576c46259de76 size: 3476


```

### 10. Create ecs-params.yml
```buildoutcfg
version: 1
task_definition:
  task_execution_role: ecsTaskExecutionRole  # This should be created above
  ecs_network_mode: awsvpc
  task_size:
    mem_limit: 0.5GB
    cpu_limit: 256
run_params:
  network_configuration:
    awsvpc_configuration:
      subnets:
        - "subnet-083f774bd55bc5d5a"  # Change it to the cluster subnet
        - "subnet-056abc38570d37666"
      security_groups:
        - "sg-0e3a05aa1381ead6b"   # Change it to respective security_group
      assign_public_ip: ENABLED
```

### 11. Deploy with ecs-cli compose
```buildoutcfg
$ ecs-cli compose --project-name telle-ai-stack service up --cluster-config telle-ai-config --cluster telle-ai-cluster
WARN[0000] Skipping unsupported YAML option for service...  option name=networks service name=redis
WARN[0000] Skipping unsupported YAML option for service...  option name=networks service name=daemon
INFO[0000] Using ECS task definition                     TaskDefinition="telle-ai-daemon:1"
INFO[0000] Updated ECS service successfully              desiredCount=1 force-deployment=false service=telle-ai-daemon
INFO[0000] Service status                                desiredCount=1 runningCount=1 serviceName=telle-ai-daemon
INFO[0000] ECS Service has reached a stable state        desiredCount=1 runningCount=1 serviceName=telle-ai-daemon

```

### 12. Check running containers in cluster
```buildoutcfg
$ ecs-cli ps --cluster telle-ai-cluster
Name                                         State    Ports                        TaskDefinition     Health
55f6ed11-5992-42de-ab35-1c8d27959bf4/daemon  RUNNING                               telle-ai-daemon:1  UNKNOWN
55f6ed11-5992-42de-ab35-1c8d27959bf4/redis   RUNNING  100.24.21.83:6379->6379/tcp  telle-ai-daemon:1  UNKNOWN

```

### 13. Clean up: stop containers
```buildoutcfg
$ ecs-cli compose --project-name telle-ai-stack \
service down --cluster-config telle-ai-config \
--cluster telle-ai-cluster

WARN[0000] Skipping unsupported YAML option for service...  option name=networks service name=redis
WARN[0000] Skipping unsupported YAML option for service...  option name=networks service name=daemon
INFO[0000] Updated ECS service successfully              desiredCount=0 force-deployment=false service=telle-ai-daemon
INFO[0000] Service status                                desiredCount=0 runningCount=1 serviceName=telle-ai-daemon
INFO[0016] Service status                                desiredCount=0 runningCount=0 serviceName=telle-ai-daemon
INFO[0016] (service telle-ai-daemon) has stopped 1 running tasks: (task 55f6ed11-5992-42de-ab35-1c8d27959bf4).  timestamp="2019-09-01 18:28:51 +0000 UTC"
INFO[0016] (service telle-ai-daemon) has reached a steady state.  timestamp="2019-09-01 18:29:02 +0000 UTC"
INFO[0016] ECS Service has reached a stable state        desiredCount=0 runningCount=0 serviceName=telle-ai-daemon
INFO[0016] Deleted ECS service                           service=telle-ai-daemon
INFO[0016] (service telle-ai-daemon) has reached a steady state.  timestamp="2019-09-01 18:29:02 +0000 UTC"
INFO[0016] ECS Service has reached a stable state        desiredCount=0 runningCount=0 serviceName=telle-ai-daemon

```

### 14. Clean up: remove cluster
```buildoutcfg
$ ecs-cli down --force --cluster-config telle-ai-config \
--cluster telle-ai-cluster
```