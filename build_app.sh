git add .
git commit -m "$1"
git push origin -u main:main
docker build -t palondomus/maturitybackend:latest .
docker push palondomus/maturitybackend:latest
docker run -it -p 8080:8080 palondomus/maturitybackend:latest
