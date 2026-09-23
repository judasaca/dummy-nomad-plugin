from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel import ArchiveSection
from nomad.datamodel.data import Quantity

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.normalizing import Normalizer

configuration = config.get_plugin_entry_point(
    'dummy_nomad_plugin.normalizers:normalizer_entry_point'
)
class Sample(ArchiveSection):
    sample_id = Quantity(type=str)


class NewNormalizer(Normalizer):
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        print('RUNNING NORMALIZER NORMALIZE before ------------------->')
        super().normalize(archive, logger)
        print('RUNNING NORMALIZER NORMALIZE ------------------->')
        logger.info('NewNormalizer.normalize', parameter=configuration.parameter)
        if archive.results and archive.results.material:
            archive.results.material.elements = ['C', 'O']

        archive.calculations = [
            Sample(sample_id='sample1'),

        ]
        logger.error(
            'NewNormalizer.normalize', results=archive.results, data=archive.data
        )
        print(
            'NewNormalizer.normalize------------------->', archive.results, archive.data
        )
