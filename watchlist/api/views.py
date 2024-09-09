from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
# from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle,ScopedRateThrottle
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.api import serializers
from watchlist.api import permissions
from watchlist.api.throttle import ReviewListThrottle, ReviewCreateThrottle
from watchlist.api.pagination import (WatchListPNPagination,
                                      WatchListLOPagination,
                                      WatchListCPagination,
                                      )


"""
django-filter only works with Generic ApiView and Concrete View Class
"""


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewListCreateCV(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        if review_user.is_anonymous:
            raise ValidationError('You have to login first!')
        review_qs = Review.objects.filter(
            watchlist=watchlist,
            review_user=review_user,
        )
        if review_qs.exists():
            raise ValidationError('You have already reviewd this watch!')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data.get('rating')
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data.get('rating'))/2
        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewDetailCV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

# class ReviewListCreateGV(mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetailGV(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    # pagination_class = WatchListPNPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination


class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {'error': 'Does not found!!!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {'Error': 'Does not found!!!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.WatchListSerializer(
            instance=movie,
            data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(
            {'message': 'Deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
            )


class StreamPlatformAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platforms, many=True)
        # to use hyperlinkrelated field in serializer, we need to pass context
        # serializer = serializers.StreamPlatformSerializer(
        #     platforms,
        #     many=True,
        #     context={'request': request}
        # )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {'error': 'Platform does not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {'error': 'Platform does not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.StreamPlatformSerializer(
            instance=platform,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {'error': 'Platform does not found!!!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        platform.delete()
        return Response(
            {'message': 'Successfully deleted the item'},
            status=status.HTTP_204_NO_CONTENT
        )

# class MovieListAV(APIView):

#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = serializers.MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# class MovieDetailAV(APIView):

#     def get(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response(
#                 {'Error': 'Movie does not found!!!'},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         serializer = serializers.MovieSerializer(movie)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response(
#                 {'Error': 'Movie does not found!!!'},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         serializer = serializers.MovieSerializer(
#             instance=movie,
#             data=request.data
#             )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     def delete(self, request, pk):
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(
#             {'message': 'Deleted successfully'},
#             status=status.HTTP_204_NO_CONTENT
#             )


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = serializers.MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = serializers.MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == "GET":
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie does not found!!!'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = serializers.MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = serializers.MovieSerializer(instance=movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
