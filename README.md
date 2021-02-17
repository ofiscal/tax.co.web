# This is a webapp to serve [tax.co](https://github.com/ofiscal/tax.co).

The idea is that a user describes an alternate Colombian tax reality to the website,
and the website runs the microsimulation (tax.co)
and gets the results to the user somehow -- maybe via email,
as that would avoid a multiuser storage problem.

# This repo was born from another.

From commit `11548a601e2b0c769cda8446aa1b09e819f8a507`
of my personal repo at
`https://github.com/JeffreyBenjaminBrown/learning-aws.git`,
I copied the following things here,
renaming (->) some of them:

  apache2
  {learning      -> studies}/django-uploads
  {learning      -> studies}/wsgi
  python-web-app -> django
  secret          # (this is in .gitignore/)
