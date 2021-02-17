from polls.models import Choice, Question
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import UploadFileForm, NameForm


####
#### (Evolution of)
#### the index
####

indexTemplate = 'polls/index_2.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `index_x` defined below and the numbers x in `polls/index_x.html` above.
# Also, IndexView below is another alternative to the index_x functions.

def index_1(request):
    latest_question_list = ( Question . objects
                             . order_by ('-pub_date')
                             [:5] )
    output = ', ' . join ( [ q . question_text
                             for q in latest_question_list ] )
    return HttpResponse ( output )

# This is better because it has a hyperlink, thanks to the template.
def index_2 ( request ) :
  return HttpResponse (
    loader . get_template ( indexTemplate )
    . render (
        { 'latest_question_list' : # this name is meaningful to the template
          Question . objects .
          order_by ( '-pub_date' )
          [:5] },
        request ) )

# The last one's idiom is so common that there's shorthand for it.
# This is equivalent to the last one.
def index_3 ( request ):
  return render (
    request, # TODO: What's the point of this argument?
    indexTemplate,
    { 'latest_question_list' :
     ( Question . objects .
       order_by (  '-pub_date' )
       [:5] ) } )

class IndexView ( generic . ListView ):
  # Override the default of '<app name>/<model name>_list.html'.
  template_name = indexTemplate

  # Override the default of 'question_list'.
  # TODO: For that default, does django infer 'question'
  # from the 'get_queryset()' field below?
  context_object_name = (
      'latest_question_list' # this name is meaningful to the template
      )

  # Override the default, which is to return all of them.
  def get_queryset ( self ):
    """Return the last five published questions."""
    return (
      Question . objects . filter (
          # pub_date__lte (less than or equal) is automatically created
          # by Django for the Question class.
          pub_date__lte = timezone . now () ) .
      order_by ( '-pub_date')
      [:5] )


####
#### Detail view of a vote, inc. the opportunity to vote
####

detailTemplate = 'polls/detail_3.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `detail_x` defined below and the numbers x in `polls/detail_x.html` above.
# DetailView below is another alternative to the detail_x functions.

def detail_1 (request, question_id):
  return HttpResponse (
    "This will eventually show question %s." % question_id )

# This is better:
#   It actually shows the question, and its options.
#   It lets you vote
#     (the template links the "vote" button to another page).
#   It gives a 404 error if the question_id isn't in the DB.
def detail_2 ( request, question_id ) :
  try:
    question = Question . Objects . get ( pk = question_id )
  except Question.DoesNotExist:
    raise Http404 ( "Question does not exist" )
  return render ( request,
                  detailTemplate,
                  {'question': question} )

# That pattern, too, is so common that there's shorthand for it.
# The following is equivalent to the preceding:
def detail_3 ( request, question_id ):
    question = get_object_or_404 ( Question,
                                   pk = question_id )
    # "There’s also a get_list_or_404() function, which works just as get_object_or_404 (), but it uses filter() instead of get(), so it can find lots of stuff. It raises Http404 if the list is empty.
    return render ( request,
                    detailTemplate,
                    {'question' :  question} )

# Just like detail_3, but more concise.
class DetailView_1 ( generic . DetailView ):
  # A generic.DetailView details a single object.
  # It "expects the primary key value captured from the URL to be called" pk.

  # TODO: Functions like detail_3 send a dictionary with a "question" key,
  # which then substitutes content into the template.
  # But this defines no such key. Does it always simply lowercase
  # the class name? If so, what about interior capitals?

  model = Question # Defines the type of thing the view details.

  # Overrides the default, which would be a template called
  # <app name>/<model name>_detail.html.
  template_name = detailTemplate

# Equal to DetailView_1, except with an overridden method.
class DetailView_2( DetailView_1 ):

  def get_object ( self ) : # Override to prohibit fetching from the future.
    # PITFALL: Altering the context (not done here) can get hairy:
    # "Generally, get_context_data will merge the context data of all parent classes with those of the current class. To preserve this behavior in your own classes where you want to alter the context, you should be sure to call get_context_data on the super class."
    # https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/
    obj = super () . get_object ()
    if obj . pub_date >= timezone . now():
      raise Http404 ( "Question not yet available." )
    return obj


####
#### The vote() function
####

# PITFALL: Question: How can vote() know what was chosen,
# given that its only argument beyond the request is question_id?
# Answer: It's in the request.
# See, e.g., the line `form action="{% url 'polls:vote' question.id %}"`
# in templates/polls/detail_2.html, and search for the word "chosen".

