from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: Googlebot",
        "Disallow: /app/auth/verify_update/",
        "Disallow: /app/auth/verify/",
        "Disallow: /app/auth/result/",
        "",
        "User-Agent: Yandex",
        "Disallow: /app/auth/verify_update/",
        "Disallow: /app/auth/verify/",
        "Disallow: /app/auth/result/",
        "Host: https://www.zametochnik.ru/",
        "",
        "User-agent: *",
        "Disallow: /app/auth/verify_update/",
        "Disallow: /app/auth/verify/",
        "Disallow: /app/auth/result/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
