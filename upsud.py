#!/usr/bin/env python3
from bs4 import BeautifulSoup
import getpass
import requests
import argparse
import sys
import os

def connect(username, password):
    # Create a session to store all the needed cookies
    s = requests.session()
    # We have to change the User-Agent to trick JQuery Portal API
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'

    # First, let's try to connect to a sample website
    r = s.get('http://captive.apple.com')
    if 'Success' in r.text:
        print('Vous êtes déjà connecté à Internet !')
        exit(0)
    # If there is no 'Success', it means we have arrived on the
    # captive portal instead of the website we want

    # Get the CAS form (by posting to the school choice form)
    r = s.post('https://sso.u-psud.fr/wayf/WAYF?entityID=https://wifi.u-psud.fr/eduspot&return=https://wifi.u-psud.fr/Shibboleth.sso/shibauth.php?SAMLDS=1&target=cookie%3A17bc56e7', data={'user_idp': 'https://idp.u-psud.fr/idp', 'Select':'Sélection'})

    soup = BeautifulSoup(r.text, 'html.parser')

    urlpost = 'https://sso.u-psud.fr/' + soup.find(id='fm1')['action']

    inputs = soup.find_all('input')

    for i in inputs:
        if (i['name'] == 'lt'):
            lt = i['value']
        if (i['name'] == 'execution'):
            execution = i['value']

    # While authentication is not done
    while (True):
        if username:
            print("Username : " + username)
        # Ask for username if not given in parameter
        if not username:
            username = input("Nom d'utilisateur : ")
        # Ask for password if not given in parameter
        if not password:
            password = getpass.getpass('Entrez votre mot de passe u-psud.fr : ')

        payload = {'_eventId': 'submit', 'lt': lt, 'execution':execution, 'submit': 'SE CONNECTER', 'username': username, 'password': password}
        # Authentication to u-psud CAS
        j = s.post(urlpost, data=payload)
        soup = BeautifulSoup(j.text, 'html.parser')

        # Check if the authentication failed or not
        if soup.title and 'Paris-Sud' in soup.title.text:
            password = ''
        else:
            break

    print('Authentification réussie')

    # Completing form for redirection to captive portal
    soup = BeautifulSoup(j.text, 'html.parser')

    urlpost = soup.find('form')['action']

    t = {}
    for i in soup.findAll('input'):
        if i.get('name'):
            t[i['name']] = i['value']

    j = s.post(urlpost, data=t)

    # HACK : Connect to CAS again (with cookies) to generate a better redirection
    g = s.get('https://wifi.u-psud.fr/shibauth.php')

    # Init JQuery Portal API again
    payload = {'action': 'init', 'free_urls': ''}
    r = s.post('https://wifi.u-psud.fr/portal_api.php', data=payload)

    # Try to authenticate to JQuery Portal API
    payload = {'action': 'authenticate',
               'login': 'shibuser',
               'password': 'shibpwd',
               'policy_accept': True,
               'from_ajax': True}

    r = s.post('https://wifi.u-psud.fr/portal_api.php', data=payload)

    # Finally, make a test with a classic test website
    sys.stdout.write('Vérification de la connexion')
    r = s.get('http://captive.apple.com')
    if 'Success' in r.text:
        sys.stdout.write('\rVérification terminée : vous êtes connecté à eduspot !\n')

parser = argparse.ArgumentParser(description='Connect to eduspot.')
parser.add_argument('-u', '--username', help='Username of the user')
parser.add_argument('-p', '--password', help='Password of the user')
args = parser.parse_args()

try:
    connect(args.username, args.password)
except KeyboardInterrupt:
    print('\nInterrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
