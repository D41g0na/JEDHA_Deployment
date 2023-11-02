#Construire image
docker build . -t getaround_image

#Création de l'appli heroku
#heroku create getarounddashboard-heroku

#Tag l'image docker à heroku
docker tag getaround_image registry.heroku.com/getarounddashboard-heroku/web

#Push l'image docker à heroku
heroku container:push web -a getarounddashboard-heroku

#Activation de l'appli heroku
heroku container:release web -a getarounddashboard-heroku

#Ouvrir
heroku open -a getarounddashboard-heroku