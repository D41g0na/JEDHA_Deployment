# Image build Widows
docker build . -t getaround_dashboard

# Create new app on Heroku
#heroku create getarounddashboard

# Login to Heroku
heroku container:login

# Tag the image
docker tag getaround_dashboard registry.heroku.com/getarounddashboard/web

# Push the image
docker push registry.heroku.com/getarounddashboard/web

# Release the image (activation du container)
heroku container:release web -a getarounddashboard 

# Open the app
heroku open -a getarounddashboard
