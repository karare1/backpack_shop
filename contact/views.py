from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


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
                )
            # message = f'We have received your inquiry: \
            #     <p>{subject1}</p> \
            #     <p>{message1}</p>.'
            # message = "Our team will be in touch with you within 48hrs."
            email_from = settings.DEFAULT_FROM_EMAIL
            email = form.cleaned_data['email']

            # send_mail(subject, message, email_from, [email])

            # subject1 = "BackpcakAround Contact Form "
            # body = {
            #     'name': form.cleaned_data['name'],
            #     'email': form.cleaned_data['email'],
            #     'subject': form.cleaned_data['subject'],
            #     'message1': form.cleaned_data['message'],
            #     }
            # message1 = "\n".join(body.values())

            # if name and subject and message and email:
            try:
                send_mail(subject, message, email_from, [email])
                # messages.success(request, f'Your message has been submitted successfully. \
                # A confirmation email will be sent to {email}.')
                return render(request, 'contact/success.html')
                # send_mail(subject1, body, email_from, [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            # return HttpResponseRedirect('/contact/thanks/')
        # send_mail(name, email, subject, message, 'admin@example.com', ['admin@example.com'])

            # return render(request, 'contact_form/success.html')
        else:
            messages.error(request, 'Invalid form submission.')
            return render(request, 'contact/contact.html', {'form': form})

    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)


# def success(request):
#     return render(request, 'contact/success.html')
