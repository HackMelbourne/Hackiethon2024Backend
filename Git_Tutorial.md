# Git Tutorial 

Note that this assumes you have python and a code editor (Eg. vscode downloaded), and a github account. 

## Downloading Git 
First you will need to download Git onto your computer... 
You can do so through this [Git Download Link](https://git-scm.com/downloads)

## Configuring Git 
After installing Git onto your computer, you will need to configure it with your name and email address
```
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```
Replace "Your Name" with your name and "your_email@example.com" with your email address.
This information is included in the commit metadata and helps identify who made a particular change in your project.

## Initializing a Git Repository
To start version controlling your project, navigate to your project's directory (folder) using the terminal and run:
```
git init
```
This creates a new Git repository in your project directory. Make sure you are in the directory (folder) that you are planning to work in for the whole project. 

## Adding files to your Repository

To add files to the staging area (the area where changes to files are prepared to be committed), you can use:
```
git add filename
```
Or if you want to add all of them at once, you can use:
```
git add .
```
## Committing a change to the repository 
Once you have added the files, you need to commit them to "save them',
```
git commit -m "Your commit message here"
```
Your message should be a brief description of the changes you have made to the project since the last commit.

## Branches
Branches in Git allow you to work on different features or bug fixes without affecting the main codebase. To create a new branch, you can use:
```
git branch new_branchname
```
Great, you have created a new branch, however you need to switch to that branch before you make any changes... to do so, use: 
```
git checkout new_branchname
```

## Cloning a repository
Cloning creates a local copy of a remote repository on your machine. 
This allows you to work on the project locally, make changes, and contribute back to the project by pushing your changes to the remote repository.
Ensure that you are in the working directory that you want to clone the online repository to. 

To get the repository_url, 

1. Navigate to the repository you want to clone 
2. Click the code button...
3. Copy the URL for the repository.

and then you have it, now to clone a repository you can use: 
```
git clone repository_url
```

## Forking a Repository 
Forking involves creating a copy of a repository on your GitHub account. This allows you to freely experiment with changes without affecting the original repository. 
You will need to fork a repository for this project... 

Here's how you can fork a repository:
1. Visit the Repository: Go to the repository you want to fork on GitHub.
2. Fork: Click on the "Fork" button at the top right corner of the repository page. This creates a copy of the repository under your GitHub account.

Great you have forked the repository onto ur account, now you need to clone it so you can make changes locally.
To do so,
1. Navigate to the forked repository on your github account,
2. Click the code button...
3. Copy the URL for the repository.
4. Go to the git bash
5. Type git clone, and then paste the URL you copied earlier. It will look like this, with your GitHub username instead of YOUR-USERNAME

Eg. 
```
git clone https://github.com/YOUR-USERNAME/repository_name
```

## Pushing changes to a Remote repository
So far you have been working locally and haven't made your changes accessible to others for collaboration. To make your changes available, you need to push them to a remote repository. 
It's important to push your changes regularly to keep your remote repository up-to-date with your local changes.

Note you will have to get the link of the repository you want to push the changes to before you do this.

To push your changes, use: 
```
git remote add origin remote_repository_url 
```
And then, do:
```
git push -u origin branchname
```
Where branchname is the branch you want to push to. 
and origin is the name of remote repository name. 


## Checking Status / logs in Git 
Git has a command to check the status of your files, you can do so with the following: 
```
git status
```
This will show you which files are modified, which files are staged for commit, and which files are untracked.

If you want to check the a list of the commits that have been used, you can use:
```
git log
```
