from __future__ import annotations
from beanie import Document, init_beanie
from pydantic import BaseModel, Field, HttpUrl, ConfigDict, model_validator
from datetime import date
from enum import Enum
from typing import Any, List, Optional
from uuid import UUID
from pymongo import AsyncMongoClient
import asyncio
import streamlit as st

MONGODB_CONNECTION_STRING = f"mongodb+srv://{st.secrets['MONGODB_USERNAME']}:{st.secrets['MONGODB_PASSWORD']}@{st.secrets['MONGODB_URI']}"


class Release(BaseModel):
    id: UUID
    releaseNumber: str
    releaseDate: date
    approvalProcess: ApprovalProcess
    currency: Currency
    currencyChangeDate: date
    iscApprovalDate: Optional[date] = None
    ministerialAgreementDate: Optional[date] = None
    nqcEndorsementDate: Optional[date] = None
    links: List[dict[str, Any]] = Field(default_factory=list)

class Currency(str, Enum):
    CURRENT = "current"
    REPLACED = "replaced"

class ApprovalProcess(str, Enum):
    NQC_PROCESS = "nqcProcess"
    ISC_UPGRADE = "iscUpgrade"

class Parent(BaseModel):
    id: UUID
    title: str

class TrainingPackageDeveloper(BaseModel):
    name: str
    organisationId: UUID
    webAddresses: List[HttpUrl] = Field(default_factory=list)

class MappingInformation(BaseModel):
    code: str
    id: UUID
    date: date
    isEquivalent: bool
    mapsToCode: str
    mapsToId: UUID
    mapsToTitle: str
    title: str


class TrainingPackage(Document):
#class TrainingPackage(BaseModel):
    # Accept JSON key "id" as domain_id to avoid clashing with MongoDB _id
    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def map_external_id(cls, data):
        # Remap top-level 'id' from JSON to 'domain_id' to avoid clashing with Beanie's 'id'
        if isinstance(data, dict) and "id" in data and "domain_id" not in data:
            data = data.copy()
            data["domain_id"] = data.pop("id")
        return data

    domain_id: UUID
    code: str
    developmentStandard: str
    mappingInformation: List[dict[str, Any]] = Field(default_factory=list)
    parent: Parent
    releases: List[Release] = Field(default_factory=list)
    reviewDate: Optional[date] = None
    title: str
    trainingPackageDeveloper: TrainingPackageDeveloper
    type: str
    usageRecommendation: str
    usageRecommendationLabel: str

    class Settings:
        name = "training_packages"

    @property
    def external_id(self) -> UUID:
        return self.domain_id


async def _init_beanie():
    mongodbclient = AsyncMongoClient(MONGODB_CONNECTION_STRING)
    await init_beanie(database=mongodbclient.tga, document_models=[TrainingPackage])

