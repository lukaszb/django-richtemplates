from livesettings.values import MultipleStringValue
from richtemplates.widgets import RichCheckboxSelectMultiple

class RichMultipleStringValue(MultipleStringValue):

    def choice_field(self, **kwargs):
        kwargs['widget'] = RichCheckboxSelectMultiple()
        return super(RichMultipleStringValue, self).choice_field(**kwargs)

