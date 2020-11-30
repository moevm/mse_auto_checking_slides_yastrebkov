from .presentation import Presentation
import inspect

class Checker:
    checks = []
    check_names = {}

    @classmethod
    def add(cls, check, id):
        check.id = id
        cls.checks.append(check)

        cls.check_names[id] = check.name

        return check

    @classmethod
    def check(cls, presentation_file, student_degree):
        presentation = Presentation(presentation_file)
        results = []
        for check in Checker.checks:
            check_parameters = {'presentation': presentation}
            if 'student_degree' in inspect.signature(check.check).parameters:
                check_parameters['student_degree'] = student_degree
            results.append({
                'id': check.id,
                'success': check.check(**check_parameters),
            })
        return results
