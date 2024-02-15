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
            contacts = request.user.contacts.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(company__icontains=search_query)
            )

        return render(request,
                      'private/space/create/components/contacts/results.html',
                      {'contacts': contacts})
    return HttpResponseBadRequest()


@require_GET
@login_required
def create_contact_modal(request):
    if request.method == 'GET':
        form = ContactForm(request=request)
        return render(request,
                      'private/space/create/components/contacts/create_modal.html', {'form': form})

    return HttpResponseBadRequest()


@require_POST
@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact created successfully')
            return render(request,
                          'private/space/create/components/contacts/create_form.html',
                          {'form': form, 'show_msg': True, 'from_htmx': True})
        return render(request,
                      'private/space/create/components/contacts/create_form.html',
                      {'form': form})
    return HttpResponseBadRequest()
