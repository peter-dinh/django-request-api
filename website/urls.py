from django.conf.urls import url
from  . import views

urlpatterns=[
    url(r'^$', views.index, name="index"),
    url(r'^type_product/(?P<id_type_product>[0-9]+)$', views.type_products, name="type_product"),
    url(r'^brand/(?P<id_brand>[0-9]+)$', views.brand, name="brand"),
    url(r'^search$', views.search, name="search"),
    url(r'^search_price$', views.search_price, name="search_price"),
    url(r'^login$', views.login, name="login" ),
    url(r'^logout$', views.logout, name="logout" ),
    url(r'^register$', views.register, name="register" ),
    url(r'^product_detail/(?P<id_product>[0-9]+)$', views.product_detail, name="product_detail"),
    url(r'^account$', views.account, name="account" ),
    url(r'^change_pass$', views.change_pass, name="change_pass"),
    url(r'^bill$', views.bill, name="bill" ),
    url(r'^bill_info/(?P<id_bill>[0-9]+)$', views.bill_info, name="bill_info" ),
    url(r'^cart$', views.cart, name="cart"),
    url(r'^add/(?P<id_product>[0-9]+)/(?P<qty>[0-9]+)$', views.add, name="add"),
    url(r'^remove/(?P<id_product>[0-9]+)$', views.remove, name="remove"),
    url(r'^submit$', views.submit, name="submit"),
    url(r'^rating/(?P<id_product>[0-9]+)$', views.rating, name="rating"),
    url(r'^emailconfirm/', views.emailconfirm, name="emailconfirm"),
    url(r'^requestmerchentaccount/', views.requestmerchentaccount, name="requestmerchentaccount"),
    url(r'^confirmmerchentaccount/', views.confirmmerchentaccount, name="confirmmerchentaccount"),
]