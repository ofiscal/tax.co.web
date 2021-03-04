# This is a webapp to serve [tax.co](https://github.com/ofiscal/tax.co).

The user describes an alternate Colombian tax system to the website,
which runs the microsimulation (tax.co)
and gets the results to the user somehow -- maybe via email,
as that would avoid a multiuser storage problem.


# PITFALL: Some legacy code here is probably broken

I did a lot of learning in folders like `studies/` and `django/polls/`.
None of that code is needed for the app to run,
but I've kept it around for reference.
I've since changed the permissions in
`django/ebdjango/settings.py` and `apache/apache2.conf`,
which probably broke some of that legacy code that was for uploading or downloading files.
