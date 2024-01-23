#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import numpy as np
from nomad.metainfo import ( Package, Quantity, SubSection, Section)
from nomad.datamodel.data import EntryData, ArchiveSection, UseCaseElnCategory
from nomad.datamodel.metainfo.eln import ElnWithStructureFile, PublicationReference
from nomad.datamodel.metainfo.basesections import PubChemPureSubstanceSection
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)

m_package = Package(name='MOF Schema', version='version_0.0.1')


class MofAtoms(ElnWithStructureFile):
    pass


class TimeQuantity(ArchiveSection):
    """
    The concentration and unit of each reagent used
    """
    value = Quantity(
        type=np.dtype(np.float64),
        unit='hr',
        description="""
        The time in hours
        """,
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit="hr")
    )
    flag = Quantity(
        type=str,
        description="""
        If a flag is provided, it implies that the time has been converted into
        hours based on the results from the survey.
        """,
        a_eln=dict(component='StringEditQuantity')
    )


class ReagentQuantities(ArchiveSection):
    """
    The concentration and unit of each reagent used
    """
    m_def = Section(label_quantity="mof_reagent_name")

    mof_reagent_name = Quantity(
        type=str,
        description="""
        The name of the reagent used in synthesis. This could be the
        metal precursor, organic ligand or solvent.
        """,
        a_eln=dict(component='StringEditQuantity')
    )

    mass = Quantity(
        type=np.dtype(np.float64),
        unit='g',
        description='The mass of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='g'
        ),
    )

    volume = Quantity(
        type=np.dtype(np.float64),
        unit='litre',
        description='The volume of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='ml'
        ),
    )

    moles = Quantity(
        type=np.dtype(np.float64),
        unit='moles',
        description='The moles of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='millimol'
        ),
    )

    molar_concentration = Quantity(
        type=np.dtype(np.float64),
        unit='molar',
        description='The concentration of the MOF reagent',
        a_eln=ELNAnnotation(
             component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='molar'
        ),
    )


class ExperimentalData(ArchiveSection):
    """
    Experimental data extracted from the Cambridge structural database and from
    journal articles downloaded using the DOI of each MOF extracted from the Cambridge
    structural database. The names of the organic ligands have been intelligently
    extracted from the IUPAC name of each MOF provided in the Cambridge structural database
    and the metal salt, solvent and temperature were computed extracted from journal articles
    using the chemicaldataextractor. The output from the chemical data extractor were process
    to ensure acurate extraction of exact synthetic parameter for each system. Consequently, this
    class maps structures to experimental synthetic conditions
    """

    mof_synthesis_method = Quantity(
        type=str,
        description='Experimental method use in synthesising the MOF',
        a_eln=dict(component='EnumEditQuantity'),
    )

    mof_metal_precursor = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_organic_linker_reagent = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_solvent = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_reaction_quanties = SubSection(
        section_def=ReagentQuantities, repeats=True
    )

    mof_reaction_time = SubSection(
        section_def=TimeQuantity, repeats=True
    )

    mof_reaction_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The temperature at which the reaction takes place. The temperature at which the reaction vessel was heated",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_crystallization_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="Temeprature at which the sample was heated to before crystallization started",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_melting_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The recorded temperature at which the MOF solid turned to liquid",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_stability_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The recorded temperature at which the MOF decomposes",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_drying_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="Temperature at which the MOF was heated to remove all guest molecules",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_synthesis_precaution = Quantity(
        type=str,
        description="Hazard statement, which users should to take into consideration before performing synthesis",
        a_eln=dict(component='RichTextEditQuantity'),
    )


class GeneralMOFData(ArchiveSection):
    """
    General information about MOFs. Some extracted directly from the CSD database
    and others extracted from structural manipulation
    """
    mof_alias = Quantity(
        type=str,
        shape=['*'],
        description='Nickname given to the MOF from the CSD',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_f_factor = Quantity(
        type=np.dtype(np.float64),
        description='The r-factor of the crystal, which is a measure of how well the refined structure matches the powder diffraction pattern',
        a_eln=dict(component='NumberEditQuantity')
    )

    mof_iupac_name = Quantity(
        type=str,
        description="The exact IUPAC name of the MOF extracted from the CSD. Note that there are some errors in the name. So care should be take when using this names since there are a couple of typos",
        a_eln=dict(component='StringEditQuantity')
    )

    mof_topology = Quantity(
        type=str,
        shape=['*'],
        description='Three letter topological symbol obtained from RSCR. This was computed using MOFid python script. We an inbuit implemetation for topological calculation is currently being implement in NOMAD',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_color = Quantity(
        type=str,
        description='colour of the MOF',
        a_eln=dict(component='StringEditQuantity')
    )


class Citation(PublicationReference):
    pass


class MOF(EntryData):
    '''
    '''
    m_def = Section(
        label='MOF Synthetic Condition',
        categories=[UseCaseElnCategory])

    data_authors = Quantity(
        type=str,
        shape=['*'],
        description='The authors',
        a_eln=dict(component='StringEditQuantity', overview=True))

    mof_identifier = Quantity(
        type=str,
        description='The unique identifier for the system in the cambridge structural database',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_source = Quantity(
        type=str,
        description='The source of the MOF',
        a_eln=dict(component='StringEditQuantity'),
    )

    institute = Quantity(
        type=str,
        shape=["*"],
        description='Alias/short name of the home institute of the owner, e.g. `KIT`.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity)
        )


    mof_generalities=SubSection(section_def=GeneralMOFData)
    mof_experimental_synthetic_condition=SubSection(
        section_def=ExperimentalData)
    citation=SubSection(section_def=Citation)
    mof_atoms=SubSection(section_def=MofAtoms)


m_package.__init_metainfo__()
