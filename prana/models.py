from datetime import datetime, timedelta

from prana.constants import SENSOR_TIMEOUT


class BaseModel:
    """
    This is the base on top of which all the actual models are built
    Building has `Floor` as components.
    Floor has `Corridor` as components.
    And so on..

    Usually, we sould have a data store.
    I am just using a simple dict for simplicity
    """
    _components = {}
    _component_prefix = ""
    _component_type = None

    def __init__(self, id):
        """
        Initialize models in runtime ;)
        """
        self.id = id

        if self._component_type is None:
            # Hush now! Don't scare BaseModel!
            return
        # Identify components by thier class names
        component_name = self._component_type.__name__.lower()
        self._component_prefix = component_name + "%d"

        # Make aliases like get_floor, get_floors, init_floors, etc
        # You know, because we can. And its convenient
        setattr(self, "get_%s" % component_name, self.get_component)
        setattr(self, "get_%ss" % component_name, self.get_components)
        setattr(self, "add_%s" % component_name, self.add_component)
        setattr(self, "init_%ss" % component_name, self.init_components)

    def component_key(self, id):
        """
        Generic way of creating component_key
        """
        return self._component_prefix % id

    def get_component(self, id):
        key = self.component_key(id)
        return self._components[key]

    def get_components(self):
        return self._components

    def add_component(self, id):
        key = self.component_key(id)
        if key in self._components:
            raise Exception("Component Already Exists")
        self._components[key] = self._component_type(id)
        return self._components[key]

    def init_components(self, component_count):
        """
        Initialize the components of this model
        """
        for component_id in range(component_count):
            self.add_component(component_id)
        return self._components


class CategoryModel(BaseModel):

    def __init__(self, id, category):
        super(CategoryModel, self).__init__(id)
        self.category = category


class Sensor(CategoryModel):

    def __init__(self, id, category, timeout=SENSOR_TIMEOUT):
        super(Sensor, self).__init__(id, category)
        # While init, make sure `last_activity` is twide the timeout
        # Which ensures we have not received any actionbale activities yet!
        # Thus gicing us a clean slate to work with
        self.last_activity = datetime.now() - timedelta(minutes=2*timeout)

    def register_activity(self, value=None):
        self.last_activity = datetime.now()


class Applicance(CategoryModel):

    _component_type = Sensor

    def __init__(self, id, category):
        super(Applicance, self).__init__(id, category)


class Corridor(CategoryModel):

    _component_type = Applicance

    def __init__(self, id, category):
        super(Corridor, self).__init__(id, category)


class Floor(BaseModel):

    _component_type = Corridor

    def __init__(self, id):
        super(Floor, self).__init__(id)


class Building(BaseModel):

    _component_type = Floor

    def __init__(self):
        super(Building, self).__init__(id)
