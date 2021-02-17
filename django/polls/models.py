import datetime

from django . db import models
from django . utils import timezone


# Each model roughly corresponds to a DB table.
# Each attribute is a DB field.
  # PITFALL: Attribute names must not conflict with the API
  # https://docs.djangoproject.com/en/3.0/ref/models/instances/
  # (e.g. clean, save, delete).
# Primary key fields are automatically generated, as integers,
  # but this can be overridden.

class Question ( models . Model ):
  question_text = models . CharField ( max_length = 200 )
    # To see all fields built into Django (custom ones are possible too):
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#model-field-types
  pub_date = models . DateTimeField (
      # All fields accept an optional human-readable name like this,
      # usually as the first argument.
      'date published' )
  def __str__( self ):
    return self . question_text

  def was_published_recently ( self ):
    t = timezone . now ()
    return ( t - datetime . timedelta( days = 365 )
             <= self . pub_date
             <= t )
  was_published_recently . admin_order_field = 'pub_date'
    # On the admin page, clicking to sort by this has the effect of
    # sorting by 'pub_date'.
  was_published_recently . boolean = True
    # On the admin page, this causes was_published_recently to display
    # as a a checkmark (true) or an X (false).
  was_published_recently . short_description = 'Published recently?'
    # On the admin page, this changes the title of the field.
    # It's like the optional argument to DateTimeField above,
    # which cannot be used for function definitions.

class Choice ( models . Model ):
  question = ( # refers to another table
      models . ForeignKey( Question,
                           on_delete = models . CASCADE ) )
  choice_text = models . CharField ( max_length = 200 )
  votes = models . IntegerField ( default = 0 )
  def __str__ ( self ):
    return self . choice_text
