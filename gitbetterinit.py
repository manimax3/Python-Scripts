#!/usr/bin/env python3

import keyring
import click
import os
import license
import requests
from datetime import date
from getpass import getpass
import github3 as gh


def create_license(l, name, email, year):
    li = license.find(l)

    if name is None:
        name = click.prompt("Enter your name for the license")

    if email is None:
        email = click.prompt("Enter your email for the license")

    with open("LICENSE", "w") as f:
        f.write(li.render(name=name, email=email, year=year))
        f.write("\n")


def create_gitignore(tags, extra):
    gitignore = ""

    if len(tags) > 0:
        gitignore = requests.get(
            "https://www.gitignore.io/api/{}".format(",".join(tags)))
        gitignore = gitignore.text

    with open(".gitignore", "w") as f:
        f.write(gitignore)
        f.write("\n")

        for e in extra:
            f.write(e)
            f.write("\n")


def gitinit(name, extra):
    if extra is not None:
        os.system("git init {1} {0}".format(name, extra))
    else:
        os.system("git init {}".format(name))


def github_repo(name):
    username = keyring.get_password("gitbetterinit", "username")
    password = keyring.get_password("gitbetterinit", "password")

    if username is None:
        username = click.prompt("Enter your github username")
        keyring.set_password("gitbetterinit", "username", username)

    if password is None:
        password = getpass("Enter your github password")
        keyring.set_password("gitbetterinit", "password", password)

    github = gh.login(username=username, password=password)
    repo = github.create_repository(name)

    os.system("git remote add origin {}".format(repo.ssh_url))


def get_licenses_list():
    return [l.id for l in license.iter()]


@click.command()
@click.option("--license", "-l", help="Add a license to the repo", type=click.Choice(get_licenses_list()))
@click.option("--autoignore", "-a", type=click.STRING, help="Tags for autogenerating a ignore file", multiple=True)
@click.option("--ignore", "-i", multiple=True, help="Other appends to the .gitignore file")
@click.option("--gitextra", "-g", help="Gets forwarded to git init", default=None, type=click.STRING)
@click.option("--github", help="Create a repo on github", default=False, is_flag=True)
@click.option("--name", "-n", help="The users name. Used for the license", type=click.STRING, default=None)
@click.option("--email", "-e", help="Used for the license", type=click.STRING, default=None)
@click.option("--year", "-y", help="Used for the license", default=str(date.today().year))
@click.option("--noinit", default=False, is_flag=True)
@click.argument("reponame")
def main(license, autoignore, github, ignore, gitextra, reponame, name, email, year, noinit):

    if not noinit:
        gitinit(reponame, gitextra)

    os.chdir(reponame)

    if license is not None:
        create_license(license, name, email, year)

    if len(ignore) > 0 or len(autoignore) > 0:
        create_gitignore(autoignore, ignore)

    if github:
        github_repo(reponame)


if __name__ == "__main__":
    main()
