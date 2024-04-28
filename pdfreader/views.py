from django.shortcuts import render
from django.http import HttpResponse
from .forms import PdfForm
import PyPDF2
from django.template.loader import render_to_string
import pdfkit

def renderpdf(request):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf']
            pdf_text = extract_text_from_pdf(pdf_file)
            generate_report(pdf_text)
            return render(request, 'report.html', {'pdf_text': pdf_text})
    else:
        form = PdfForm()

    return render(request, 'upload_pdf.html', {'form': form})


def extract_text_from_pdf(pdf_file):
    pdf_text = ''
    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            pdf_text += pdf_reader.getPage(page_num).extractText()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return pdf_text


def generate_report(pdf_text):
    # Render the HTML template with the extracted information
    html_content = render_to_string('report.html', {'extracted_information': pdf_text})

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html_content, False, options=options)

    # Save the PDF file
    with open('vehicle_report.pdf', 'wb') as f:
        f.write(pdf)
