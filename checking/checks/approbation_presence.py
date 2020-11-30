class ApprobationPresence:
    name = 'Наличие слайда "Апробация работы"'

    @classmethod
    def check(cls, presentation):
        return "Апробация работы" in presentation.slides_titles
