import time
from prana.models import Building
from prana.enums import CorridorCategory, ApplianceCategory, SensorCategory, \
     ApplianceStatus


NUMBER_OF_FLOORS = 2
NUMBER_OF_MAIN_COORRIDORS = 1
NUMBER_OF_SUB_COORRIDORS = 2

b = Building()
corridor_categories = [CorridorCategory.MAIN] * NUMBER_OF_MAIN_COORRIDORS \
    + [CorridorCategory.SUB] * NUMBER_OF_SUB_COORRIDORS

for floor_id in range(NUMBER_OF_FLOORS):
    f = b.add_floor(floor_id)
    for corridor_category in corridor_categories:
        c = f.append_corridor(corridor_category)
        c.append_appliance(ApplianceCategory.AC)
        c.append_appliance(ApplianceCategory.LIGHT)
        c.append_sensor(SensorCategory.MOTION)

b.boot()

# Target AC: Floor 1 Subcorridor 1 AC 1
target_light = b.get_floor(0).get_corridor(1).get_appliance(1)
# Expendable AC: Floor 1 Subcorridor 2 AC 1
expendable_ac = b.get_floor(0).get_corridor(2).get_appliance(0)
print("\n")
print("=" * 80)
print("BEFORE ACTIVITY:")
print("CURRENT WATTS: ", f.current_watts(), "  MAX WATTS: ", f.max_watts())
print("Target Light State", ApplianceStatus.lookup(target_light.status))
print("Expendable AC State", ApplianceStatus.lookup(expendable_ac.status))

b.register_activity(0, 1, 0)  # Activity at Floor 1, Sub corridor 2, sensor 1
print("\n")
print("=" * 80)
print("After ACTIVITY:")
print("CURRENT WATTS: ", f.current_watts(), "  MAX WATTS: ", f.max_watts())
print("Target Light State", ApplianceStatus.lookup(target_light.status))
print("Expendable AC State", ApplianceStatus.lookup(expendable_ac.status))

print("Countdown to 30")
for i in range(30):
    print(30-i)
    time.sleep(1)

b.optimize()
print("\n")
print("=" * 80)
print("BEFORE TIMEOUT")
print("Target Light State", ApplianceStatus.lookup(target_light.status))
print("Expendable AC State", ApplianceStatus.lookup(expendable_ac.status))

print("\n")
print("=" * 80)
print("Countdown to 30")
for i in range(30):
    print(30-i)
    time.sleep(1)


b.optimize()
print("\n")
print("=" * 80)
print("AFTER TIMEOUT")
print("Target Light State", ApplianceStatus.lookup(target_light.status))
print("Expendable AC State", ApplianceStatus.lookup(expendable_ac.status))
