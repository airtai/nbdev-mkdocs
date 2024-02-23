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
export PYTHON=3.11

echo Building $CI_REGISTRY_IMAGE, with tag: $TAG
docker build --build-arg BASE=$BASE --build-arg PYTHON=$PYTHON \
    -t $CI_REGISTRY_IMAGE:$TAG .

