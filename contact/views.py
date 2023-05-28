from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject1 = form.cleaned_data["subject"]
            message1 = form.cleaned_data['message']
            subject = "Thank you for contacting BackpackAround"
            message = (
                f"We have received your inquiry: \n"
                f"Subject: {subject1} \n"
                f"Message: {message1} \n"
                f"Our staff will contact you within 48 hrours.\n"
                )
            email_from = settings.DEFAULT_FROM_EMAIL
            email = form.cleaned_data['email']
            try:
                send_mail(subject, message, email_from, [email])
                return render(request, 'contact/success.html')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            messages.error(request, 'Invalid form submission.')
            return render(request, 'contact/contact.html', {'form': form})

    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)
