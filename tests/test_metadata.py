"""
Tests for metadata generation and citation utilities.
"""

import re
import uuid
from datetime import datetime

import pytest

from cognitive_tribunal.utils.metadata import CitationGenerator, MetadataGenerator


def parse_uuid_uri(value):
    assert value.startswith("uuid:")
    return uuid.UUID(value[len("uuid:"):])


def assert_utc_timestamp(value):
    assert value.endswith("Z")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    return parsed


def test_base_metadata_contains_governance_provenance_and_stable_identifiers():
    output = MetadataGenerator.base_metadata(
        data_type="archives",
        module_name="ArchiveScanner",
        source_files=["/archives/source.zip"],
        version="2.1.0",
        license_="CC-BY-4.0",
        attribution="Example Archivist",
    )

    metadata = output["metadata"]

    parse_uuid_uri(metadata["id"])
    assert metadata["type"] == "archives"
    assert metadata["version"] == "2.1.0"
    assert metadata["schema_version"] == MetadataGenerator.SCHEMA_VERSION
    assert metadata["created_at"] == metadata["updated_at"]
    assert_utc_timestamp(metadata["created_at"])
    assert metadata["generator"] == {
        "tool": "cognitive-tribunal",
        "version": MetadataGenerator.TOOL_VERSION,
        "module": "ArchiveScanner",
    }
    assert metadata["provenance"]["source_files"] == ["/archives/source.zip"]
    assert metadata["provenance"]["processing_date"] == metadata["created_at"]
    assert metadata["provenance"]["parameters"] == {}
    assert metadata["license"] == "CC-BY-4.0"
    assert metadata["attribution"] == "Example Archivist"


def test_wrap_data_adds_dublin_core_metadata_without_mutating_payload():
    payload = {"conversations": [{"title": "Genesis"}], "stats": {"total": 1}}

    output = MetadataGenerator.wrap_data(
        data=payload,
        data_type="ai-conversations",
        module_name="AIContextAggregator",
        title="Genesis Conversation Export",
        creator="Cognitive Tribunal Team",
        description="Conversation archive for integration testing",
        source_files=["conversation.json"],
        version="1.2.3",
        license_="CC0-1.0",
        subjects=["ai", "archive"],
    )

    metadata = output["metadata"]
    dublin_core = metadata["dublin_core"]

    assert output["data"] is payload
    assert metadata["type"] == "ai-conversations"
    assert metadata["provenance"]["source_files"] == ["conversation.json"]
    assert dublin_core["dc:title"] == "Genesis Conversation Export"
    assert dublin_core["dc:creator"] == "Cognitive Tribunal Team"
    assert dublin_core["dc:subject"] == ["ai", "archive"]
    assert dublin_core["dc:description"] == "Conversation archive for integration testing"
    assert dublin_core["dc:identifier"] == metadata["id"]
    assert dublin_core["dc:rights"] == "CC0-1.0"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", dublin_core["dc:date"])
    assert "datacite" not in metadata


def test_add_dublin_core_includes_optional_coverage():
    output = MetadataGenerator.base_metadata("bookmarks", "WebBookmarkAnalyzer")

    MetadataGenerator.add_dublin_core(
        output,
        title="Browser Bookmarks",
        creator="User",
        description="Exported browser bookmarks",
        coverage="Temporal: 2024-01 to 2024-12",
    )

    assert (
        output["metadata"]["dublin_core"]["dc:coverage"]
        == "Temporal: 2024-01 to 2024-12"
    )
    assert output["metadata"]["dublin_core"]["dc:subject"] == []


def test_add_datacite_uses_dublin_core_values_and_license_uri():
    output = MetadataGenerator.wrap_data(
        data=[],
        data_type="repos",
        module_name="OrgRepoAnalyzer",
        title="Repository Inventory",
        creator="Ops Team",
        description="Repository state export",
        version="3.0.0",
        license_="MIT",
        subjects=["repositories", "inventory"],
    )

    MetadataGenerator.add_datacite(
        output,
        creators=[{"name": "Doe, Jane", "orcid": "0000-0001-2345-6789"}],
        doi="10.5281/zenodo.1234567",
    )

    datacite = output["metadata"]["datacite"]
    assert datacite["identifier"] == "10.5281/zenodo.1234567"
    assert datacite["identifierType"] == "DOI"
    assert datacite["creators"] == [
        {"name": "Doe, Jane", "orcid": "0000-0001-2345-6789"}
    ]
    assert datacite["titles"] == [{"title": "Repository Inventory"}]
    assert datacite["resourceType"] == "Dataset"
    assert datacite["subjects"] == ["repositories", "inventory"]
    assert datacite["dates"] == [
        {"date": output["metadata"]["created_at"], "dateType": "Created"}
    ]
    assert datacite["version"] == "3.0.0"
    assert datacite["rights"] == [
        {"rights": "MIT", "rightsURI": "https://opensource.org/licenses/MIT"}
    ]


