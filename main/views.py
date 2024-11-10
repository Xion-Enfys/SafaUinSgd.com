import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CartItemForm, TokoEntryForm, ProductEntryForm
from .models import Cart, CartItem, TokoEntry, ProductEntry
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.core.exceptions import ValidationError
import re
import json
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import os
from django.shortcuts import render, redirect
from .models import Review
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect  
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from django.shortcuts import render, get_object_or_404

@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(user=request.user)  
    total_price = sum(item.total_price for item in cart_items)  

    if request.method == 'POST':
        return redirect('main:checkout_success')

    return render(request, 'pembayaran.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def checkout_success(request):

    cart_items = CartItem.objects.filter(user=request.user)  
    total_price = sum(item.total_price for item in cart_items)  

    return render(request, 'Struk.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
def show_admin(request):
    toko_entries = TokoEntry.objects.all()
    product_entries = ProductEntry.objects.all()

    unique_categorys = set(toko_entry.category.lower() for toko_entry in toko_entries)
    unique_categorys_display = {category: toko_entry.category for toko_entry in toko_entries for category in unique_categorys if category == toko_entry.category.lower()}

    
    context = {
        'toko_entries': toko_entries,
        'product_entries': product_entries,
        'unique_categorys': unique_categorys_display.values(),
    }

    return render(request, "boardadmin.html", context)

def create_toko_entry(request):
    form = TokoEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect ('main:show_admin')
    
    context = {'form': form}
    return render(request, "create_toko_entry.html", context)

def create_product_entry(request):
    if request.method == "POST":
        form = ProductEntryForm(request.POST, request.FILES)  
        if form.is_valid():
            try:
                form.save()
                return redirect('main:show_admin')
            except ValidationError as e:
                form.add_error('name', e)
    else:
        form = ProductEntryForm()

    context = {'form': form}
    return render(request, "create_product_entry.html", context)

def show_xml(request):
    toko_data = serializers.serialize("xml", TokoEntry.objects.all())
    product_data = serializers.serialize("xml", ProductEntry.objects.all())

    # Menghapus deklarasi XML <?xml ... ?> dari kedua hasil serialisasi
    toko_data = re.sub(r'<\?xml[^>]+\?>', '', toko_data)
    product_data = re.sub(r'<\?xml[^>]+\?>', '', product_data)

    # Gabungkan keduanya dalam satu XML dengan root <data>
    xml_data = f'<?xml version="1.0" encoding="UTF-8"?>\n<data>\n<toko>{toko_data}</toko>\n<produk>{product_data}</produk>\n</data>'

    # Return hasil XML gabungan
    return HttpResponse(xml_data, content_type="application/xml")

def show_xml_toko_by_id(request, id):
    try:
        # Ambil data toko berdasarkan id
        toko = get_object_or_404(TokoEntry, pk=id)

        # Serialize data dari model TokoEntry berdasarkan id
        toko_data = serializers.serialize("xml", [toko])  # serialize toko sebagai list

        # Menghapus deklarasi XML <?xml ... ?> dari hasil serialisasi
        toko_data = re.sub(r'<\?xml[^>]+\?>', '', toko_data)

        # Return hasil XML dari toko saja
        xml_data = f'<?xml version="1.0" encoding="UTF-8"?>\n<toko>{toko_data}</toko>'
        return HttpResponse(xml_data, content_type="application/xml")

    except TokoEntry.DoesNotExist:
        return HttpResponse("<error>Toko with given ID does not exist.</error>", content_type="application/xml", status=404)

def show_xml_produk_by_id(request, id):
    try:
        # Ambil toko berdasarkan id
        product = get_object_or_404(ProductEntry, pk=id)

        # Serialize data dari model ProductEntry berdasarkan toko yang diambil
        product_data = serializers.serialize("xml", [product])

        # Menghapus deklarasi XML <?xml ... ?> dari hasil serialisasi
        product_data = re.sub(r'<\?xml[^>]+\?>', '', product_data)

        # Return hasil XML dari produk saja
        xml_data = f'<?xml version="1.0" encoding="UTF-8"?>\n<produk>{product_data}</produk>'
        return HttpResponse(xml_data, content_type="application/xml")

    except TokoEntry.DoesNotExist:
        return HttpResponse("<error>Toko with given ID does not exist.</error>", content_type="application/xml", status=404)

def show_json(request):
    # Serialize data dari model TokoEntry dan ProductEntry
    toko_data = serializers.serialize("json", TokoEntry.objects.all())
    product_data = serializers.serialize("json", ProductEntry.objects.all())

    # Mengubah string JSON menjadi list of dict agar bisa digabungkan
    toko_data = json.loads(toko_data)
    product_data = json.loads(product_data)

    # Gabungkan data menjadi satu dict dengan dua kunci: 'toko' dan 'produk'
    combined_data = {
        "toko": toko_data,
        "produk": product_data
    }

    # Return JSON response
    return JsonResponse(combined_data)

def show_json_toko_by_id(request, id):
    try:
        # Ambil data toko berdasarkan id
        toko = get_object_or_404(TokoEntry, pk=id)

        # Serialize data dari model TokoEntry berdasarkan id
        toko_data = serializers.serialize("json", [toko])  # serialize toko sebagai list

        # Mengubah string JSON menjadi list of dict agar lebih fleksibel
        toko_data = json.loads(toko_data)

        # Return hasil JSON dari toko saja
        return JsonResponse({"toko": toko_data}, safe=False)

    except TokoEntry.DoesNotExist:
        return JsonResponse({"error": "Toko with given ID does not exist."}, status=404)

def show_json_produk_by_id(request, id):
    try:
        # Ambil toko berdasarkan id
        product = get_object_or_404(ProductEntry, pk=id)

        # Serialize data dari model ProductEntry berdasarkan toko yang diambil
        product_data = serializers.serialize("json", [product])

        # Mengubah string JSON menjadi list of dict agar lebih fleksibel
        product_data = json.loads(product_data)

        # Return hasil JSON dari produk saja
        return JsonResponse({"produk": product_data}, safe=False)

    except TokoEntry.DoesNotExist:
        return JsonResponse({"error": "Toko with given ID does not exist."}, status=404)

def edit_toko(request, id):
    # Ambil data toko berdasarkan id
    toko = get_object_or_404(TokoEntry, pk=id)

    # Set TokoEntry sebagai instance dari form
    form = TokoEntryForm(request.POST or None, instance=toko)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman utama
        form.save()
        return HttpResponseRedirect(reverse('main:show_admin'))

    context = {'form': form}
    return render(request, "edit_toko.html", context)

def edit_product(request, id):
    # Ambil data produk berdasarkan id
    product = get_object_or_404(ProductEntry, pk=id)

    # Set ProductEntry sebagai instance dari form
    form = ProductEntryForm(request.POST or None, request.FILES or None, instance=product)


    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman utama
        form.save()
        return HttpResponseRedirect(reverse('main:show_admin'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_toko(request, id):
    toko = get_object_or_404(TokoEntry, pk=id)
    toko.delete()
    return HttpResponseRedirect(reverse('main:show_admin'))

def delete_product(request, id):
    product = get_object_or_404(ProductEntry, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_admin'))

def product_page(request, toko_id):
    # Ambil toko berdasarkan ID
    toko = get_object_or_404(TokoEntry, id=toko_id)
    
    # Ambil produk yang terkait dengan toko tersebut
    products = ProductEntry.objects.filter(toko=toko)
    
    return render(request, 'product_page.html', {'products': products, 'toko': toko})
    
def product_detail(request, product_id):
    product = get_object_or_404(ProductEntry, id=product_id)  # sesuaikan dengan tipe data
    return render(request, 'product_detail.html', {'product': product})

@login_required
@require_POST
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Ambil produk berdasarkan product_id
        product = get_object_or_404(ProductEntry, id=product_id)
        quantity = int(request.POST.get('quantity', 1))  # Ambil jumlah dari form
        
        # Jika pengguna login, kita dapat menghubungkan item dengan pengguna yang login
        user = request.user if request.user.is_authenticated else None

        # Cek apakah produk sudah ada di keranjang untuk pengguna yang sama
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=user,
            defaults={'quantity': quantity}
        )

        if not created:
            # Jika sudah ada, tambahkan kuantitasnya
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'success': True, 'message': 'Item added to cart!'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
@csrf_exempt  # Hanya untuk pengujian, pastikan untuk menghapus ini dalam produksi
def add_review(request, product_id):
    if request.method == 'POST':
        try:
            # Ambil data dari request
            user = request.user
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            # Validasi data
            if not rating or not comment:
                return JsonResponse({'success': False, 'message': 'Rating and comment are required'}, status=400)
            
            # Pastikan rating dalam rentang 1-5
            rating = int(rating)
            if rating < 1 or rating > 5:
                return JsonResponse({'success': False, 'message': 'Rating must be between 1 and 5'}, status=400)

            # Pastikan ProductEntry ditemukan
            product = ProductEntry.objects.get(id=product_id)

            # Buat atau update ulasan
            review, created = Review.objects.update_or_create(
                user=user,
                product=product,
                defaults={
                    'rating': rating,
                    'comment': comment
                }
            )
            
            # Respons JSON
            return JsonResponse({
                'success': True,
                'username': user.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%B %d, %Y, %I:%M %p')
            })
        
        except ProductEntry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid rating value'}, status=400)
        
        except Exception as e:
            print("Error:", e)  # Debug
            return JsonResponse({'success': False, 'message': 'An error occurred'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def edit_review(request, product_id, review_id):
    try:
        review = Review.objects.get(id=review_id, product_id=product_id, user=request.user)

        # Load data JSON dari body permintaan
        data = json.loads(request.body)

        # Update rating dan comment
        review.rating = data['rating']
        review.comment = data['comment']
        review.save()

        return JsonResponse({
            "success": True,
            "username": review.user.username,
            "rating": review.rating,
            "comment": review.comment
        })
    except Review.DoesNotExist:
        return JsonResponse({"success": False, "message": "Review not found."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

    
@login_required
@csrf_exempt
def delete_review(request, product_id, review_id):
    if request.method == 'DELETE':
        try:
            review = Review.objects.get(id=review_id, product_id=product_id)
            review.delete()
            return JsonResponse({'success': True, 'message': 'Review deleted successfully'})
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Review not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def list_reviews(request):
    reviews = Review.objects.all().values("id", "food_name", "rating", "review_text", "created_at")
    return JsonResponse(list(reviews), safe=False, status=200)

def index(request):
    category = request.GET.get('category')  # Ambil kategori dari parameter query string
    if category:
        toko_entries = TokoEntry.objects.filter(category__icontains=category)
    else:
        toko_entries = TokoEntry.objects.all()  # Tampilkan semua toko jika kategori tidak dipilih

    categories = TokoEntry.objects.values_list('category', flat=True).distinct()  # Ambil daftar kategori unik
    return render(request, 'index.html', {
        'toko_entries': toko_entries,
        'categories': categories,
        'selected_category': category
    })
    
def toko_by_category(request, category):
    toko_entries = TokoEntry.objects.filter(category__iexact=category)
    return render(request, 'category_page.html', {'toko_entries': toko_entries, 'category': category})



@login_required(login_url='/login')
def profile(request):
    return render(request, "profile.html")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:index"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
       form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    
    cart_item.delete()

    return redirect('main:view_cart')


def import_csv(request):
    # Define the path to the CSV file
    csv_file_path = "static/csv/data.csv"  # Adjust this to the correct path of your CSV file
    
    # Check if the file exists
    if not os.path.exists(csv_file_path):
        messages.error(request, 'CSV file not found.')
        return render(request, 'import_csv.html')

    # Read and process the CSV file
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Process and store the data in the database
                toko, created = TokoEntry.objects.get_or_create(
                    name=row['TOKO'],
                    defaults={'category': row['KATEGORI']}
                )
                
                ProductEntry.objects.update_or_create(
                    name=row['NAMA_PRODUK'],
                    defaults={
                        'price': row['HARGA_RETAIL'],
                        'description': row['KATEGORI'],
                        'image': row['URL'],
                        'toko': toko,# Make sure to pass only the TokoEntry instance, not the tuple
                    }
                )
        messages.success(request, 'Data CSV successfully imported into the database.')
    except Exception as e:
        messages.error(request, f'Error processing the CSV file: {e}')

    return render(request, 'import_csv.html')