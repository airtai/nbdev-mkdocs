#!/bin/bash

AIRT_DOCKER=ghcr.io/airtai/airt-docker-dask-tf2

BRANCH=$(git branch --show-current)
if [ "$BRANCH" == "main" ]
then
    TAG=latest
elif [ "$BRANCH" == "dev" ]
then
    TAG=dev
else
    if [ "$(docker image ls -q $AIRT_DOCKER:$BRANCH)" == "" ]
    then
        TAG=dev
    else
        TAG=$BRANCH
    fi
fi
AIRT_DOCKER=$AIRT_DOCKER:$TAG

if test -z "$AIRT_JUPYTER_PORT"
then
      echo 'AIRT_JUPYTER_PORT variable not set, setting to 8888'
      export AIRT_JUPYTER_PORT=8888
else
    echo AIRT_JUPYTER_PORT variable set to $AIRT_JUPYTER_PORT
fi

if test -z "$AIRT_TB_PORT"
then
      echo 'AIRT_TB_PORT variable not set, setting to 6006'
      export AIRT_TB_PORT=6006
else
    echo AIRT_TB_PORT variable set to $AIRT_TB_PORT
fi

if test -z "$AIRT_DASK_PORT"
then
      echo 'AIRT_DASK_PORT variable not set, setting to 8787'
      export AIRT_DASK_PORT=8787
else
    echo AIRT_DASK_PORT variable set to $AIRT_DASK_PORT
fi

if test -z "$AIRT_DOCS_PORT"
then
      echo 'AIRT_DOCS_PORT variable not set, setting to 4000'
      export AIRT_DOCS_PORT=4000
else
    echo AIRT_DOCS_PORT variable set to $AIRT_DOCS_PORT
fi

if test -z "$AIRT_DATA"
then
      echo 'AIRT_DATA variable not set, setting to current directory'
      export AIRT_DATA=`pwd`
fi
echo AIRT_DATA variable set to $AIRT_DATA

if test -z "$AIRT_PROJECT"
then
      echo 'AIRT_PROJECT variable not set, setting to current directory'
      export AIRT_PROJECT=`pwd`
fi
echo AIRT_PROJECT variable set to $AIRT_PROJECT

if test -z "$AIRT_GPU_PARAMS"
then
      echo 'AIRT_GPU_PARAMS variable not set, setting to all GPU-s'
      export AIRT_GPU_PARAMS="--gpus all"
fi
echo AIRT_GPU_PARAMS variable set to $AIRT_GPU_PARAMS

if test -z "$AZURE_SUBSCRIPTION_ID"
then
      echo 'AZURE_SUBSCRIPTION_ID variable not set'
      export AZURE_SUBSCRIPTION_ID=""
else
    echo AZURE_SUBSCRIPTION_ID variable set to $AZURE_SUBSCRIPTION_ID
fi

if test -z "$AZURE_TENANT_ID"
then
      echo 'AZURE_TENANT_ID variable not set'
      export AZURE_TENANT_ID=""
else
    echo AZURE_TENANT_ID variable set to $AZURE_TENANT_ID
fi

if test -z "$AZURE_CLIENT_ID"
then
      echo 'AZURE_CLIENT_ID variable not set'
      export AZURE_CLIENT_ID=""
else
    echo AZURE_CLIENT_ID variable set to $AZURE_CLIENT_ID
fi

if test -z "$AZURE_CLIENT_SECRET"
then
      echo 'AZURE_CLIENT_SECRET variable not set'
      export AZURE_CLIENT_SECRET=""
else
    echo AZURE_CLIENT_SECRET variable set to $AZURE_CLIENT_SECRET
fi


echo Using $AIRT_DOCKER
docker image ls $AIRT_DOCKER

if `which nvidia-smi`
then
	echo INFO: Running docker image with: $AIRT_GPU_PARAMS
	nvidia-smi -L
	export GPU_PARAMS=$AIRT_GPU_PARAMS
else
	echo INFO: Running docker image without GPU-s
	export GPU_PARAMS=""
fi

docker run --rm $GPU_PARAMS -u $(id -u):$(id -g) \
    --security-opt label=disable \
    -e JUPYTER_CONFIG_DIR=/root/.jupyter \
    -p $AIRT_JUPYTER_PORT:8888 -p $AIRT_TB_PORT:6006 -p $AIRT_DASK_PORT:8787 -p $AIRT_DOCS_PORT:4000 \
    -v $AIRT_DATA:/work/data -v $AIRT_PROJECT:/tf/nbdev-mkdocs \
    -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /etc/sudoers:/etc/sudoers -v /etc/shadow:/etc/shadow \
    -v $HOME/.ssh:$HOME/.ssh -v $HOME/.gitconfig:/root/.gitconfig -v $HOME/.aws:/root/.aws \
    -w /tf/nbdev-mkdocs \
    -e USER=$USER -e USERNAME=$USERNAME \
    -e AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID -e AZURE_TENANT_ID=$AZURE_TENANT_ID \
    -e AZURE_CLIENT_ID=$AZURE_CLIENT_ID -e AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
    $AIRT_DOCKER
