from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import File, Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'dummy_nomad_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class NewSchemaPackage(Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    message = Quantity(type=str)
    test_file_0 = Quantity(
        type=File,
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        logger.info('NewSchema.normalize', parameter=configuration.parameter)
        self.message = f'Hello {self.name}!'


m_package.__init_metainfo__()
