from pypdf import PdfReader, PdfWriter
import os
from time import sleep

#Fedex generated shipping label PDFs need data trimmed from the end of the file in order to find the end-of-file statement, required for handling
def reset_eof_of_pdf_return_stream(pdf_stream_in:list):
    # find the line position of the EOF
    for i, x in enumerate(txt[::-1]):
        if b'%%EOF' in x:
            actual_line = len(pdf_stream_in)-i
            print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
            break

    # return the list up to that point
    return pdf_stream_in[:actual_line]


while True:
    list = os.listdir('C:\\Users\\c.jared.eckenstam\\documents')
    for item in list:
        if ".pdf" in item:
            # opens the file for reading
            with open(item, 'rb') as p:
                txt = (p.readlines())


            # get the new list terminating correctly
            txtx = reset_eof_of_pdf_return_stream(txt)

            # write to new pdf
            with open(item, 'wb') as f:
                f.writelines(txtx)

            #load new pdf
            fixed_pdf = PdfReader(item)
            writer = PdfWriter()

            #rotate 90 degrees
            page = fixed_pdf.pages[0].rotate(90)

            #crop to fit label, trim white space
            page.mediabox.upper_right = (
                page.mediabox.right * .91,
                page.mediabox.top * .48,
            )
            page.trimbox.lower_left = (120, 90)
            page.trimbox.upper_right = (556, 556)
            page.cropbox.lower_left = (120, 90)
            page.cropbox.upper_right = (556, 556)

            #create output pdf from modified input pdf
            writer.add_page(page)
            with open("output.pdf","wb") as fp:
                writer.write(fp)

            #clean folder and print output
            os.remove(item)
            os.system('cmd /c "PdftoPrinter.exe output.pdf "ZDesigner ZT411-300dpi ZPL""')
            os.remove('output.pdf')
        sleep(3)