from .presentation import Presentation

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
    def check(cls, presentation_file):
        presentation = Presentation(presentation_file)
        results = []
        for check in Checker.checks:
            print(check)
            results.append({
                'id': check.id,
                'success': check.check(presentation),
            })
        return results
