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

export TF_VERSION=2.12.0

export CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE-tensorflow-$TF_VERSION
export BASE=tensorflow/tensorflow:$TF_VERSION-gpu-jupyter

echo Building $CI_REGISTRY_IMAGE, with tag: $TAG
docker build --build-arg BASE=$BASE \
    -t $CI_REGISTRY_IMAGE:$TAG . \
    -f Dockerfile_tensorflow \
    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m -s CRITICAL,HIGH $CI_REGISTRY_IMAGE:$TAG \
    && trivy image --skip-files /usr/local/bin/git-secrets --no-progress --timeout 10m -s CRITICAL,HIGH --exit-code 1 --ignore-unfixed $CI_REGISTRY_IMAGE:$TAG

