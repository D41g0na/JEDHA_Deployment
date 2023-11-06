# Image build Widows
docker build . -t mlflow-training

# Create new app on Heroku
heroku create mlflow-getaround

# Login to Heroku
heroku container:login

# Tag the image
docker tag mlflow-training registry.heroku.com/mlflow-getaround/web

# Push the image
docker push registry.heroku.com/mlflow-getaround/web

# Release the image (activation du container)
heroku container:release web -a mlflow-getaround

# Open the app
heroku open -a mlflow-getaround