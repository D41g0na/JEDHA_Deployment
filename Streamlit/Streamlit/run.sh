#docker build . -t getaround_image

docker run -it \
-v "$(pwd):/home/app" \
-p $PORT:$PORT \
-e PORT=$PORT \
getaround_image