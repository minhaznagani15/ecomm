from django.urls import path
from . import views
from .views import SimpleView
from ecomm import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about',views.about),
    # path('',views.home),
    path('contact',views.contact),
    path('edit/<rid>',views.edit),
    path('addition/<x1>/<x2>',views.addition),
    path('myview',SimpleView.as_view()),
    path('hello',views.hello),
    path('',views.index),
    path('pdetails',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('pdetails/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
