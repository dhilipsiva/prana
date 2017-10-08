from orm_choices import choices, ChoiceUtils

from prana.constants import AC_WATTS, LIGHT_WATTS, MULTIPLIER_CORRIDOR_MAIN, \
    MULTIPLIER_CORRIDOR_SUB


@choices
class SensorCategory(ChoiceUtils):

    class Meta:
        IR = [1, "IR"]
        MOTION = [2, "Motion"]
        PRESSURE = [3, "Pressure"]


@choices
class ApplianceCategory:

    @classmethod
    def watts(klass, category):
        if category == klass.AC:
            return AC_WATTS
        if category == klass.LIGHT:
            return LIGHT_WATTS
        raise ValueError("Applicance category '%d' does not exist" % category)

    class Meta:
        AC = [1, 'AC']
        LIGHT = [2, 'Light']


@choices
class CorridorCategory(ChoiceUtils):

    @classmethod
    def multiplier(klass, category):
        if category == klass.MAIN:
            return MULTIPLIER_CORRIDOR_MAIN
        if category == klass.SUB:
            return MULTIPLIER_CORRIDOR_SUB
        raise ValueError("Corridor category '%d' does not exist" % category)

    class Meta:
        MAIN = [1, "Main"]
        SUB = [2, "Sub"]


@choices
class DeviceStatus(ChoiceUtils):

    class Meta:
        ON = [1, "ON"]
        OFF = [2, "OFF"]
