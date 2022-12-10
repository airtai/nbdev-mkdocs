#!/bin/bash
if test -z "$CI_REGISTRY_IMAGE"
then
        export CI_REGISTRY_IMAGE=ghcr.io/airtai/nbdev-mkdocs
fi

if test -z "$CI_COMMIT_REF_NAME"
then
        export CI_COMMIT_REF_NAME=$(git branch --show-current)
fi


if [[ $CI_COMMIT_REF_NAME == "main" ]]; then TAG=latest ; else TAG=$CI_COMMIT_REF_NAME ; fi;

export BASE=ubuntu:latest
export PYTHON=3.10

echo Building $CI_REGISTRY_IMAGE, with tag: $TAG
#docker build --build-arg BASE=$BASE --build-arg PYTHON=$PYTHON \
#    -t $CI_REGISTRY_IMAGE:`date -u +%Y.%m.%d-%H.%M.%S` -t $CI_REGISTRY_IMAGE:$TAG . \
#    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m -s CRITICAL,HIGH $CI_REGISTRY_IMAGE:$TAG \
#    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m --exit-code 1 --ignore-unfixed $CI_REGISTRY_IMAGE:$TAG


export CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE-cuda-11.2.1
export BASE=nvidia/cuda:11.2.1-cudnn8-runtime-ubuntu20.04
export PYTHON=3.9

echo Building $CI_REGISTRY_IMAGE, with tag: $TAG
docker build --build-arg BASE=$BASE --build-arg PYTHON=$PYTHON \
    -t $CI_REGISTRY_IMAGE:`date -u +%Y.%m.%d-%H.%M.%S` -t $CI_REGISTRY_IMAGE:$TAG . \
    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m -s CRITICAL,HIGH $CI_REGISTRY_IMAGE:$TAG \
    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m --exit-code 1 --ignore-unfixed $CI_REGISTRY_IMAGE:$TAG

