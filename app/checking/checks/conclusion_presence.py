class ConclusionPresence:
    name = 'Наличие слайда "Заключение"'

    @classmethod
    def check(cls, presentation):
        return "Заключение" in presentation.slides_titles
