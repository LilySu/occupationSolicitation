import aspose.words as aw



# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    # load the PDF file
    doc = aw.Document("ResumeC.pdf")

    # convert PDF to Word DOCX format
    doc.save("ResumeC.docx")
