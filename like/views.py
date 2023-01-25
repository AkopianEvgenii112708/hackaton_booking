

def add_like(request, slug):
    try:
        article = get_object_or_404(Article, slug=slug)
        article.likes += 1
        article.save()
    except ObjectDoesNotExist:
        return Http404
    return redirect(request.GET.get('next', '/'))


def add_dislike(request, slug):
    try:
        article = get_object_or_404(Article, slug=slug)
        article.dislikes += 1
        article.save()
    except ObjectDoesNotExist:
        return Http404
    return redirect(request.GET.get('next', '/'))
