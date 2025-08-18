#!/bin/bash

USER_VM=yc-user
HOST_VM=46.21.244.159
SSH_KEY=/home/aavdonin/.ssh/ssh_private_key
FOLDER=src
IMAGE_VM=$(ssh -i $SSH_KEY $USER_VM@$HOST_VM docker ps --format '{{.Names}}')
echo USER_VM $USER_VM
echo HOST_VM $HOST_VM
echo IMAGE_VM $IMAGE_VM
scp -ri $SSH_KEY $FOLDER $USER_VM@$HOST_VM:~/
ssh -i $SSH_KEY $USER_VM@$HOST_VM "
    docker cp ~/$FOLDER $IMAGE_VM:/lessons/
"