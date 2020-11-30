class RelevancePresence:
    name = 'Наличие слайда с актуальностью работы'

    @classmethod
    def check(cls, presentation):
        for title in presentation.slides_titles:
            if "актуальность" in str.lower(title):
                return True
        return False
