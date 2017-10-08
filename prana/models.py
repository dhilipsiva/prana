from datetime import datetime, timedelta

from prana.constants import SENSOR_TIMEOUT, TIME_SLOT_CURRENT, TIME_SLOT_DAY
from prana.enums import ApplianceCategory, CorridorCategory, ApplianceStatus


class BaseModel:
    """
    This is the base on top of which all the actual models are built
    Building has `Floor` as components.
    Floor has `Corridor` as components.
    And so on..

    FYI: Usually, we sould have a data store.
    I am just using a simple dict for simplicity.
    Would not do this in a real world application. :P
    """
    _components = None
    _component_type = None
    _component_prefix = None

    def __init__(self, id):
        """
        Initialize base & dynamic methods
        """
        self.id = id

        if self._component_type is None:
            # Hush now! Don't scare BaseModel!
            return

        # add methods to models in runtime ;)
        self._components = {}
        # Identify components by thier class names
        component_name = self._component_type.__name__.lower()
        self._component_prefix = component_name + "%d"

        # Make aliases like get_floor, get_floors, init_floors, etc
        # You know, because we can. And its convenient
        setattr(self, "get_%s" % component_name, self.get_component)
        setattr(self, "list_%ss" % component_name, self.list_components)
        setattr(self, "add_%s" % component_name, self.add_component)
        setattr(self, "init_%ss" % component_name, self.init_components)
        setattr(self, "append_%s" % component_name, self.append_component)
        setattr(
            self, "filtered_%ss" % component_name, self.filtered_components)

    def component_key(self, id):
        """
        Generic way of creating component_key
        """
        return self._component_prefix % id

    def get_component(self, id):
        """
        Get a specific component
        """
        key = self.component_key(id)
        return self._components[key]

    def list_components(self):
        """
        List all components
        """
        if self._components is None:
            return []
        return list(self._components.values())

    def filtered_components(self, category):
        """
        Filter component according to category
        """
        return [
            component for component in self.list_components()
            if component.category == category]

    def add_component(self, id, *args, **kwargs):
        """
        Add a component
        """
        key = self.component_key(id)
        if key in self._components:
            raise Exception("Component Already Exists")
        self._components[key] = self._component_type(id, *args, **kwargs)
        return self._components[key]

    def append_component(self, *args, **kwargs):
        """
        A shoutcut to add more components
        """
        component_id = len(self.list_components())
        return self.add_component(component_id, *args, **kwargs)

    def init_components(self, component_count, *args, **kwargs):
        """
        Initialize the components of this model
        """
        for component_id in range(component_count):
            self.add_component(component_id, *args, **kwargs)
        return self._components

    def __str__(self):
        return '%s(%d) {%s}' % (
            self.__class__.__name__, self.id, self.list_components())

    def __repr__(self):
        return '<%s>' % self.__str__()


class CategoryModel(BaseModel):
    """
    Abstract Model to handle category
    """
    def __init__(self, id, category):
        super(CategoryModel, self).__init__(id)
        self.category = category


class Appliance(CategoryModel):
    """
    TV / AC / LIGHTS
    """

    # Appliances are switched off by default
    status = ApplianceStatus.OFF

    def __init__(self, id, category):
        super(Appliance, self).__init__(id, category)

    def switch_on(self):
        """
        Switch on the Appliance
        """
        self.status = ApplianceStatus.ON
        return self.status

    def switch_off(self):
        """
        Switch off the Appliance
        """
        self.status = ApplianceStatus.OFF
        return self.status

    def current_watts(self):
        """
        How many watts is this Appliance consuming at the moment?
        """
        if self.status == ApplianceStatus.OFF:
            return 0
        return ApplianceCategory.watts(self.category)


class Sensor(CategoryModel):
    """
    Motion, Pressure sensor
    """

    def __init__(self, id, category, timeout=SENSOR_TIMEOUT):
        super(Sensor, self).__init__(id, category)
        # While init, make sure `last_activity` is twide the timeout
        # Which ensures we have not received any actionbale activities yet!
        # Thus gicing us a clean slate to work with
        self.last_activity = datetime.now() - timedelta(minutes=2*timeout)

    def register_activity(self, value=None):
        """
        Invoked when given sensor detected an activity
        """
        self.last_activity = datetime.now()
        return self.last_activity

    def is_active(self):
        """
        Has it timed-out since last activity yet?
        """
        expiry = self.last_activity + timedelta(minutes=SENSOR_TIMEOUT)
        return datetime.now() < expiry


