#!/bin/bash

export LEIN_ROOT=yes

APP_NAME='data-models'
CONTAINER="$ECR_PATH/$APP_NAME"

export ANSIBLE_HOST_KEY_CHECKING=false

function docker_login {
    { set +x; } 2>/dev/null
    login="$(aws ecr get-login --no-include-email --region ap-northeast-2)"
    ${login}
    set -x
}

function remove_containers {
    echo "remove existing containers"
    remove_existing_dockers
}

function test_application {
    :
}

function remove_existing_dockers {
    echo "remove dockers"
    docker rm -f $(docker ps -q -a) > /dev/null 2>&1 && echo 'All containers removed' || echo 'No containers to remove'
    docker rmi -f $(docker images -q) > /dev/null 2>&1 && echo 'All images removed' || echo 'No images to remove'
}

function build_containers {
    docker build \
    --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    -t ${CONTAINER} .
}

function tag_containers {
    push_containers "" "${BUILD_NUMBER}"
}

function promote_containers {
    echo "promote container ${BUILD_NUMBER} to green"
    docker pull ${CONTAINER}:${BUILD_NUMBER}
    push_containers "${BUILD_NUMBER}" "green"
}

function push_containers {
    from_suffix=$1
    tag_suffix=$2
    tag_name="$CONTAINER:$tag_suffix"

     if [ -z "$from_suffix" ]; then
        from_tag="$CONTAINER"
    else
        from_tag="${CONTAINER}:${from_suffix}"
    fi

    docker tag ${from_tag} ${tag_name}

    echo "push container: docker push $CONTAINER"
    docker push ${CONTAINER}
}

function ci {
  { set +x; } 2>/dev/null
  : "${TRAVIS_BRANCH:?is required to be set}"
  : "${TRAVIS_BUILD_NUMBER:?is required to be set}"
  set -x

  BRANCH=$TRAVIS_BRANCH
  BUILD_NUMBER=travis-$TRAVIS_BUILD_NUMBER
  IS_PR=$TRAVIS_PULL_REQUEST

  docker_login
  build_containers
  if [[ "$BRANCH" == "master" && "$IS_PR" == "false" ]]; then
    tag_containers
    promote_containers
  fi
}

if [[ "$1" == "--test" ]]; then
    test_application
elif [[ "$1" == "--remove" ]]; then
    remove_containers
elif [[ "$1" == "--build" ]]; then
    build_containers
elif [[ "$1" == "--publish" ]]; then
    tag_containers
elif [[ "$1" == "--promote" ]]; then
    promote_containers
elif [[ "$1" == "--teardown" ]]; then
    teardown_build
elif [[ "$1" == "--ci" ]]; then
    ci
fi
