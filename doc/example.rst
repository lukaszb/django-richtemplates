=====================
Using example project
=====================

------------
Introduction
------------

You don't need to install `richtemplates` in order to run boundled example
project located at `example_project` directory. In it's forged settings
module it tries to set special variable `RICHTEMPLATES_ROOT` (it is not used
normally) and insert it's parent directory to sys.path at the beggining of
a list so while importing it will use `richtemplates` from this boundled
package even if you have already installed other version globally.


-----------
Quick start
-----------

Follow this steps in order to browse example project:

1. Go into directory `example_project`
2. Run ``python manage.py syncdb`` (if asked, you may create admin account)
3. Run ``python manage.py import_media richtemplates``
4. Run ``python manage.py runserver`` and point you browser to location
   `http://127.0.0.1:8000`

You should be able to browse example project.
Have fun!

