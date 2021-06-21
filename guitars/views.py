
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from guitars.forms import GuitarModelForm
from guitars.models import Guitar, Type
#from .forms import GuitarForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_guitars = Guitar.objects.all().count()
    guitars = Guitar.objects.order_by('-rate')[:3]

    context = {
        'num_guitars': num_guitars,
        'guitars': guitars
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class GuitarListView(ListView):
    model = Guitar

    context_object_name = 'guitar_list'   # your own name for the list as a template variable
    template_name = 'guitar/list.html'  # Specify your own template name/location
    paginate_by = 3

    def get_queryset(self):
        if 'type_name' in self.kwargs:
            return Guitar.objects.filter(type__name=self.kwargs['type_name']).all() # Get 5 books containing the title war
        else:
            return Guitar.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_guitars'] = len(self.get_queryset())
        if 'type_name' in self.kwargs:
            context['view_name'] = f"Typ: {self.kwargs['type_name']}"
            context['view_head'] = f"Typ Kytary: {self.kwargs['type_name']}"
        else:
            context['view_name'] = 'Kytary'
            context['view_head'] = 'Přehled kytar'
        return context

class GuitarDetailView(DetailView):
    model = Guitar

    context_object_name = 'guitar_detail'   # your own name for the list as a template variable
    template_name = 'guitar/detail.html'  # Specify your own template name/location


class TypeListView(ListView):
    model = Type
    template_name = 'blocks/type_list.html'
    context_object_name = 'types'
    queryset = Type.objects.order_by('name').all()


class TopTenListView(ListView):
    model = Guitar
    template_name = 'blocks/top_ten.html'
    context_object_name = 'guitars'
    queryset = Guitar.objects.order_by('-rate').all()[:10]


class NewGuitarListView(ListView):
    model = Guitar
    template_name = 'blocks/new_guitars.html'
    context_object_name = 'guitars'
    paginate_by = 2


class GuitarCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Guitar
    fields = ['name', 'description', 'stringnumber', 'image', 'rate', 'type']
    initial = {'rate': '5'}
    login_url = '/accounts/login/'
    permission_required = 'guitar.add_guitar'


class GuitarUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Guitar
    template_name = 'guitars/guitar_bootstrap_form.html'
    form_class = GuitarModelForm
    login_url = '/accounts/login/'
    permission_required = 'guitars.change_guitar'


class GuitarDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Guitar
    success_url = reverse_lazy('guitars')
    login_url = '/accounts/login/'
    permission_required = 'guitars.delete_guitar'


def error_404(request, exception=None):
        return render(request, 'errors/404.html')

def error_500(request):
    return render(request, 'errors/500.html')

def error_403(request, exception=None):
    return render(request, 'errors/403.html')

def error_400(request, exception=None):
    return render(request, 'errors/400.html')

@never_cache
def clear_cache(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cache.clear()
    return HttpResponse('Cache has been cleared')
