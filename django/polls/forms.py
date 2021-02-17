from django import forms


class NameForm ( forms. Form ):
  your_name = forms.CharField(
      label = 'Your name',
      max_length = 100 )

class UploadFileForm ( forms . Form ) :
  # Copied from
  # https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
  title = forms . CharField ( max_length = 50 )
  file = forms . FileField () # This part permits file upload,
    # ASSUMING the request method was POST and the HTML form element
    # has the attribute `enctype="multipart/form-data"`.
    # A view handling this form
    # can access the file uploaded in this field as `request.FILES['file']`,
    # because the field is named "file".
    # There could be multiple such fields in the same form.
