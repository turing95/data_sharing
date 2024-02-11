from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.forms import ContactForm


@require_POST
@login_required
def search_contacts(request):
    contacts = []
    if request.method == 'POST':
        search_query = request.POST.get('search-contacts')
        if search_query:
            contacts = request.user.contacts.annotate(
                first_name_similarity=TrigramSimilarity('first_name', search_query),
                last_name_similarity=TrigramSimilarity('last_name', search_query),
                email_similarity=TrigramSimilarity('email', search_query),
            ).filter(
                Q(first_name_similarity__gt=0.1) |
                Q(last_name_similarity__gt=0.1) |
                Q(email_similarity__gt=0.1)
            )

        return render(request,
                      'private/space/create/components/contacts/results.html',
                      {'contacts': contacts})
    return HttpResponseBadRequest()


@require_GET
@login_required
def create_contact_modal(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request,
                      'private/space/create/components/contacts/create_modal.html', {'form': form})

    return HttpResponseBadRequest()


@require_POST
@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact created successfully')
            return render(request,
                          'private/space/create/components/contacts/create_form.html',
                          {'form': form,'show_msg':True,'from_htmx':True},status=201)
        return render(request,
                      'private/space/create/components/contacts/create_form.html',
                      {'form': form})
    return HttpResponseBadRequest()
