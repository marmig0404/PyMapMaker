import helpers
import running
from address2img import Generator

__author__ = "Martin Miglio"
__credits__ = "Mapnik Community"
__license__ = "GNU LGPL"
__version__ = "1.0.0"
__maintainer__ = "Martin Miglio"
__email__ = "marmig0404@gmail.com"
__status__ = "Production"

running.start_process()

address_database = helpers.get_database_config("address")
map_database = helpers.get_database_config("map")
data_sources = [
    map_database,
]
output_directory = helpers.get_config("General Config", "Output Location")
addresses = address_database.get_addresses()
map_style = helpers.get_config("Map Image Config", "Style Sheet")
map_settings_keys = ['']
map_settings = helpers.get_all_config("Map Image Config", )
map_renderer = Renderer(data_sources, map_style, map_settings)
map_renderer.render(addresses, output_directory)

running.end_process()
