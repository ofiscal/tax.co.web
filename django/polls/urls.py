from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [

  ####
  #### The index
  ####

  path( '', # Corresponds to the post-domain path "/polls/".

        ( # pick one of the following
          # views.index_1,
          # views.index_2,
          # views.index_3,
          views . IndexView . as_view ()
          ),

        name = 'index' ), # Optional. Useful for `URL reversing`.
        # See "demonstrateReverse" below, or the reading here:
        # https://docs.djangoproject.com/en/3.1/topics/http/urls/#naming-url-patterns


  ####
  #### The detail (of a Question)
  ####

  # These correspond to a post-domain path like "/polls/5/".

  # Pick one of these
#  path('<int:question_id>/', views.detail_1, name='detail'),
#  path('<int:question_id>/', views.detail_2, name='detail'),
#  path('<int:question_id>/', views.detail_3, name='detail'),
  path( '<int:pk>/', # Matches an integer, uses it as the primary key
                     # with which to lookup a question.
        ( # Pick one of these.
          # views.DetailView_1.as_view(),
          views.DetailView_2.as_view()
          ),
        name='detail'),


  ####
  #### The vote action
  ####

  # This does not correspond to any view.
  # Visiting this URL is achieved by submitting a vote from 'detail'.
  # Once the vote action is complete, the user is taken to 'results'.

  # These patterns correspond to a post-domain URL like /polls/5/vote/

  path( '<int:question_id>/vote/',
        views.vote,
        name='vote'),


  ####
  #### Results (of submitting a vote)
  ####

  # These correspond to a post-domain path like "/polls/5/results".

  # Pick one of these:
  # path( '<int:question_id>/results/', views.results_1, name='results'),
  path( '<int:pk>/results/',
        views . ResultsView . as_view(),
        name = 'results' ),


  ####
  #### A page to demonstrate django's 'reverse' function
  ####

  # Http://127.0.0.1:8000/polls/1/1/demonstrateReverse/1/
  path( '<int:a>/<int:b>/demonstrateReverse/<int:c>/',
        views . demonstrateReverse,
        name = 'nameOfUrlToDemonstrateReverse' ),


  ####
  #### Embed pictures
  ####

  path( "embed-pictures",
        views . embed_pictures,
        name = "embed-pictures" ),


  ####
  #### A minimal example of form submission and redirection.
  ####

  # The user visits 'silly-form', which sends their data (their name) to
  # 'silly-form-process', which changes it (appends "Mr ") and sends it to
  # 'silly-form-result'. Although 'silly-form-process' is a URL,
  # it never displays a page to the user;
  # they are taken straight from the first URL to the last,
  # skipping the midpoint.

  # Each URL lookup goes through this code,
  # which looks through polls.views for a function.
  # Each function calling "render" uses a template in polls/templates/polls.
  # The URL in the middle, 'silly-form-process', renders nothing
  # and therefore uses no template.

  path( 'silly-form/',
        views . silly_form,
        name = 'silly-form' ),

  path( 'silly-form-2/',
        views . silly_form_2,
        name = 'silly-form-2' ),

  path( 'silly-form-process/',
        views . silly_form_process,
        name = 'silly-form-process' ),

  path( 'silly-form-result/<name_augmented>/',
        views . silly_form_result,
        name = 'silly-form-result' ),
]
