from django.urls import path

import run_make.views.views    as vs
import run_make.views.examples as vx


app_name = 'run_make'

urlpatterns = [
    path( 'write_time',
          vx.write_time,
          name='write_time'),

    path( 'ingest_full_spec',
          vs.ingest_full_spec,
          name='ingest_full_spec'),

    path( 'thank-for-spec/<user_email>',
          vs.thank_for_spec,
          name='thank-for-spec'),

    path( 'download',
          vx.download,
          name='download'),

    path( "upload_multiple_with_logging",
          vx.upload_multiple_with_logging,
          name="upload_multiple_with_logging" ),

    path( 'upload_and_show_url',
           vx.upload_and_show_url,
           name="upload_and_show_url" ),

    path( 'upload_multiple',
           vx.upload_multiple,
           name="upload_multiple" )
]
