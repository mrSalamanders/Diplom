from django.shortcuts import render
from .models import Tag


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "products/snippets/tag.html", context={"tags": tags})
