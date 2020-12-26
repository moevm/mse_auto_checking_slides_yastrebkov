class SlidesAmount:
    name = 'Количество слайдов'

    @classmethod
    def check(cls, presentation, student_degree, failure_reasons):
        slides_amount = len(presentation.slides_titles)

        max_slides_amount = 0
        min_slides_amount = 0
        if student_degree == 'master':
            max_slides_amount = 15
            min_slides_amount = 9
        elif student_degree == 'bachelor':
            max_slides_amount = 12
            min_slides_amount = 7
        else:
            return True

        if slides_amount > max_slides_amount:
            failure_reasons.append(f'Должно быть не больше {max_slides_amount} слайдов')
            return False

        if slides_amount < min_slides_amount:
            failure_reasons.append(f'Должно быть не меньше {min_slides_amount} слайдов')
            return False

        return True