def vote ( request, question_id ) :
  question = get_object_or_404 ( Question,
                                 pk = question_id )
  try: selected_choice = (
    question . choice_set . get(
      pk = request . POST [ 'chosen' ] ) ) # returns the ID of the selected choice, as a string. request.POST values are always strings.
      # GET objects are similar, but that's not what vote() receives.
  except ( KeyError,             # If the POST[] lookup fails.
           Choice . DoesNotExist # If, I think, the get() lookup fails.
           ):
    # Redisplay the question voting form.
    return render ( request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    } )

  selected_choice . votes += 1
  selected_choice . save ()
  return HttpResponseRedirect ( # Takes one argument, a URL.
    # PITFALL:
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button. (This advice is not Django-specific.)
    reverse( # TODO: PITFALL: reverse() is confusing. To understand it,
             # try visiting polls . nameOfUrlToDemonstrateReverse,
             # which calls demonstrateReverse() (defined below).
             # I see no reversal in it; you give it a list of arguments
             # in the order they appear in the URL.
        'polls:results',
        kwargs = { "pk" : question . id } ) )


####
#### Results of a vote
####

resultsTemplate = 'polls/results_1.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `results_x` defined below and the numbers x in `polls/results_x.html` above.
# Also, ResultsView below is another alternative to the results_x functions.

def results_1 ( request, question_id ) :
    question = get_object_or_404 ( Question,
                                   pk = question_id )
    return render ( request,
                    resultsTemplate,
                    { 'question' :  question } )

class ResultsView(generic.DetailView):
  model = Question
  template_name = resultsTemplate


####
#### The (url) `reverse` function.
####

def demonstrateReverse (request, a, b, c):
  return HttpResponse (
    '\n'.join( [
      "If the arguments were 1,2 and 3: ",
      reverse( 'polls:nameOfUrlToDemonstrateReverse',
               # PITFALL: safer than 'args' below, which uses a list,
               # would be to use 'kwargs', which takes a dict.
               # But I'm illustrating that reversal does not reverse,
               # so here I'm sticking with 'args'.
               args = [1,2,3] ),
      "If the arguments were those in the URL that brought you here:",
      reverse( 'polls:nameOfUrlToDemonstrateReverse',
               args = [a,b,c] )
    ] ) )


####
#### A page with embedded pictures
####

def embed_pictures ( request ) :
  return render (
    request,
    "polls/embed-pictures.html",
    { "folder" : "user-12" } )


####
#### A silly form
####

# A view (by me) that uses the template code suggested at
#   https://docs.djangoproject.com/en/3.1/topics/forms/

def silly_form ( request ) :
    return render (
        request,
        "polls/silly-form.html",
        { 'default_name' : "Bob Hope" } )

def silly_form_process ( request ):
  # Modifies the data (appending "Mr. " to the name)
  # and passes it to a new URL, without rendering any HTML.
  your_name = request . POST [ 'your_name' ]
  return HttpResponseRedirect (
    reverse ( 'polls:silly-form-result',
              kwargs = { "name_augmented" : "Mr. " + your_name } ) )

def silly_form_result ( request, name_augmented ):
  return render (
      request,
      "polls/silly-form-result.html",
      { 'name_augmented' : name_augmented } )

# Uses a Django Form to reduce template boilerplate.
def silly_form_2 ( request ):
  # Docs that suggest this code:
  #   https://docs.djangoproject.com/en/3.1/topics/forms/

  # If this is a POST request we need to process the form data.
  if request . method == 'POST':
      # Create a form instance and populate it with data from the request.
      # This is called "binding the data to the form",
      # after which the form is "bound":
      form = NameForm ( request . POST )
      # Check whether it's valid:
      if form . is_valid ():
          # Process The Data in `form . cleaned_data` as required:
          # ...
          # (You can still access the unvalidated data directly from
          # request.POST at this point, but the validated data is better.)

          # Redirect to a new URL:
          return HttpResponseRedirect (
              reverse (
                  'polls:silly-form-result',
                  kwargs = { "name_augmented" :
                             "Mr. " + form . cleaned_data [ your_name ]
                             } ) )

  # If a GET (or any other method) we'll create a blank form.
  else:
    form = NameForm()

  # TODO ? This is the alternative to the HttpResponseRedirect above?
  # Is it meant to redisplay this same page,
  # because the user's data was bad?
  return render ( request,
                  'polls/silly-form-2.html',
                  { 'form' :  form } )
