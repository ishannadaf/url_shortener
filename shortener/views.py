from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from .models import URL
from .serializers import URLSerializer
from django.shortcuts import render
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle

@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def create_short_url(request):
    serializer = URLSerializer(data=request.data)

    if serializer.is_valid():
        obj = serializer.save()
        short_url = request.build_absolute_uri(f"/{obj.short_code}")
        return Response({"short_url": short_url})

    return Response(serializer.errors)


def redirect_url(request, code):
    cache_key = f"url:{code}"

    # 1. Try cache
    original_url = cache.get(cache_key)

    if not original_url:
        # 2. Fallback to DB
        url = get_object_or_404(URL, short_code=code)
        original_url = url.original_url

        # 3. Store in cache (TTL: 1 hour)
        cache.set(cache_key, original_url, timeout=3600)

        # Update click count
        url.click_count += 1
        url.save()
    else:
        # Optional: still update DB count (can optimize later)
        url = URL.objects.get(short_code=code)
        url.click_count += 1
        url.save()

    return redirect(original_url)


def home(request):
    return render(request, 'index.html')


@api_view(['GET'])
def url_stats(request):
    urls = URL.objects.all().order_by('-created_at')

    data = []
    for url in urls:
        data.append({
            "original_url": url.original_url,
            "short_code": url.short_code,
            "click_count": url.click_count,
            "created_at": url.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return Response(data)


def dashboard(request):
    return render(request, 'dashboard.html')