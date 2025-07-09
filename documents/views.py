from django.contrib.auth.decorators import login_required
from .forms import DocumentForm, DocumentRenameForm, FolderForm
from .models import Document, Folder
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def main(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        folder_id = request.POST.get('folder')
        folder = Folder.objects.filter(id=folder_id).first() if folder_id else None
        for f in files:
            document = Document(file=f, folder=folder)
            document.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('home')
    else:
        form = DocumentForm()
        folder_form = FolderForm()
        documents = Document.objects.all()
        folders = Folder.objects.all()
    return render(
        request,
        'main.html',
        {
            'form': form,
            'documents': documents,
            'folders': folders,
            'folder_form': folder_form,
        },
    )

@login_required
def photos(request):
    # This regex matches files ending with .jpg, .jpeg, .png, or .gif (case-insensitive)
    photo_files_regex = r'.*\.(jpg|jpeg|png|gif)$'
    documents = Document.objects.filter(file__iregex=photo_files_regex)
    return render(request, 'photos.html', {'documents': documents})


@login_required
def videos(request):
    video_files_regex = r'.*\.(mp4|mov|avi|mkv)$'  # Regular expression to match video file extensions
    documents = Document.objects.filter(file__iregex=video_files_regex)
    return render(request, 'videos.html', {'documents': documents})


@login_required
def others(request):
    # Combine photo and video regex patterns and exclude them
    not_photo_video_regex = r'.*\.(jpg|jpeg|png|gif|mp4|mov|avi|mkv)$'
    documents = Document.objects.exclude(file__iregex=not_photo_video_regex)
    return render(request, 'others.html', {'documents': documents})


@login_required
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


@login_required
def search(request):
    query = request.GET.get('q', '')
    documents = Document.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {
        'documents': documents,
        'query': query,
    })


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('home')
    return render(request, 'confirm_delete.html', {'document': document})


@login_required
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


@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FolderForm()
    return render(request, 'create_folder.html', {'form': form})
