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
from typing import (
    TYPE_CHECKING
)
from nomad.metainfo import (
    Quantity,
)
from nomad.parsing import MatchingParser, MatchingParserInterface
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
)
from nomad.metainfo import (Quantity, SubSection)

from nomad.datamodel.data import (
    EntryData,
)
from nomad.datamodel.metainfo.eln import PublicationReference

from nomad_mof.utils import create_archive
from nomad_mof import MOFData

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
import json


# class MOFDataFile(EntryData):
#     '''
#     Section for a XRD data file.
#     '''
#     mof = Quantity(
#         type=MOFData,
#         a_eln=ELNAnnotation(
#             component='ReferenceEditQuantity',
#         )
#     )


class MOFParser(MatchingParser):
    '''
    Parser for matching MOF files and creating instances of MOFs.
    '''

    def __init__(self):
        super().__init__(
            code_name='MOF Parser'
        )

    def is_mainfile(self, **kwargs):
        is_mainfile = super().is_mainfile(**kwargs)
        print("checker", is_mainfile, kwargs)
        if is_mainfile:
            filename = kwargs.get('filename')
            print('This is filename', filename)
            if filename is not None:
                try:
                    data = json.load(filename)
                    structure_file = data.get(
                        "mof_atoms", {}).get("structure_file")
                    if structure_file:
                        self.creates_children = True
                        return [structure_file]
                except Exception:
                    pass
        return is_mainfile

    def parse(
        self, mainfile: str, archive: 'EntryArchive', logger=None, child_archives=None
    ) -> None:
        data_file = mainfile.split('/')[-1]
        
        entry = MOFData.m_from_dict(MOFData.m_def.a_template)
        entry.data_file = data_file
        file_name = f'{"".join(data_file.split(".")[:-1])}.archive.json'
        archive.data = MOFDataFile(
            mof=create_archive(entry, archive, file_name))
        archive.metadata.entry_name = f'{data_file} data file'
        print('This is child', child_archives)
