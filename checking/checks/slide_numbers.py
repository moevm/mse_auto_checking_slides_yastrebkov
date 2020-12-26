class SlideNumbers:
    name = 'Номера слайдов'

    @classmethod
    def check(cls, presentation, failure_reasons):
        slide_numbers = presentation.slide_numbers

        if len(slide_numbers) > 0 and slide_numbers[0] is not None:
            failure_reasons.append('На слайде 1 присутствует номер слайда')
            return False
        slide_numbers.pop(0)

        for index, slide_number in enumerate(slide_numbers):
            index += 2
            if slide_number is None:
                failure_reasons.append(f'На слайде {index} отсутсвует номер слайда')
                return False
            if slide_number.index != index:
                failure_reasons.append(f'На слайде {index} неверный номер слайда')
                return False
            if slide_number.right < 0.9 or slide_number.bottom < 0.9:
                failure_reasons.append(f'На слайде {index} неверно расположен номер слайда')
                return False

        return True
