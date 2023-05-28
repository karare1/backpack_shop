from django.forms import ModelForm
from contact.models import Contact
from django import forms


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message',)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'cont-form'
        self.fields['subject'].widget.attrs['class'] = 'cont-form'
        self.fields['email'].widget.attrs['class'] = 'cont-form'
        self.fields['message'].widget.attrs['class'] = 'cont-form'

    def success(request):
        return render(request, "contact/success.html")
