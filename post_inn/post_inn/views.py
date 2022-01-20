from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: Googlebot",
        "Allow: /",
        "",
        "User-Agent: Yandex",
        "Allow: /",
        "Host: https://www.zametochnik.ru/",
        "",
        "User-agent: *",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
