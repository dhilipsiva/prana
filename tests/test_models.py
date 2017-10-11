"""
Just declaring some sample models to test BaseModel
"""

import time

from prana.constants import LIGHT_WATTS
from prana.models import BaseModel, CategoryModel, Appliance,\
    Sensor, Building
from prana.enums import CorridorCategory, ApplianceCategory, SensorCategory, \
     ApplianceStatus


# Test settings
NUMBER_OF_FLOORS = 2
NUMBER_OF_MAIN_COORRIDORS = 1
NUMBER_OF_SUB_COORRIDORS = 2


class Foo(CategoryModel):
    """
    Just a foo model
    """
    pass


class Bar(BaseModel):
    """
    Just a bar model which will have many Foo components
    """
    _component_type = Foo


def test_BaseModel_CategoryModel():
    b = Bar(1)

    # Test for dynamically created functions
    assert hasattr(b, "get_foo")
    assert hasattr(b, "list_foos")
    assert hasattr(b, "add_foo")
    assert hasattr(b, "init_foos")
    assert hasattr(b, "append_foo")
    assert hasattr(b, "filtered_foos")

    # Test for component_key
    component_key = b.component_key(2)
    assert component_key == 'foo2'

    # No components to start with
    assert b.list_foos() == []

    # Init some 2 Foos with category 1
    b.init_foos(2, category=1)
    # add new foo with category 2
    b.append_foo(category=2)
    assert len(b.list_foos()) == 3

    # get a Foo object
    f = b.get_foo(2)
    assert isinstance(f, Foo)
    assert f.id == 2

    # Filter foo bt category 1
    assert len(b.filtered_foos(1)) == 2


def test_Applicance():
    """
    Test our applicance objects
    """

    a = Appliance(id=1, category=ApplianceCategory.LIGHT)
    assert a.status == ApplianceStatus.OFF
    assert a.current_watts() == 0

    a.switch_on()
    assert a.status == ApplianceStatus.ON
    assert a.current_watts() == LIGHT_WATTS


def test_Sensor():
    """
    Test our sensors
    """
    s = Sensor(id=1, category=1, timeout=1)
    assert s.is_active() is False


def test_integration():
    """
    Previos tests are unit tests. This one is sort of like an
    integration test :P
    """
    b = Building()
    corridor_categories = \
        [CorridorCategory.MAIN] * NUMBER_OF_MAIN_COORRIDORS \
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
    assert f.current_watts() == 35
    assert f.max_watts() == 35
    assert target_light.status == ApplianceStatus.OFF
    assert expendable_ac.status == ApplianceStatus.ON

    # Activity at Floor 1, Sub corridor 2, sensor 1
    b.register_activity(0, 1, 0)
    assert f.current_watts() == 35
    assert f.max_watts() == 35
    assert target_light.status == ApplianceStatus.ON
    assert expendable_ac.status == ApplianceStatus.OFF

    print("Countdown to 30")
    for i in range(30):
        print(30-i)
        time.sleep(1)

    b.refresh()
    assert f.current_watts() == 35
    assert f.max_watts() == 35
    assert target_light.status == ApplianceStatus.ON
    assert expendable_ac.status == ApplianceStatus.OFF

    print("Countdown to 30")
    for i in range(30):
        print(30-i)
        time.sleep(1)

    b.refresh()
    assert f.current_watts() == 35
    assert f.max_watts() == 35
    assert target_light.status == ApplianceStatus.OFF
    assert expendable_ac.status == ApplianceStatus.ON
