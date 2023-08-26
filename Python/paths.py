from pathlib import Path


class Paths:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.incoming_dir = self.project_dir / "incoming"
        self.outgoing_dir = self.project_dir / "outgoing"
        self.diffed_pdf = self.outgoing_dir / "diffed.pdf"
        self.build_dirs(self.incoming_dir, self.outgoing_dir)
        self.clean_dirs(self.outgoing_dir)

    @staticmethod
    def build_dirs(*args):
        for arg in args:
            arg.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clean_dirs(*args):
        for arg in args:
            for file in arg.glob("*"):
                file.unlink()


paths = Paths()
