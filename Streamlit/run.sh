#docker build . -t getaround_image

docker run -it \
-v "$(pwd):/home/app" \

getaround_image