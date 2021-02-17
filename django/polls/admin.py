from django . contrib import admin

from .models import Question, Choice


class QuestionAdmin_1 ( admin . ModelAdmin ):
  # Alternatives.
    fields = ['pub_date', 'question_text']
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]


class ChoiceInline ( admin . TabularInline ):
    # Gives a compact, 2d presentation of the same info.

#class ChoiceInline(admin.StackedInline):
    # Gives a long, 1d presentation of the same info.

    model = Choice

    # "By default, provide enough fields for 3 choices."
    # The user can add more, and they don't have to fill out all 3.
    # "each time you come back to the “Change” page for an
    # already-created object, you get another three extra slots.
    extra = 3

class QuestionAdmin_2 ( admin . ModelAdmin ):

    # Attributes to show while user chooses from all questions.
    # Optional. "By default, Django displays the str() of each object."
    # TODO ? Why, when I change Question.__str__() to always return
    # "hoo-ha!", does this page not show "hoo-ha!"?
    list_display = (
        'question_text',
        'pub_date', # Displays as 'date published'. See models.py for why.
                    # (By default, fields are shown as the field name,
                    # in caps, with '_' replaced by ' '.
        'was_published_recently' )
    list_filter = ['pub_date']
      # Django automatically creates options like "last 7 days".
    search_fields = ['question_text']
      # Text-based search. Strict matching, not regex.
      # Whitespace defines tokens. Order of tokens is ignored.

    # What to show while user creates|edits a question.
    fieldsets = [
      (None,               { 'fields': ['question_text']}),
      ('Date information', { 'fields': ['pub_date'],
                             'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

# Makes the Question type visible, modifiable from the /admin page.
admin.site.register(
    Question,
    QuestionAdmin_2 ) # Optional argument

# This enables an awkward way to add Choices to a Question:
# Create the choice, and select that question as its question field.
# The "inline" method above offers a more natural way.
admin . site . register ( Choice )
