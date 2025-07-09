from .forms import DocumentForm, DocumentRenameForm
from .models import Document
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def main(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for f in files:
            document = Document(file=f)
            document.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('home')
    else:
        form = DocumentForm()
        documents = Document.objects.all()
    return render(request, 'main.html', {'form': form, 'documents': documents})


def photos(request):
    # This regex matches files ending with .jpg, .jpeg, .png, or .gif (case-insensitive)
    photo_files_regex = r'.*\.(jpg|jpeg|png|gif)$'
    documents = Document.objects.filter(file__iregex=photo_files_regex)
    return render(request, 'photos.html', {'documents': documents})


def videos(request):
    video_files_regex = r'.*\.(mp4|mov|avi|mkv)$'  # Regular expression to match video file extensions
    documents = Document.objects.filter(file__iregex=video_files_regex)
    return render(request, 'videos.html', {'documents': documents})


def others(request):
    # Combine photo and video regex patterns and exclude them
    not_photo_video_regex = r'.*\.(jpg|jpeg|png|gif|mp4|mov|avi|mkv)$'
    documents = Document.objects.exclude(file__iregex=not_photo_video_regex)
    return render(request, 'others.html', {'documents': documents})


def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Identify the document type based on its extension
    if document.is_photo():
        queryset = Document.objects.filter(file__iregex=r'.*\.(jpg|jpeg|png|gif)$')
    elif document.is_video():
        queryset = Document.objects.filter(file__iregex=r'.*\.(mp4|mov|avi|mkv)$')
    else:
        not_photo_video_regex = r'.*\.(jpg|jpeg|png|gif|mp4|mov|avi|mkv)$'
        queryset = Document.objects.exclude(file__iregex=not_photo_video_regex)

    next_document = queryset.filter(id__gt=document.id).order_by('id').first()
    prev_document = queryset.filter(id__lt=document.id).order_by('-id').first()

    return render(request, 'document_detail.html', {
        'document': document,
        'next_document': next_document,
        'prev_document': prev_document,    })


def search(request):
    query = request.GET.get('q', '')
    documents = Document.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {
        'documents': documents,
        'query': query,
    })


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('home')
    return render(request, 'confirm_delete.html', {'document': document})


def rename_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentRenameForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_detail', document_id=document.id)
    else:
        form = DocumentRenameForm(instance=document)
    return render(request, 'rename_document.html', {
        'form': form,
        'document': document,
    })
