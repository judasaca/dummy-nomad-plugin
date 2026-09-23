"""Schema package deliberately named without the `dummy_nomad_plugin` prefix.

The section is built with the low-level `Section`/`Quantity` API instead of
class syntax (`class X(Schema): ...`), because subclassing triggers
`Package.from_module`, which unconditionally resets `Package.name` to the
defining module's dotted path (see `nomad/metainfo/metainfo.py:4103`,
`Package.from_module`). That reset is why pynxtools's own
`Package(name="nexus_data_converter")` (dataconverter.py) never actually
takes effect: that module also defines `class ElnYamlConverter(EntryData)`,
so its package ends up named `pynxtools.nomad.schema_packages.dataconverter`
(prefix `pynxtools`) despite the explicit name. Only building sections
without class subclasses avoids the reset, which is what actually reproduces
a root prefix unrelated to the plugin's own package name.
"""

from nomad.metainfo import Package, Quantity, Section

m_package = Package(name='detached_schema')

DetachedThing = Section(
    name='DetachedThing',
    quantities=[Quantity(name='label', type=str)],
)
m_package.m_add_sub_section(Package.section_definitions, DetachedThing)

m_package.__init_metainfo__()
