from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AnnounceForm, UserReactionForm
from .models import *


class AnnounceList(ListView):
    model = Announce  # Указываем модель, объекты которой будут выводиться
    ordering = '-dateCreation'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'announces.html'  # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'Announces'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['next_announce'] = None
        return context


class AnnounceDetail(DetailView):
    model = Announce
    template_name = 'announce_id.html'
    context_object_name = 'Announce_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reacts = UserReaction.objects.filter(announce_id=self.kwargs['pk'])
        context['reacts'] = reacts
        return context


class ReactionList(ListView):
    model = UserReaction
    ordering = '-dateCreation'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'reactions.html'  # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'Reaction'
    paginate_by = 4

    def get_queryset(self):
        return UserReaction.objects.filter(userreaction_announce__announce_user=self.request.user)

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context


class ReactDetail(DetailView):
    model = UserReaction
    template_name = 'react_detail.html'
    context_object_name = 'React_id'

    def react_detail_view(self, request, pk):
        try:
            react_id = UserReaction.objects.get(pk=pk)
        except UserReaction.DoesNotExist:
            raise Http404("React does not exist!")

        return render(
            request, 'react_detail.html', context={'react': react_id, }
                  )


class AnnounceCreate(LoginRequiredMixin, CreateView):
    # permission_required = ('news.add_post',)
    raise_exception = True
    form_class = AnnounceForm
    model = Announce
    template_name = 'announce_edit.html'
    success_url = reverse_lazy('announce_list')

    def form_valid(self, form):
        announce = form.save(commit=False)
        announce.author = self.request.user.author
        announce.save()
        return super().form_valid(form)


class ReactionCreate(LoginRequiredMixin, CreateView):
    # permission_required = ('news.add_post',)
    raise_exception = True
    form_class = UserReactionForm
    model = UserReaction
    template_name = 'reaction_edit.html'
    success_url = reverse_lazy('announce_list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        announce = Announce.objects.get(pk=kwargs['pk'])
        if form.is_valid():
            react = form.save(commit=False)
            react.author = user
            react.announce = announce
            react.save()
            return self.form_valid(form)

        return redirect('content:react_detail')


def react_accept(request, react_id, announce_id):
    react = get_object_or_404(UserReaction, id=react_id)
    react.status = True  # Изменяем статус на "Подтвержден"
    react.save()
    return redirect('content:react_detail', pk=announce_id)