def test_add_datacite_falls_back_to_uuid_and_empty_unknown_license_uri():
    output = MetadataGenerator.base_metadata(
        data_type="exports",
        module_name="ExampleModule",
        license_="LicenseRef-Internal",
    )

    MetadataGenerator.add_datacite(output, creators=[{"name": "Internal User"}])

    datacite = output["metadata"]["datacite"]
    assert datacite["identifier"] == output["metadata"]["id"]
    assert datacite["identifierType"] == "UUID"
    assert datacite["titles"] == [{"title": "Untitled Dataset"}]
    assert datacite["subjects"] == []
    assert datacite["rights"] == [{"rights": "LicenseRef-Internal", "rightsURI": ""}]


def test_update_timestamp_and_processing_steps_mutate_existing_metadata():
    output = MetadataGenerator.base_metadata("archives", "ArchiveScanner")
    original_updated_at = output["metadata"]["updated_at"]

    MetadataGenerator.update_timestamp(output)
    MetadataGenerator.add_processing_step(
        output,
        "classify-files",
        parameters={"max_depth": 3, "include_hidden": False},
    )
    MetadataGenerator.add_processing_step(output, "deduplicate")

    assert output["metadata"]["updated_at"] >= original_updated_at
    steps = output["metadata"]["provenance"]["processing_steps"]
    assert [step["step"] for step in steps] == ["classify-files", "deduplicate"]
    assert steps[0]["parameters"] == {"max_depth": 3, "include_hidden": False}
    assert steps[1]["parameters"] == {}
    for step in steps:
        assert_utc_timestamp(step["timestamp"])


def test_metadata_mutators_ignore_missing_metadata_sections():
    raw = {"data": [1, 2, 3]}

    assert MetadataGenerator.update_timestamp(raw) is raw
    assert MetadataGenerator.add_processing_step(raw, "noop") is raw
    assert raw == {"data": [1, 2, 3]}


def test_citation_formats_from_metadata_with_doi():
    output = MetadataGenerator.wrap_data(
        data={},
        data_type="ai-conversations",
        module_name="AIContextAggregator",
        title="Genesis Conversation Export",
        creator="Doe, Jane",
        description="Conversation archive",
        version="1.2.0",
    )
    output["metadata"]["id"] = "uuid:1234-abcd"
    output["metadata"]["dublin_core"]["dc:date"] = "2026-06-20"
    MetadataGenerator.add_datacite(
        output,
        creators=[{"name": "Doe, Jane"}],
        doi="10.5281/zenodo.7654321",
    )

    assert CitationGenerator.from_metadata(output, "bibtex") == """@dataset{uuid_1234_abcd,
  author = {Doe, Jane},
  title = {Genesis Conversation Export},
  year = {2026},
  publisher = {Cognitive Archaeology Tribunal},
  version = {1.2.0},
  doi = {10.5281/zenodo.7654321}
}"""
    assert CitationGenerator.from_metadata(
        output, "apa"
    ) == (
        "Doe, Jane. (2026). Genesis Conversation Export (Version 1.2.0) "
        "[Data set]. Cognitive Archaeology Tribunal. "
        "https://doi.org/10.5281/zenodo.7654321"
    )
    assert CitationGenerator.from_metadata(
        output, "chicago"
    ) == (
        'Doe, Jane. 2026. "Genesis Conversation Export." Version 1.2.0. '
        "Cognitive Archaeology Tribunal. https://doi.org/10.5281/zenodo.7654321."
    )


def test_citation_generators_include_url_when_doi_is_absent():
    assert CitationGenerator.to_bibtex(
        dataset_id="uuid:abc-def",
        author="Doe, Jane",
        title="Repository Inventory",
        year="2026",
        version="1.0.0",
        url="https://example.test/dataset",
    ) == """@dataset{uuid_abc_def,
  author = {Doe, Jane},
  title = {Repository Inventory},
  year = {2026},
  publisher = {Cognitive Archaeology Tribunal},
  version = {1.0.0},
  url = {https://example.test/dataset}
}"""
    assert CitationGenerator.to_apa(
        "Doe, Jane",
        "2026",
        "Repository Inventory",
        "1.0.0",
        url="https://example.test/dataset",
    ).endswith("https://example.test/dataset")
    assert CitationGenerator.to_chicago(
        "Doe, Jane",
        "2026",
        "Repository Inventory",
        "1.0.0",
        url="https://example.test/dataset",
    ).endswith("https://example.test/dataset.")


def test_from_metadata_rejects_unknown_citation_format():
    with pytest.raises(ValueError, match="Unknown citation format: mla"):
        CitationGenerator.from_metadata({}, "mla")
