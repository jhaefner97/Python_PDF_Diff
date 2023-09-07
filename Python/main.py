import pdf_tools


class App:

    def __init__(self):
        self.pdf_data_objs = []

    def main(self) -> None:
        for input_doc in pdf_tools.iterate_over_incoming_pdf_files():
            self.pdf_data_objs.append(pdf_tools.read_pdf(input_doc))
        differ = pdf_tools.Differ(self.pdf_data_objs[0], self.pdf_data_objs[1])
        differ.compare()
        differ.annotate_diffs()


if __name__ == '__main__':
    app = App()
    app.main()
