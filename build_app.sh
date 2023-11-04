git add .
git commit -m "CaesarMaturity mostly works, slight error in deletion, need to improve testing slightly"
git push origin -f master:main
docker build -t palondomus/maturitybackend:latest .
docker push palondomus/maturitybackend:latest
docker run -it -p 8080:8080 palondomus/maturitybackend:latest
