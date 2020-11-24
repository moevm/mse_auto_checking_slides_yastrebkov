class SlidesAmount:
    name = 'Количество слайдов'

    @classmethod
    def check(cls, presentation, student_degree):
        slides_amount = len(presentation.slides_titles)
        if student_degree == 'master':
            return slides_amount <= 15
        if student_degree == 'bachelor':
            return slides_amount <= 12
        return False
