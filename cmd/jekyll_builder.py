class Jekyll:
    def __init__(self, jekyll_repo):
        self.jekyll_repo = jekyll_repo

    def check_if_site(self):
       return "test -e {0} && echo True || echo False".format(self.jekyll_repo)

    def _build(self):
        return "jekyll build"

    