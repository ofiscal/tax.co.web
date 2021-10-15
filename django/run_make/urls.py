from django.urls import path

import run_make.views.views    as views
import run_make.views.examples as examples


app_name = 'run_make'

urlpatterns = [
    path( 'write_time',
          examples.write_time,
          name='write_time' ),

    path( 'render_content_argument',
          examples.render_content_argument,
          name='render_content_argument' ),

    path( 'manual_ingest',
          views.manual_ingest,
          name='manual_ingest'),

    path( 'ingest_full_spec',
          views.ingest_full_spec,
          name='ingest_full_spec'),

    path( 'thank-for-spec/<user_email>',
          views.thank_for_spec,
          name='thank-for-spec'),

    path( 'dynamic_form',
          examples.dynamic_form,
          name='dynamic_form'),

    path( 'radio_table',
          examples.radio_table,
          name='radio_table'),

    path( 'radio_table_generated',
          examples.radio_table_generated,
          name='radio_table_generated'),

    path( 'download',
          examples.download,
          name='download'),

    path( "upload_multiple_with_logging",
          examples.upload_multiple_with_logging,
          name="upload_multiple_with_logging" ),

    path( 'upload_and_show_url',
           examples.upload_and_show_url,
           name="upload_and_show_url" ),

    path( 'upload_multiple',
           examples.upload_multiple,
           name="upload_multiple" )
]
