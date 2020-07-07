## Overview

This project demonstrates
- streaming of tweets (twitter_app.py)
- processing of streamed tweets using Spark (spark_app.py)
- storing processed tweets into SQLite (database_app.py)

## Installation (Docker)

#### Step 1
Spin up GCE instance (Container Optimized OS)

#### Step 2
SSH into instance and clone project
```
git clone https://github.com/randy-chng/demo_pyspark_streaming.git
```

#### Step 3
Build image and provide Twitter details [W], [X], [Y] and [Z]
```
cd demo_pyspark_streaming
docker image build --tag streaming_pipeline_i --build-arg access_token=[W] --build-arg access_secret=[X] --build-arg consumer_key=[Y] --build-arg consumer_secret=[Z] --file Dockerfile .
```

#### Step 4
Run created image
```
docker run --name streaming_pipeline_c --publish 5555:5555 -di streaming_pipeline_i
```

#### Step 5
Access created container
```
docker exec -it streaming_pipeline_c /bin/bash
```

#### Step 6
Run following commands to start pipeline
```
nohup python -u twitter_app.py > twitter_app_output.log 2>&1 &
nohup python -u spark_app.py > spark_app_output.log 2>&1 &
```

## Query SQLite via Jupyter

For sample output, refer to notebook.ipynb

#### Step 1
Access created container
```
docker exec -it streaming_pipeline_c /bin/bash
```

#### Step 2
Run following commands to start jupyterlab
```
jupyter lab --ip=0.0.0.0 --port=5555 --allow-root
```

#### Step 3
Visit provided link using local web browser
- http://127.0.0.1:5555/?token=[SOME RANDOM GENERATED TOKEN VALUE]
