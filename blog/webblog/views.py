from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Category, Movie, Comments, Profile, Ip
from .forms import LoginForm, RegistrationForm, AddMoviesForm, CommentForm, EditAccountForm, EditProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tests import get_client_ip


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'webblog/index.html'
    extra_context = {
        'title': 'WebBlog'
    }

    def get_queryset(self):
        return Movie.objects.all().order_by('-id')


class MovieListByCategory(MovieListView):
    def get_queryset(self):
        movies = Movie.objects.filter(category_id=self.kwargs['pk']).order_by('-id')
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class MoviesDetailView(DetailView):
    template_name = 'webblog/movies_detail.html'
    model = Movie
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        movies = Movie.objects.all()[:3]
        context['title'] = movie.title
        context['movies'] = movies
        comments = Comments.objects.filter(movie=movie)
        context['comments'] = comments

        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
            ip = get_client_ip(self.request)
            user_ip = Ip.objects.filter(ip=ip, movie=movie, user=self.request.user)

            if not user_ip:
                ip = Ip.objects.create(ip=ip, movie=movie, user=self.request.user)
                ip.save()
        return context


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Авторизация прошла успешно')
                return redirect('index')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')

        else:
            messages.error(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }
    if not request.user.is_authenticated:
        return render(request, 'webblog/login.html', context)
    else:
        return redirect('index')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid:
            user = reg_form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Регестрация прошла успешно, авторизуйтесь!')
            return redirect('login')
        else:
            for field in reg_form.errors:
                messages.error(request, reg_form.errors[field].as_text())
            return redirect('register')

    else:
        reg_form = RegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': reg_form
    }
    if not request.user.is_authenticated:
        return render(request, 'webblog/register.html', context)
    else:
        return redirect('index')


class AddMovie(CreateView):
    form_class = AddMoviesForm
    template_name = 'webblog/add_movies.html'
    context_object_name = {
        'title': 'Добавить',
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            return super(AddMovie, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MovieUpdate(UpdateView):
    model = Movie
    form_class = AddMoviesForm
    template_name = 'webblog/add_movies.html'


class DeleteMovie(DeleteView):
    model = Movie
    context_object_name = 'movie'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Удаление'
    }

    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            if movie.author != self.request.user:
                return redirect('index')
        return super(DeleteMovie, self).get(request, *args, **kwargs)


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = Movie.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        return redirect('movie', pk)


class CommentUpdate(UpdateView):
    model = Comments
    form_class = CommentForm
    template_name = 'webblog/movies_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comment = Comments.objects.get(pk=self.kwargs['pk'])
        movie = Movie.objects.get(pk=comment.movie.pk)
        movies = Movie.objects.all()[:3]
        comments = Comments.objects.filter(movie=movie)
        context['comments'] = comments
        context['movie'] = movie
        context['movies'] = movies
        return context

    def get_success_url(self):
        return reverse('movie', kwargs={'pk': self.object.movie.pk})


def comment_delete(request, pk):
    comment = Comments.objects.get(pk=pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('movie', comment.movie.pk)


class SearchResults(MovieListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        movies = Movie.objects.filter(title__iregex=word)
        return movies


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        movies = Movie.objects.filter(author_id=pk)
        context = {
            'title': profile.user.username,
            'profile': profile,
            'movies': movies
        }

        return render(request, 'webblog/profile.html', context)

    else:
        return redirect('login')


def edit_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            edit_account_form = EditAccountForm(request.POST, instance=request.user)
            if edit_account_form.is_valid():
                data = edit_account_form.cleaned_data
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Данные успешно изменены')
                        return redirect('profile', user.pk)

                    else:
                        for field in edit_account_form.errors:
                            messages.error(request, edit_account_form.errors[field].as_text())
                            return redirect('edit_account')
                else:
                    for field in edit_account_form.errors:
                        messages.error(request, edit_account_form.errors[field].as_text())
                        return redirect('edit_account')

                edit_account_form.save()
                return redirect('profile', user.pk)

        else:
            edit_account_form = EditAccountForm(instance=request.user)

        context = {
            'title': 'Изменить аккаунт',
            'edit_account_form': edit_account_form
        }

        return render(request, 'webblog/change.html', context)

    else:
        return redirect('login')


def edit_profile_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            edit_profile = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if edit_profile.is_valid():
                edit_profile.save()
                messages.success(request, 'Изменения были успешно добавлены')
                return redirect('profile', request.user.pk)
            else:
                for field in edit_profile.errors:
                    messages.error(request, edit_profile.errors[field].as_text())
                    return redirect('edit_profile')

        else:
            edit_profile = EditProfileForm(instance=request.user.profile)

        context = {
            'title': 'Изменить профиль',
            'edit_profile_form': edit_profile
        }
        return render(request, 'webblog/change.html', context)
    else:
        return redirect('login')
