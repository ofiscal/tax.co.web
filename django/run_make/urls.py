from django.urls import path

from . import views


app_name = 'run_make'

urlpatterns = [
    path( 'write_time',
          views.write_time,
          name='write_time'),

    path( 'ingest-spec',
          views.ingest_spec,
          name='ingest-spec'),

    path( 'thank-for-spec/<email>',
          views.thank_for_spec,
          name='thank-for-spec'),

    path( 'download',
          views.download,
          name='download'),

    path( 'upload_and_show_url',
           views.upload_and_show_url,
           name="upload_and_show_url" ),

    path( 'upload_multiple',
           views.upload_multiple,
           name="upload_multiple" )
]
