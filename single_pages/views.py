from django.shortcuts import render


def landing(request):
    return render(
        request,  # request 가 text가 ('request') < 되면 안된다.
        'single_pages/landing.html',
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )
