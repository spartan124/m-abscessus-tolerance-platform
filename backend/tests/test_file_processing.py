import csv
import os
import tempfile
import pytest

from app.services.file_handler import FileHandler
from app.services.crispr_processor import CrisprProcessor
from app.services.tnseq_processor import TnseqProcessor
from app.services.image_processor import ImageProcessor


def make_crispr_csv(tmpdir: str) -> str:
    path = os.path.join(tmpdir, "crispr_data.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["gene", "guide_rna", "score", "control", "treatment"])
        writer.writeheader()
        writer.writerows([
            {"gene": "embB", "guide_rna": "g1", "score": "3.2", "control": "100", "treatment": "25"},
            {"gene": "embB", "guide_rna": "g2", "score": "2.8", "control": "100", "treatment": "30"},
            {"gene": "inhA", "guide_rna": "g1", "score": "-1.5", "control": "100", "treatment": "80"},
            {"gene": "kasA", "guide_rna": "g1", "score": "4.1", "control": "100", "treatment": "10"},
        ])
    return path


def make_tnseq_csv(tmpdir: str) -> str:
    path = os.path.join(tmpdir, "tnseq_data.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["position", "gene", "read_count"])
        writer.writeheader()
        writer.writerows([
            {"position": "100", "gene": "embB", "read_count": "5"},
            {"position": "200", "gene": "inhA", "read_count": "1200"},
            {"position": "300", "gene": "kasA", "read_count": "3"},
            {"position": "400", "gene": "recA", "read_count": "800"},
        ])
    return path


def test_file_handler_validate_extension():
    handler = FileHandler()
    assert handler.validate_extension("data.csv", "crispr") is True
    assert handler.validate_extension("image.tiff", "imaging") is True
    assert handler.validate_extension("data.bam", "tnseq") is True
    assert handler.validate_extension("data.exe", "crispr") is False


def test_file_handler_parse_csv():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_crispr_csv(tmpdir)
        handler = FileHandler()
        rows = handler.parse_csv(path)
        assert len(rows) == 4
        assert rows[0]["gene"] == "embB"


def test_crispr_normalize_scores():
    proc = CrisprProcessor()
    rows = [
        {"gene": "embB", "guide_rna": "g1", "score": "3.2"},
        {"gene": "inhA", "guide_rna": "g1", "score": "-1.5"},
        {"gene": "kasA", "guide_rna": "g1", "score": "4.1"},
    ]
    normalized = proc.normalize_scores(rows)
    assert len(normalized) == 3
    assert "normalized_score" in normalized[0]


def test_crispr_filter_hits():
    proc = CrisprProcessor()
    rows = [
        {"gene": "embB", "normalized_score": "3.2"},
        {"gene": "inhA", "normalized_score": "0.5"},
        {"gene": "kasA", "normalized_score": "4.1"},
    ]
    hits = proc.filter_hits(rows, threshold=2.0)
    assert len(hits) == 2
    assert all(abs(float(h["normalized_score"])) >= 2.0 for h in hits)


def test_crispr_process_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_crispr_csv(tmpdir)
        proc = CrisprProcessor()
        result = proc.process_file(path)
        assert "total_guides" in result
        assert result["total_guides"] == 4
        assert "top_genes" in result


def test_tnseq_normalize():
    proc = TnseqProcessor()
    rows = [
        {"position": "100", "gene": "embB", "read_count": "500"},
        {"position": "200", "gene": "inhA", "read_count": "1500"},
    ]
    normalized = proc.normalize_by_library_size(rows, total_reads=2000)
    assert "rpm" in normalized[0]
    assert abs(normalized[0]["rpm"] - 250000.0) < 0.1


def test_tnseq_call_essential():
    proc = TnseqProcessor()
    rows = [
        {"position": "100", "gene": "embB", "read_count": "5", "rpm": "2.5"},
        {"position": "200", "gene": "inhA", "read_count": "1200", "rpm": "600.0"},
    ]
    essential = proc.call_essential_genes(rows, rpm_threshold=10.0)
    assert any(g["gene"] == "embB" and g["is_essential"] for g in essential)
    assert any(g["gene"] == "inhA" and not g["is_essential"] for g in essential)


def test_tnseq_process_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_tnseq_csv(tmpdir)
        proc = TnseqProcessor()
        result = proc.process_file(path)
        assert "total_insertion_sites" in result
        assert result["total_insertion_sites"] == 4
        assert "essential_genes" in result


def test_image_processor_mock():
    proc = ImageProcessor()
    result = proc._mock_tiff_metadata("fake.tiff")
    assert result["format"] == "TIFF"
    assert result["width"] == 512
