#Construire image
docker build . -t getaround_image

#Création de l'appli heroku
#heroku create getaround-dashboard-heroku

#Tag l'image docker à heroku
docker tag getaround_image registry.heroku.com/getaround-dashboard-heroku/web

#Push l'image docker à heroku
heroku container:push web -a getaround-dashboard-heroku

#Activation de l'appli heroku
heroku container:release web -a getaround-dashboard-heroku

#Ouvrir
heroku open -a getaround-dashboard-heroku