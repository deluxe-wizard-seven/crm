from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in RegistrationForm.Meta.fields:

            # Setting the label as the placeholder
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label

            # Setting the class of the form
            self.fields[field].widget.attrs["class"] = "form-control"

            # Setting the label as empty string
            self.fields[field].label = ""

            # Removing the help text
            self.fields[field].help_text = ""
