# Introduction #

This document will guide you through installation of Ochs. This is a preliminary document and will be refined.
This document assumes you are familiar with Django and have it installed. It also assumes you are familiar with using either the Terminal or command line (depending on your context/platform).


# Installation #

These instructions have been tested on Mac OS X 10.5.6. If you are on a different platform or on a version of Mac OS X prior to 10.5 you will also want to make sure you have Python 2.5 and Apache 2.x installed.

## Dependencies ##
First off, make sure you meet the base requirements to install Django and install Django.
More info on that at http://www.djangoproject.com

Secondly, if you are on a Mac, make sure you have the Developer tools installed. These are included free with your Mac on the install disc that came with it. If you don't have your install disc handy, you can sign up for a free Developer Connection account and download Xcode and the Developer Tools here: http://developer.apple.com/mac/

These tools include gcc which you'll need to build and install all the parts that make up PIL, which will make all of your images beautiful.

### Install PIL ###

**Mac OS X**
These instructions could be applied to other **nix type platforms, but for now this has only been tested on Mac OS X.**

First, install libjpeg:

Get the source: http://www.ijg.org/files/jpegsrc.v6b.tar.gz

Extract the archive.

Move inside the source directory in terminal. On the Mac you can open terminal, type cd followed by a space and then drag and drop the folder containing the libjpeg files onto the terminal window to quickly move you to that folder.

Once there, execute the following commands:
```
cp /usr/share/libtool/config.sub .
cp /usr/share/libtool/config.guess .
./configure --enable-shared
make
sudo mkdir -p /usr/local/include
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/local/lib
sudo mkdir -p /usr/local/man/man1
sudo make install
```
Install PIL:

Get PIL at: http://effbot.org/downloads/Imaging-1.1.6.tar.gz

Extract the archive.

Move inside the source directory as described above.

Open the setup.py file in the Imaging-1.1.6 folder, you can use TextEdit or your favorite text editor.
Change the following values in setup.py from the default None to:
```
JPEG_ROOT = "/usr/local/include"
ZLIB_ROOT = "/usr/local/include"
```
Check if everything is well configured by running these commands from within that folder, in terminal:
```
python setup.py build_ext -i
python selftest.py
```
If no errors are found and the required libraries are installed (like JPEG support), install PIL:
```
sudo python setup.py install
```

---


## Install ##

Open Terminal and go to a folder where you would like Ochs to live. A folder in your homespace should be fine for testing.

Now, you'll need to checkout the latest version of Ochs from our subversion repository.
From the Terminal, move to the folder you want Ochs to live, and enter this command:
```
svn checkout http://ochs.googlecode.com/svn/trunk/
```

This will copy all of the core files required to make the Ochs application work.

### Settings Modifications ###

Before we can run Ochs, we need to make a few quick changed to the settings.py file. So open the settings.py file in your favorite text editor and change the following lines:

```
IMAGE_UPLOAD_PATH = "contentdirectory"
```
_Where contentdirectory is the location you want to store media files._

```
IMAGE_FILE_PATH = "contentdirectory"
```
_Where contentdirectory is the location you expect to store other media files._

```
ADMINS = (
    ('Operations', 'errors@tnjn.com'),
)
```
_Optional: Change these to the name of and email address of the admin for your installation._

```
DATABASE_ENGINE = ''
```
_For testing on a local machine, put sqlite3 inside the single quotes._

```
DATABASE_NAME = ''
```
_Put a name for your database file inside the single quotes._

### Sync your Database and Test ###

Now that you've copied the Ochs app to your computer and modified the settings to be at least somewhat unique to you, you're ready to have Django create Ochs' tables for you.

From the terminal, within the root of Ochs (where we've been for most of this part of the tutorial) enter this command:

```
python manage.py syncdb
```

This will synchronize the structure of the models within Ochs to your database and create any tables that need creating. Keep in mind however, that this function will not create new columns in the tables, so if you were to add a "Gonzo Journalism" checkbox to the Story model after you had already created that table, you would then have to go back in later and manually add that column.

Next, we'll start out test server.
From the terminal, enter this command:

```
python manage.py runserver
```

You should now be able to go to your web browser of choice and entere into the address bar, http://127.0.0.1:8000/admin and you will now be in your Django Admin!