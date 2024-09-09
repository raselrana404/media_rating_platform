from django.urls import path

from watchlist.api import views

urlpatterns = [
    # path('list/', views.MovieListAV.as_view(), name='movie-list'),
    # path('<int:pk>/', views.MovieDetailAV.as_view(), name='movie-detail'),

    path('list/', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-detail'),
    # for testing purpose - django-filter
    path('watchlist/', views.WatchListGV.as_view(), name='watch-list'),

    path('platforms/', views.StreamPlatformAV.as_view(), name='platform-list'),
    path(
        'platforms/<int:pk>/',
        views.StreamPlatformDetailAV.as_view(),
        name='platform-detail'
    ),

    # path('review/', views.ReviewListCreateCV.as_view(), name='review-list'),
    # path(
    #     'review/<int:pk>/',
    #     views.ReviewDetailCV.as_view(),
    #     name='review-detail',
    # ),
    path('<int:pk>/reviews/', views.ReviewListCreateCV.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailCV.as_view(), name='review-detail'),
    # path('<int:id>/review/<int:pk>/', views.ReviewDetailCV.as_view(), name='review-detail'),
    path('reviews/', views.UserReview.as_view(), name='user-review-detail'),

]
