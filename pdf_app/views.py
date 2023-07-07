import PyPDF2
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
from io import BytesIO


def rotate_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        rotation_degree = int(request.POST['rotation_degree'])
        rotation_pages = request.POST['rotation_pages']

        # Save the uploaded PDF file
        save_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
        with open(save_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Rotate the specified pages in the PDF
        rotated_pdf = rotate_pages(save_path, rotation_degree, rotation_pages)

        # Prepare the response as a downloadable file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rotated_pdf.pdf"'
        response.write(rotated_pdf)

        # Delete the uploaded file
        os.remove(save_path)

        return response

    return render(request, 'pdf_app/rotate.html')


def rotate_pages(pdf_path, rotation_degree, rotation_pages):
    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(pdf_path)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]

        # Rotate the specified pages by the given degree
        if str(page_num + 1) in rotation_pages:
            page.rotate(rotation_degree)

        pdf_writer.add_page(page)

    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    rotated_pdf = output_stream.getvalue()
    output_stream.close()

    return rotated_pdf
