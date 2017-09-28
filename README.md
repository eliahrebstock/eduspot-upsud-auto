# Connection script to 'eduspot' wireless hotspot on Université Paris-Sud campus  #

Connection script to log faster to eduspot captive portal with GET and
POST requests to the right urls. This script works only on Université
Paris-Sud campus.

## Dependencies ##

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/master/)

_Also, you can use [pipenv](https://docs.pipenv.org/)._

## Usage ##

```
    $ upsud.py [-h] [-u USERNAME] [-p PASSWORD]
```

If no username or password is given to the script, it will be asked
during runtime.

* * *

# Script de connexion automatique à eduspot - Université Paris-Sud #

Script de connexion rapide au portail captif de eduspot en envoyant
des requêtes GET et POST aux bonnes urls. Ce script gère uniquement la
connexion sur le campus de l'université de Paris-Sud.

## Dépendances ##

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/master/)

_Vous pouvez aussi utiliser [pipenv](https://docs.pipenv.org/)._

## Utilisation ##

```
    $ upsud.py [-h] [-u USERNAME] [-p PASSWORD]
```

Si le nom d'utilisateur ou le mot de passe n'est pas donné au script,
il sera demandé à l'exécution.
