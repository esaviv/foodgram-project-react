from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TokenViewSet, UsersViewSet

app_name = 'api'

router = SimpleRouter()
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
router.register('users', UsersViewSet, basename='users')


auth_urls = [
    path(
        'login/', TokenViewSet.as_view(), name='login'
    )
]


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(auth_urls)),
]
