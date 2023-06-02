from django.urls import include, path
from .views import SearchResultsView, home, CustomLoginView, profile, update_profile, remove_avatar, UserFavoriteMovies, add_to_favorite

urlpatterns = [
    path("", home, name="home"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('accounts/', include('allauth.urls')),
    path('login/', CustomLoginView.as_view(), name='custom_account_login'),
    path('profile/', profile, name='profile_view'),
    path('accounts/profile/', profile, name='profile_view'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update/remove-avatar/', remove_avatar, name='remove_avatar'),
    path('profile/favorite-movies/', UserFavoriteMovies.as_view(), name='favorite_movies_view'),
    path('profile/add-to-favorite/', add_to_favorite, name='add_to_favorite'),
]












