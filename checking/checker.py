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
            failure_reasons = []
            if 'failure_reasons' in inspect.signature(check.check).parameters:
                check_parameters['failure_reasons'] = failure_reasons
            result = {
                'id': check.id,
                'success': check.check(**check_parameters),
            }
            if len(failure_reasons) > 0:
                result['failureReasons'] = failure_reasons
            results.append(result)
        return results
