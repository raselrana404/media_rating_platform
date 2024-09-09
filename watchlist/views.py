# from django.shortcuts import render
# from django.http import JsonResponse

# from watchlist.models import Movie
# # Create your views here.


# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {'movies': list(movies.values())}
#     return JsonResponse(data)


# def movie_details(request, pk):
#     movie = Movie.objects.filter(pk=pk)

#     return JsonResponse({'movie': list(movie.values())})