async def main():
    await _init_beanie()
    data = {'code': 'ICT', 'developmentStandard': 'streamline', 'id': '3f36b521-35ac-4943-8b27-037127281c92', 'mappingInformation': [{'code': 'ICT', 'id': '3f36b521-35ac-4943-8b27-037127281c92', 'date': '2016-01-14', 'isEquivalent': False, 'mapsToCode': 'ICA11', 'mapsToId': '0692ba2e-54d8-47c1-a55f-83ace0ad71eb', 'mapsToTitle': 'Information and Communications Technology Training Package', 'title': 'Information and Communications Technology'}, {'code': 'ICT', 'id': '3f36b521-35ac-4943-8b27-037127281c92', 'date': '2015-03-06', 'isEquivalent': False, 'mapsToCode': 'ICT10', 'mapsToId': '9f6e9c25-6a6e-4d6b-a0f6-554ee24f79a2', 'mapsToTitle': 'Integrated Telecommunications Training Package', 'title': 'Information and Communications Technology'}], 'parent': {'id': '109c72a5-f546-4966-bb1d-7b1164ceaf0a', 'title': 'Information and Communications Technology'}, 'releases': [{'approvalProcess': 'iscUpgrade', 'currency': 'current', 'currencyChangeDate': '2025-06-20', 'id': '7d6929c5-e986-42d7-a39a-3e8109cfcd23', 'links': [], 'releaseDate': '2025-06-20', 'releaseNumber': '9.1'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2024-12-17', 'id': 'b5a5e50c-979b-49e7-829a-e922c4cbd710', 'iscApprovalDate': '2024-12-17', 'links': [], 'ministerialAgreementDate': '2024-12-10', 'nqcEndorsementDate': '2024-12-10', 'releaseDate': '2024-12-17', 'releaseNumber': '9.0'}, {'approvalProcess': 'iscUpgrade', 'currency': 'replaced', 'currencyChangeDate': '2022-06-22', 'id': '9f901fd8-732b-4a62-aebe-2ae56d4ad233', 'iscApprovalDate': '2022-06-21', 'links': [], 'releaseDate': '2022-06-21', 'releaseNumber': '8.1'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2022-02-04', 'id': 'b7e2d116-2bbe-4fb9-88c4-a5916b5efa7e', 'iscApprovalDate': '2022-02-04', 'links': [], 'ministerialAgreementDate': '2021-11-17', 'nqcEndorsementDate': '2021-11-17', 'releaseDate': '2022-02-03', 'releaseNumber': '8.0'}, {'approvalProcess': 'iscUpgrade', 'currency': 'replaced', 'currencyChangeDate': '2021-04-09', 'id': 'e3e79338-c947-4799-aee2-6950238b6376', 'iscApprovalDate': '2021-04-09', 'links': [], 'releaseDate': '2021-04-09', 'releaseNumber': '7.2'}, {'approvalProcess': 'iscUpgrade', 'currency': 'replaced', 'currencyChangeDate': '2021-02-13', 'id': 'ad367083-d1d7-45d3-a034-c4b27fd4c88f', 'iscApprovalDate': '2021-02-12', 'links': [], 'releaseDate': '2021-02-12', 'releaseNumber': '7.1'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2021-01-19', 'id': 'bdbb4c66-4814-42dd-bd23-489eac09911b', 'iscApprovalDate': '2021-01-19', 'links': [], 'ministerialAgreementDate': '2021-01-18', 'nqcEndorsementDate': '2020-12-02', 'releaseDate': '2021-01-19', 'releaseNumber': '7.0'}, {'approvalProcess': 'iscUpgrade', 'currency': 'replaced', 'currencyChangeDate': '2020-10-03', 'id': '5724f340-ef5a-4c95-ab45-3e6fd0361afd', 'iscApprovalDate': '2020-10-02', 'links': [], 'releaseDate': '2020-10-02', 'releaseNumber': '6.1'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2020-07-22', 'id': 'cc3806c1-e98a-43f6-b84b-804bcdb888c5', 'iscApprovalDate': '2020-07-22', 'links': [], 'ministerialAgreementDate': '2020-07-14', 'nqcEndorsementDate': '2020-06-18', 'releaseDate': '2020-07-21', 'releaseNumber': '6.0'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2019-08-31', 'id': '76f3fa05-1411-4e67-bc0e-7a9959c27bf8', 'iscApprovalDate': '2019-08-31', 'links': [], 'ministerialAgreementDate': '2019-03-26', 'nqcEndorsementDate': '2019-03-26', 'releaseDate': '2019-08-30', 'releaseNumber': '5.0'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2019-01-30', 'id': '36d8e307-a8fa-4df9-bfae-d4fe18659c95', 'iscApprovalDate': '2019-01-30', 'links': [], 'ministerialAgreementDate': '2018-08-14', 'nqcEndorsementDate': '2018-08-14', 'releaseDate': '2019-01-30', 'releaseNumber': '4.0'}, {'approvalProcess': 'iscUpgrade', 'currency': 'replaced', 'currencyChangeDate': '2016-09-14', 'id': '03a53679-8cbf-4389-b4e4-db6704dd0b52', 'iscApprovalDate': '2016-09-13', 'links': [], 'releaseDate': '2016-09-13', 'releaseNumber': '3.1'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2016-01-18', 'id': 'dbf89af8-805e-46b8-9c1d-d4f924ab022d', 'iscApprovalDate': '2016-01-18', 'links': [], 'ministerialAgreementDate': '2015-12-21', 'nqcEndorsementDate': '2015-12-01', 'releaseDate': '2016-01-18', 'releaseNumber': '3.0'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2016-01-15', 'id': '5cd488bf-112d-4985-a616-57672d462365', 'iscApprovalDate': '2016-01-15', 'links': [], 'ministerialAgreementDate': '2015-10-12', 'nqcEndorsementDate': '2015-10-12', 'releaseDate': '2016-01-14', 'releaseNumber': '2.0'}, {'approvalProcess': 'nqcProcess', 'currency': 'replaced', 'currencyChangeDate': '2015-03-27', 'id': '614c048b-146a-431a-953c-a7506ac114d3', 'iscApprovalDate': '2015-03-27', 'links': [], 'nqcEndorsementDate': '2015-03-06', 'releaseDate': '2015-03-25', 'releaseNumber': '1.0'}], 'reviewDate': '2026-12-17', 'title': 'Information and Communications Technology', 'trainingPackageDeveloper': {'name': 'Future Skills Organisation', 'organisationId': '7683909a-6ebd-46b0-8fd9-7cefb78f27e9', 'webAddresses': ['https://www.futureskillsorganisation.com.au/']}, 'type': 'trainingPackage', 'usageRecommendation': 'current', 'usageRecommendationLabel': 'Current'}
    tp = TrainingPackage(**data)
    print(tp)

if __name__ == "__main__":
    asyncio.run(main())
