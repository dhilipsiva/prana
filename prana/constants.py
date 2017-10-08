# Defaults

AC_COUNT = 1
AC_WATTS = 10
LIGHT_COUNT = 1
LIGHT_WATTS = 5

TIME_SLOT_DAY = (6, 18)  # Assuming 6AM to 6PM is day slot => in 24 hour format
TIME_SLOT_NIGHT = tuple(24 - t for t in TIME_SLOT_DAY)  # what isn't day slot

SENSOR_TIMEOUT = 1  # A timeout for sensors, For 1 minute.

MULTIPLIER_CORRIDOR_MAIN = 15
MULTIPLIER_CORRIDOR_SUB = 10

# Ideally, in the real world, time slot will be decided based on current time
# Since this more of a prgaramming challene,
# I am emulating current time rather than using actual time utils
TIME_SLOT_CURRENT = TIME_SLOT_NIGHT
