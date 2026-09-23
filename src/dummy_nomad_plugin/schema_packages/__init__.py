from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from dummy_nomad_plugin.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
)


class DetachedSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from dummy_nomad_plugin.schema_packages.detached_schema import m_package

        return m_package


detached_schema_package_entry_point = DetachedSchemaPackageEntryPoint(
    name='DetachedSchema',
    description=(
        'Schema package registered under a root prefix unrelated to the '
        'dummy_nomad_plugin package name, to reproduce the pynxtools edge case.'
    ),
)
