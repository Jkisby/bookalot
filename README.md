# Bookalot

## Running the Bookalot app

To run bookalot, you need Vagrant and VirtualBox installed.
[Vagrant](https://www.vagrantup.com/) and 
[VirtualBox](https://www.virtualbox.org/wiki/Downloads). 
Run vagrant from the vagrant folder with 'vagrant up', then login with 'vagrant ssh'. Next navigate to the bookalot folder with cd /vagrant/bookalot. use:
python databse_setup.py - to setup a new database for the app.
python populate_db - populates the db with some premade data.
python project.py - Launches the Flask webserver application on the virtual machine.

With the app running, you can access it on your webbrowser at http://localhost:5000