class Corridor(CategoryModel):
    """
    Represents both corridors
    """
    _component_type = Appliance
    _sensors = None

    def __init__(self, id, category):
        super(Corridor, self).__init__(id, category)
        self._sensors = {}

    def sensor_key(self, id):
        """
        Generic way of creating component_key
        """
        return "sensor%d" % id

    def get_sensor(self, id):
        key = self.sensor_key(id)
        return self._sensors[key]

    def list_sensors(self):
        return list(self._sensors.values())

    def add_sensor(self, id, sensor_category):
        key = self.sensor_key(id)
        if key in self._sensors:
            raise Exception("Sensor Already Exists")
        self._sensors[key] = Sensor(id, sensor_category)
        return self._sensors[key]

    def append_sensor(self, sensor_category):
        sensor_id = len(self.list_sensors())
        return self.add_sensor(sensor_id, sensor_category)

    def is_active(self):
        """
        Can appliances in this room be optimized?
        """
        sensors = self.list_sensors()
        for sensor in sensors:
            if sensor.is_active():
                return False
        return True

    def optimize(self, appliance_category):
        """
        Try to conserve some energy
        """
        if not self.is_active():
            return
        for appliance in self.filtered_appliances(appliance_category):
            appliance.switch_off()

    def refresh(self):
        """
        Refresh the Appliance status
        """
        if self.is_active():
            return
        for appliance in self.filtered_appliances(ApplianceCategory.LIGHT):
            appliance.switch_off()
        self.boot()

    def switch_on_appliances(self, appliance_category):
        """
        Switch on particular applicances
        """
        for appliance in self.filtered_appliances(appliance_category):
            appliance.switch_on()

    def boot(self):
        """
        First boot
        """
        for appliance in self.filtered_appliances(ApplianceCategory.AC):
            appliance.switch_on()


class Floor(BaseModel):

    _component_type = Corridor

    # Specify the Expendible appliances to switch-off when power usage exceeds
    _appliances_expendable = [
        dict(corridor=CorridorCategory.SUB, appliance=ApplianceCategory.AC),
    ]

    # Appliances that should always be switched on (At night slot)
    _appliances_always_on = [
        dict(
            corridor=CorridorCategory.MAIN, appliance=ApplianceCategory.LIGHT),
    ]

    def __init__(self, id):
        super(Floor, self).__init__(id)

    def max_watts(self):
        """
        Max watts allowed on this floor
        """
        return sum([
            CorridorCategory.multiplier(corridor.category)
            for corridor in self.list_corridors()])

    def current_watts(self):
        """
        Amout of watts consumed at the moment
        """
        watts = 0
        for corridor in self.list_corridors():
            for appliance in corridor.list_appliances():
                watts += appliance.current_watts()
        return watts

    def boot(self):
        if self.current_watts() >= self.max_watts():
            return

        [corridor.boot() for corridor in self.list_corridors()]
        if TIME_SLOT_CURRENT is TIME_SLOT_DAY:
            return
        for rule in self._appliances_always_on:
            for corridor in self.filtered_corridors(rule['corridor']):
                corridor.switch_on_appliances(rule['appliance'])

    def optimize(self):
        """
        Optimize appliances
        """
        if self.current_watts() <= self.max_watts():
            return
        for rule in self._appliances_expendable:
            corridors = self.filtered_corridors(rule['corridor'])
            for corridor in corridors:
                corridor.optimize(rule['appliance'])

    def refresh(self):
        """
        Refresh appliances
        """
        for corridor in self.list_corridors():
            corridor.refresh()


class Building(BaseModel):

    _component_type = Floor

    def __init__(self, id=0):
        super(Building, self).__init__(id)

    def boot(self):
        [floor.boot() for floor in self.list_floors()]

    def optimize(self):
        [floor.optimize() for floor in self.list_floors()]

    def refresh(self):
        [floor.refresh() for floor in self.list_floors()]

    def register_activity(self, floor_id, corridor_id, sensor_id):
        floor = self.get_floor(floor_id)
        corridor = floor.get_corridor(corridor_id)
        sensor = corridor.get_sensor(sensor_id)
        sensor.register_activity()
        return self.optimize()
