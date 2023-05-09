from django.shortcuts import render


def my_profile(request):
    """ Display the user's profile. """

    template = 'profiles/my_profile.html'
    context = {}

    return render(request, template, context)
