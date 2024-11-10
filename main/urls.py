from django.urls import path
from .views import add_to_cart, checkout, checkout_success, import_csv, profile, index, register, login_user, logout_user, remove_from_cart, show_admin, create_toko_entry, create_product_entry, show_xml, show_json, edit_toko, edit_product, delete_toko, delete_product, show_xml_toko_by_id, show_xml_produk_by_id, show_json_toko_by_id, show_json_produk_by_id, product_page, product_detail, add_review, edit_review, delete_review, toko_by_category, view_cart
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main'

urlpatterns = [
    path('', index, name = 'index'),
    path('admin/', show_admin, name='show_admin'),
    path('category/<str:category>/', toko_by_category, name='toko_by_category'),
    path('toko/<uuid:toko_id>/products/', product_page, name='product_page'),
    path('create-toko/', create_toko_entry, name='create_toko_entry'),
    path('create-product/', create_product_entry, name='create_product_entry'),
    path('add_to_cart/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name="show_json"),
    path('xml/toko/<str:id>/', show_xml_toko_by_id, name="show_xml_toko_by_id"),
    path('xml/produk/<str:id>/', show_xml_produk_by_id, name="show_xml_produk_by_id"),
    path('json/toko/<str:id>/', show_json_toko_by_id, name="show_json_toko_by_id"),
    path('json/produk/<str:id>/', show_json_produk_by_id, name="show_json_produk_by_id"),
    path('edit-toko/<uuid:id>', edit_toko, name="edit_toko"),
    path('edit-product/<uuid:id>', edit_product, name="edit_product"),
    path('delete-toko/<uuid:id>/', delete_toko, name="delete_toko"),
    path('delete-product/<uuid:id>', delete_product, name="delete_product"),
    path('product_page/<uuid:product_id>/', product_detail, name='product_detail'),
    path('product_page/<uuid:product_id>/add-review/', add_review, name='add_review'),
    path('product_page/<uuid:product_id>/edit-review/<int:review_id>/', edit_review, name='edit_review'),  # Edit review
    path('product_page/<uuid:product_id>/delete-review/<int:review_id>/', delete_review, name='delete_review'),  # Delete review
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('import-csv/', views.import_csv, name='import_csv'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

