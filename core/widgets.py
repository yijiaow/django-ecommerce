from django.forms import widgets


class NumberStepperWidget(widgets.NumberInput):
    template_name = 'widgets/number-stepper.html'

    class Media:
        js = ('js/numberStepper.js')

    # def get_context(self, name, value, min, max, attrs):
    #     context = super().get_context(name, value, attrs)
    #     return context
