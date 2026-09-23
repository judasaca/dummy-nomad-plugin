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

import numpy as np
import plotly.graph_objects as go
from nomad.config import config
from nomad.datamodel.data import Schema, ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import File, Quantity, SchemaPackage, SubSection
from nomad.metainfo.elasticsearch_extension import Elasticsearch

configuration = config.get_plugin_entry_point(
    'dummy_nomad_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()

class Sample(ArchiveSection):
    sample_id = Quantity(type=str)

class NewSchemaPackage(PlotSection, Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    popular_weight = Quantity(
        type=int, a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity)
    )
    message = Quantity(type=str)
    file_with_file_type = Quantity(
        type=File,
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )
    file_with_file_string_type = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )
    custom_tags = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
            props={
            "direction": "horizontal",
        }),
        shape=['*'],
        a_elasticsearch=Elasticsearch(many_all=True),
    )
    samples = SubSection(section=Sample, repeats=True)
    time = Quantity(type=np.float64, shape=['*'], unit='s')
    frequencies = Quantity(type=np.float64, shape=['n_signals'], unit='Hz')
    signals = Quantity(type=np.float64, shape=['n_signals', '*'])

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        print('RUNNING SCHEMA NORMALIZER ------------------->', archive.results)

        logger.info('NewSchema.normalize', parameter=configuration.parameter)
        #logger.error(
        #    'NewSchema.normalize.test',
        #    data=archive.data,
        #    results=archive.results.eln,
        #    tabular_tree=archive.tabular_tree,
        #    #md_def_0=archive.m_def.m_to_dict(),
        #    file_with_file_type=archive.data.file_with_file_type,
        #    #file_with_file_type_functions=dir(archive.data.file_with_file_type),
        #    type_of_file_with_file_type=type(archive.data.file_with_file_type),
        #    separator='-----------------------',
        #    file_with_file_string_type=archive.data.file_with_file_string_type,
        #    #file_with_file_string_type_functions=dir(
        #    #    archive.data.file_with_file_string_type
        #    #),
        #    type_of_file_with_string_type=type(archive.data.file_with_file_string_type),
        #)

        self.message = f'Hello {self.name}!'
        self.samples = [
            Sample(sample_id=f'sample_{x}') for x in range(437)
        ]

        # Fake data: several noisy damped sine waves with different frequencies.
        rng = np.random.default_rng(seed=42)
        time = np.linspace(0, 10, 200)
        frequencies = np.array([0.3, 0.5, 0.8, 1.2])
        signals = np.exp(-0.2 * time) * np.sin(
            2 * np.pi * frequencies[:, np.newaxis] * time
        )
        signals += rng.normal(scale=0.05, size=signals.shape)
        self.time = time
        self.frequencies = frequencies
        self.signals = signals

        figure = go.Figure(
            data=[
                go.Scatter(x=time, y=signal, mode='lines', name=f'{frequency} Hz')
                for frequency, signal in zip(frequencies, signals)
            ]
        )
        figure.update_layout(
            title='Fake signals',
            legend_title='frequency',
            xaxis_title='time (s)',
            yaxis_title='signal',
            showlegend=True,
        )
        self.figures = [
            PlotlyFigure(label='Fake signals', index=0, figure=figure.to_plotly_json())
        ]


m_package.__init_metainfo__()
