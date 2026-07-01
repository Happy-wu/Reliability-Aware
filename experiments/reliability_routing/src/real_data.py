from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from .data import GraphData, standardize


HETERO_UNDIRECTED_DATASETS = (
    "Roman-empire",
    "Amazon-ratings",
    "Minesweeper",
    "Tolokers",
    "Questions",
)
WEBKB_DATASETS = ("Texas", "Cornell", "Wisconsin")
OGB_ORIGINAL_DATASETS = ("OGBN-Arxiv",)
LINKX_CANDIDATE_DATASETS = ("Genius", "Arxiv-year", "Wiki")
WIKICS_DATASETS = ("WikiCS",)
ROC_AUC_DATASETS = (
    "Minesweeper",
    "Tolokers",
    "Questions",
    "Genius",
)
REAL_DATASETS = (
    "Cora",
    "Citeseer",
    "Pubmed",
    "Chameleon",
    "Squirrel",
    "Actor",
    *WEBKB_DATASETS,
    *HETERO_UNDIRECTED_DATASETS,
    *OGB_ORIGINAL_DATASETS,
    *LINKX_CANDIDATE_DATASETS,
    *WIKICS_DATASETS,
)
EDGE_PROTOCOLS = ("undirected", "source_to_target", "target_to_source")


def primary_metric_for_dataset(name: str) -> str:
    if name not in REAL_DATASETS:
        raise ValueError(f"Unknown real dataset: {name}")
    return "roc_auc" if name in ROC_AUC_DATASETS else "accuracy"


@dataclass(frozen=True)
class DatasetExpectation:
    num_nodes: int
    num_edges: int
    num_features: int
    num_classes: int
    num_splits: int
    source: str
    source_url: str


EXPECTED_DATASETS = {
    "Cora": DatasetExpectation(2708, 10556, 1433, 7, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Citeseer": DatasetExpectation(3327, 9104, 3703, 6, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Pubmed": DatasetExpectation(19717, 88648, 500, 3, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Chameleon": DatasetExpectation(2277, 36101, 2325, 5, 10, "PyG WikipediaNetwork Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Squirrel": DatasetExpectation(5201, 217073, 2089, 5, 10, "PyG WikipediaNetwork Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Actor": DatasetExpectation(7600, 30019, 932, 5, 10, "PyG Actor/Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Texas": DatasetExpectation(183, 325, 1703, 5, 10, "PyG WebKB/Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Cornell": DatasetExpectation(183, 298, 1703, 5, 10, "PyG WebKB/Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Wisconsin": DatasetExpectation(251, 515, 1703, 5, 10, "PyG WebKB/Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    # PyG stores both directions after processing these originally undirected
    # edge lists, so the expected edge counts are twice the paper's counts.
    "Roman-empire": DatasetExpectation(22662, 65854, 300, 18, 10, "PyG HeterophilousGraphDataset", "https://github.com/yandex-research/heterophilous-graphs"),
    "Amazon-ratings": DatasetExpectation(24492, 186100, 300, 5, 10, "PyG HeterophilousGraphDataset", "https://github.com/yandex-research/heterophilous-graphs"),
    "Minesweeper": DatasetExpectation(10000, 78804, 7, 2, 10, "PyG HeterophilousGraphDataset", "https://github.com/yandex-research/heterophilous-graphs"),
    "Tolokers": DatasetExpectation(11758, 1038000, 10, 2, 10, "PyG HeterophilousGraphDataset", "https://github.com/yandex-research/heterophilous-graphs"),
    "Questions": DatasetExpectation(48921, 307080, 301, 2, 10, "PyG HeterophilousGraphDataset", "https://github.com/yandex-research/heterophilous-graphs"),
    "OGBN-Arxiv": DatasetExpectation(169343, 1166243, 128, 40, 1, "OGB ogbn-arxiv original subject classification", "https://ogb.stanford.edu/docs/nodeprop/#ogbn-arxiv"),
    "Genius": DatasetExpectation(421961, 984979, 12, 2, 5, "LINKX Non-Homophily-Large-Scale", "https://github.com/CUAI/Non-Homophily-Large-Scale"),
    "Arxiv-year": DatasetExpectation(169343, 1166243, 128, 5, 5, "LINKX / OGB ogbn-arxiv year labels", "https://github.com/CUAI/Non-Homophily-Large-Scale"),
    "WikiCS": DatasetExpectation(11701, 297110, 300, 10, 20, "Wiki-CS dataset data.json directed links", "https://github.com/pmernyei/wiki-cs-dataset"),
    # LINKX wiki is a very large candidate. The exact tensor shapes are
    # validated after downloading because the official files are stored as
    # external Google Drive tensors and no fixed split file is provided.
    "Wiki": DatasetExpectation(0, 0, 0, 0, 5, "LINKX Non-Homophily-Large-Scale wiki", "https://github.com/CUAI/Non-Homophily-Large-Scale"),
}


class CandidateDataset:
    def __init__(self, data: object, raw_paths: list[Path]):
        self.data = data
        self.raw_paths = [str(path) for path in raw_paths]

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index: int) -> object:
        if index != 0:
            raise IndexError(index)
        return self.data


def require_pyg() -> None:
    try:
        import torch_geometric  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "PyTorch Geometric is required for real datasets. "
            "Install it in the server environment before running this script."
        ) from exc


def load_and_validate_dataset(
    name: str,
    root: Path,
    allow_download: bool = True,
) -> tuple[object, dict[str, object]]:
    if name not in REAL_DATASETS:
        raise ValueError(f"Unknown real dataset: {name}")

    dataset = load_pyg_dataset(name, root, allow_download)
    data = dataset[0]
    report = validate_pyg_data(name, dataset, data)
    return data, report


def load_pyg_dataset(name: str, root: Path, allow_download: bool) -> object:
    if name == "Genius":
        return load_genius_candidate(root, allow_download)
    if name == "OGBN-Arxiv":
        return load_ogbn_arxiv_original(root, allow_download)
    if name == "Arxiv-year":
        return load_arxiv_year_candidate(root, allow_download)
    if name == "WikiCS":
        return load_wikics_candidate(root, allow_download)
    if name == "Wiki":
        return load_linkx_wiki_candidate(root, allow_download)

    require_pyg()
    from torch_geometric.datasets import (
        Actor,
        HeterophilousGraphDataset,
        Planetoid,
        WebKB,
        WikipediaNetwork,
    )

    if not allow_download and not dataset_has_local_files(name, root):
        raise FileNotFoundError(
            f"{name} is not present under {root}. Re-run without --no-download."
        )

    if name in {"Cora", "Citeseer", "Pubmed"}:
        pyg_name = existing_planetoid_name(name, root)
        return Planetoid(root=str(root), name=pyg_name, split="public")
    if name in {"Chameleon", "Squirrel"}:
        return WikipediaNetwork(
            root=str(root),
            name=name.lower(),
            geom_gcn_preprocess=True,
        )
    if name == "Actor":
        return Actor(root=str(root / "Actor"))
    if name in WEBKB_DATASETS:
        return WebKB(root=str(root), name=name)
    return HeterophilousGraphDataset(root=str(root), name=name)


def existing_planetoid_name(name: str, root: Path) -> str:
    aliases = {
        "Cora": ("Cora",),
        "Citeseer": ("Citeseer", "CiteSeer"),
        "Pubmed": ("Pubmed", "PubMed"),
    }
    for candidate in aliases[name]:
        if (root / candidate).exists():
            return candidate
    return name


def dataset_has_local_files(name: str, root: Path) -> bool:
    aliases = {
        "Cora": ("Cora",),
        "Citeseer": ("Citeseer", "CiteSeer"),
        "Pubmed": ("Pubmed", "PubMed"),
        "Chameleon": ("chameleon", "Chameleon"),
        "Squirrel": ("squirrel", "Squirrel"),
        "Actor": ("Actor",),
        "Texas": ("texas", "Texas"),
        "Cornell": ("cornell", "Cornell"),
        "Wisconsin": ("wisconsin", "Wisconsin"),
        "Roman-empire": ("roman_empire", "Roman-empire"),
        "Amazon-ratings": ("amazon_ratings", "Amazon-ratings"),
        "Minesweeper": ("minesweeper", "Minesweeper"),
        "Tolokers": ("tolokers", "Tolokers"),
        "Questions": ("questions", "Questions"),
        "OGBN-Arxiv": ("ogb/ogbn_arxiv",),
        "Genius": (
            "linkx/genius",
            "new_candidates/Non-Homophily-Large-Scale/data",
            "Non-Homophily-Large-Scale/data",
        ),
        "Arxiv-year": (
            "ogb/ogbn_arxiv",
            "linkx/arxiv-year",
            "new_candidates/Non-Homophily-Large-Scale/data/splits",
        ),
        "WikiCS": ("wikics", "wiki_cs", "WikiCS"),
        "Wiki": (
            "linkx/wiki",
            "new_candidates/Non-Homophily-Large-Scale/data",
            "Non-Homophily-Large-Scale/data",
        ),
    }
    for candidate in aliases[name]:
        dataset_root = root / candidate
        if not dataset_root.is_dir():
            continue
        for subdir_name in ("raw", "processed"):
            subdir = dataset_root / subdir_name
            if not subdir.is_dir():
                continue
            if any(
                path.is_file() and path.stat().st_size > 0
                for path in subdir.rglob("*")
            ):
                return True
    return False


def validate_pyg_data(name: str, dataset: object, data: object) -> dict[str, object]:
    expected = EXPECTED_DATASETS[name]
    errors: list[str] = []

    actual = {
        "num_nodes": int(data.num_nodes),
        "num_edges": int(data.edge_index.size(1)),
        "num_features": int(data.x.size(1)),
        "num_classes": int(torch.unique(data.y).numel()),
        "num_splits": mask_split_count(data.train_mask),
    }
    for field in ("num_nodes", "num_edges", "num_features", "num_classes", "num_splits"):
        expected_value = getattr(expected, field)
        if name == "Wiki" and expected_value == 0:
            continue
        if actual[field] != expected_value:
            errors.append(f"{field}: expected {expected_value}, got {actual[field]}")

    if data.x.size(0) != data.num_nodes or data.y.numel() != data.num_nodes:
        errors.append("Node feature/label count does not match num_nodes")
    if data.edge_index.dim() != 2 or data.edge_index.size(0) != 2:
        errors.append("edge_index must have shape [2, num_edges]")
    if data.edge_index.numel() and (
        int(data.edge_index.min()) < 0 or int(data.edge_index.max()) >= data.num_nodes
    ):
        errors.append("edge_index contains out-of-range node indices")
    if not torch.isfinite(data.x).all():
        errors.append("Node features contain NaN or Inf")
    if data.y.min().item() < 0:
        errors.append("Labels contain negative values")
    if name in HETERO_UNDIRECTED_DATASETS:
        from torch_geometric.utils import is_undirected

        if not is_undirected(data.edge_index, num_nodes=data.num_nodes):
            errors.append("Official undirected dataset is not stored bidirectionally")

    labels = torch.unique(data.y).cpu()
    if expected.num_classes and not torch.equal(labels, torch.arange(expected.num_classes)):
        errors.append(f"Labels are not contiguous 0..{expected.num_classes - 1}")

    split_report = validate_masks(data, expected.num_splits)
    errors.extend(split_report.pop("errors"))

    raw_files = raw_file_manifest(dataset)
    if not raw_files:
        errors.append("No non-empty raw dataset files were found")

    report = {
        "dataset": name,
        "status": "valid" if not errors else "invalid",
        "source": expected.source,
        "source_url": expected.source_url,
        "officially_undirected": name in HETERO_UNDIRECTED_DATASETS,
        "primary_metric": primary_metric_for_dataset(name),
        "expected": asdict(expected),
        "actual": actual,
        "splits": split_report,
        "raw_files": raw_files,
        "errors": errors,
    }
    if errors:
        raise RuntimeError(
            f"{name} failed dataset validation:\n- " + "\n- ".join(errors)
        )
    return report


def candidate_repo_root(root: Path) -> Path:
    candidates = (
        root / "new_candidates" / "Non-Homophily-Large-Scale",
        root / "Non-Homophily-Large-Scale",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[0]


def load_genius_candidate(root: Path, allow_download: bool) -> CandidateDataset:
    repo = candidate_repo_root(root)
    mat_path = first_existing_path(
        root / "linkx" / "genius" / "genius.mat",
        repo / "data" / "genius.mat",
    )
    splits_path = first_existing_path(
        root / "linkx" / "genius" / "genius-splits.npy",
        repo / "data" / "splits" / "genius-splits.npy",
    )
    ensure_files("Genius", (mat_path, splits_path), allow_download)

    try:
        import scipy.io
    except ImportError as exc:
        raise RuntimeError("Genius loader requires scipy") from exc

    matrix = scipy.io.loadmat(mat_path)
    x = torch.as_tensor(matrix["node_feat"], dtype=torch.float32)
    y = torch.as_tensor(matrix["label"], dtype=torch.long).view(-1)
    edge_index = torch.as_tensor(matrix["edge_index"], dtype=torch.long)
    train_mask, val_mask, test_mask = load_npy_splits(splits_path, y.numel())
    data = SimpleNamespace(
        x=x,
        y=y,
        edge_index=edge_index,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        num_nodes=int(y.numel()),
    )
    return CandidateDataset(data, [mat_path, splits_path])


def load_arxiv_year_candidate(root: Path, allow_download: bool) -> CandidateDataset:
    repo = candidate_repo_root(root)
    splits_path = first_existing_path(
        root / "linkx" / "arxiv-year" / "arxiv-year-splits.npy",
        repo / "data" / "splits" / "arxiv-year-splits.npy",
    )
    if not splits_path.is_file():
        raise FileNotFoundError(
            f"Arxiv-year split file is missing: {splits_path}. "
            "Place CUAI/Non-Homophily-Large-Scale under data/new_candidates."
        )

    ogb_root = root / "ogb"
    if not allow_download and not (ogb_root / "ogbn_arxiv").exists():
        raise FileNotFoundError(
            f"ogbn-arxiv is not present under {ogb_root}. Re-run without --no-download."
        )
    try:
        from ogb.nodeproppred import NodePropPredDataset
    except ImportError as exc:
        raise RuntimeError("Arxiv-year loader requires ogb") from exc

    dataset = load_ogb_node_dataset_compat("ogbn-arxiv", ogb_root)
    graph, _ = dataset[0]
    x = torch.as_tensor(graph["node_feat"], dtype=torch.float32)
    edge_index = torch.as_tensor(graph["edge_index"], dtype=torch.long)
    years = np.asarray(graph["node_year"]).reshape(-1)
    y = torch.as_tensor(even_quantile_labels(years, 5), dtype=torch.long)
    train_mask, val_mask, test_mask = load_npy_splits(splits_path, y.numel())
    raw_paths = [splits_path]
    raw_paths.extend(path for path in (ogb_root / "ogbn_arxiv").rglob("*") if path.is_file())
    data = SimpleNamespace(
        x=x,
        y=y,
        edge_index=edge_index,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        num_nodes=int(y.numel()),
    )
    return CandidateDataset(data, raw_paths[:64])


def load_ogbn_arxiv_original(root: Path, allow_download: bool) -> CandidateDataset:
    ogb_root = root / "ogb"
    if not allow_download and not (ogb_root / "ogbn_arxiv").exists():
        raise FileNotFoundError(
            f"ogbn-arxiv is not present under {ogb_root}. Re-run without --no-download."
        )
    try:
        import ogb  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("OGBN-Arxiv loader requires ogb") from exc

    dataset = load_ogb_node_dataset_compat("ogbn-arxiv", ogb_root)
    graph, labels = dataset[0]
    split_idx = dataset.get_idx_split()
    x = torch.as_tensor(graph["node_feat"], dtype=torch.float32)
    edge_index = torch.as_tensor(graph["edge_index"], dtype=torch.long)
    y = torch.as_tensor(labels, dtype=torch.long).view(-1)
    train_mask = index_mask(split_idx["train"], y.numel())
    val_mask = index_mask(split_idx["valid"], y.numel())
    test_mask = index_mask(split_idx["test"], y.numel())
    raw_paths = [path for path in (ogb_root / "ogbn_arxiv").rglob("*") if path.is_file()]
    data = SimpleNamespace(
        x=x,
        y=y,
        edge_index=edge_index,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        num_nodes=int(y.numel()),
    )
    return CandidateDataset(data, raw_paths[:64])


def load_ogb_node_dataset_compat(name: str, root: Path) -> object:
    from ogb.nodeproppred import NodePropPredDataset

    original_load = torch.load

    def compatible_load(*args, **kwargs):
        kwargs.setdefault("weights_only", False)
        return original_load(*args, **kwargs)

    torch.load = compatible_load
    try:
        return NodePropPredDataset(name=name, root=str(root))
    finally:
        torch.load = original_load


def load_wikics_candidate(root: Path, allow_download: bool) -> CandidateDataset:
    raw_path = wikics_raw_path(root)
    if not raw_path.is_file():
        if allow_download:
            download_wikics(raw_path)
        else:
            raise FileNotFoundError(
                f"WikiCS is not present under {root}. Re-run without --no-download."
            )

    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    x = torch.as_tensor(payload["features"], dtype=torch.float32)
    y = torch.as_tensor(payload["labels"], dtype=torch.long)
    edge_index = wikics_edge_index(payload["links"])
    train_mask = bool_mask_matrix(payload["train_masks"], x.size(0))
    val_key = "val_masks" if "val_masks" in payload else "stopping_masks"
    val_mask = bool_mask_matrix(payload[val_key], x.size(0))
    test_mask = bool_mask_matrix(payload["test_mask"], x.size(0), repeat=train_mask.size(1))
    data = SimpleNamespace(
        x=x,
        y=y,
        edge_index=edge_index,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        num_nodes=int(y.numel()),
    )
    return CandidateDataset(data, [raw_path])


def load_linkx_wiki_candidate(root: Path, allow_download: bool) -> CandidateDataset:
    repo = candidate_repo_root(root)
    data_dir = root / "linkx" / "wiki"
    fallback_data_dir = repo / "data"
    paths = {
        "features": first_existing_path(
            data_dir / "wiki_features2M.pt",
            fallback_data_dir / "wiki_features2M.pt",
        ),
        "edges": first_existing_path(
            data_dir / "wiki_edges2M.pt",
            fallback_data_dir / "wiki_edges2M.pt",
        ),
        "labels": first_existing_path(
            data_dir / "wiki_views2M.pt",
            fallback_data_dir / "wiki_views2M.pt",
        ),
    }
    if not all(path.is_file() for path in paths.values()):
        if allow_download:
            raise FileNotFoundError(
                "LINKX Wiki is very large. Download it explicitly with "
                "prepare_new_candidate_datasets.py --datasets Wiki --download-large."
            )
        raise FileNotFoundError(
            f"LINKX Wiki files are missing under {data_dir}. "
            "Run prepare_new_candidate_datasets.py with --download-large."
        )
    x = torch.load(paths["features"], map_location="cpu", weights_only=False).float()
    edges = torch.load(paths["edges"], map_location="cpu", weights_only=False).long()
    edge_index = edges.t().contiguous() if edges.dim() == 2 and edges.size(1) == 2 else edges
    y_raw = torch.load(paths["labels"], map_location="cpu", weights_only=False)
    y = torch.as_tensor(y_raw, dtype=torch.long).view(-1)
    if torch.unique(y).numel() > 100:
        y = torch.as_tensor(even_quantile_labels(y.cpu().numpy(), 5), dtype=torch.long)
    train_mask, val_mask, test_mask = deterministic_stratified_masks(y, splits=5)
    data = SimpleNamespace(
        x=x,
        y=y,
        edge_index=edge_index,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        num_nodes=int(y.numel()),
    )
    return CandidateDataset(data, list(paths.values()))


def first_existing_path(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    return paths[0]


def ensure_files(name: str, paths: tuple[Path, ...], allow_download: bool) -> None:
    missing = [path for path in paths if not path.is_file()]
    if not missing:
        return
    suffix = " Download is not automatic for this local-candidate file." if allow_download else ""
    raise FileNotFoundError(
        f"{name} is missing required files:\n- "
        + "\n- ".join(str(path) for path in missing)
        + suffix
    )


def load_npy_splits(path: Path, num_nodes: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    splits = np.load(path, allow_pickle=True)
    train_masks = []
    val_masks = []
    test_masks = []
    for item in splits:
        split = item.item() if hasattr(item, "item") else item
        train_masks.append(index_mask(split["train"], num_nodes))
        val_masks.append(index_mask(split.get("valid", split.get("val")), num_nodes))
        test_masks.append(index_mask(split["test"], num_nodes))
    return (
        torch.stack(train_masks, dim=1),
        torch.stack(val_masks, dim=1),
        torch.stack(test_masks, dim=1),
    )


def index_mask(indices: object, num_nodes: int) -> torch.Tensor:
    mask = torch.zeros(num_nodes, dtype=torch.bool)
    idx = torch.as_tensor(indices, dtype=torch.long).view(-1)
    if idx.numel():
        mask[idx] = True
    return mask


def even_quantile_labels(values: np.ndarray, nclass: int) -> np.ndarray:
    values = np.asarray(values).reshape(-1)
    boundaries = np.percentile(values, np.linspace(0, 100, nclass + 1)[1:-1])
    labels = np.zeros(values.shape[0], dtype=np.int64)
    for boundary in boundaries:
        labels += values > boundary
    return labels


def wikics_raw_path(root: Path) -> Path:
    for candidate in (root / "wikics" / "raw" / "data.json", root / "wiki_cs" / "raw" / "data.json"):
        if candidate.is_file():
            return candidate
    return root / "wikics" / "raw" / "data.json"


def download_wikics(raw_path: Path) -> None:
    import urllib.request

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    url = "https://raw.githubusercontent.com/pmernyei/wiki-cs-dataset/master/dataset/data.json"
    urllib.request.urlretrieve(url, raw_path)


def wikics_edge_index(links: object) -> torch.Tensor:
    sources = []
    targets = []
    if isinstance(links, dict):
        iterator = links.items()
    else:
        iterator = enumerate(links)
    for source, neighbors in iterator:
        source_int = int(source)
        for target in neighbors:
            sources.append(source_int)
            targets.append(int(target))
    return torch.tensor([sources, targets], dtype=torch.long)


def bool_mask_matrix(values: object, num_nodes: int, repeat: int | None = None) -> torch.Tensor:
    tensor = torch.as_tensor(values, dtype=torch.bool)
    if tensor.dim() == 1:
        if tensor.numel() != num_nodes:
            raise ValueError(f"Mask length {tensor.numel()} does not match {num_nodes}")
        if repeat is None:
            return tensor.unsqueeze(1)
        return tensor.unsqueeze(1).repeat(1, repeat)
    if tensor.size(0) == num_nodes:
        return tensor
    if tensor.size(1) == num_nodes:
        return tensor.t().contiguous()
    raise ValueError(f"Cannot interpret mask shape {tuple(tensor.shape)} for {num_nodes} nodes")


def deterministic_stratified_masks(
    y: torch.Tensor,
    splits: int,
    train_fraction: float = 0.5,
    val_fraction: float = 0.25,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    rng = np.random.default_rng(0)
    y_np = y.cpu().numpy()
    train_masks = []
    val_masks = []
    test_masks = []
    for split in range(splits):
        rng = np.random.default_rng(split)
        train = torch.zeros(y.numel(), dtype=torch.bool)
        val = torch.zeros(y.numel(), dtype=torch.bool)
        test = torch.zeros(y.numel(), dtype=torch.bool)
        for label in np.unique(y_np):
            idx = np.flatnonzero(y_np == label)
            rng.shuffle(idx)
            train_end = int(round(idx.size * train_fraction))
            val_end = train_end + int(round(idx.size * val_fraction))
            train[torch.from_numpy(idx[:train_end])] = True
            val[torch.from_numpy(idx[train_end:val_end])] = True
            test[torch.from_numpy(idx[val_end:])] = True
        train_masks.append(train)
        val_masks.append(val)
        test_masks.append(test)
    return (
        torch.stack(train_masks, dim=1),
        torch.stack(val_masks, dim=1),
        torch.stack(test_masks, dim=1),
    )


def mask_split_count(mask: torch.Tensor) -> int:
    return 1 if mask.dim() == 1 else int(mask.size(1))


def validate_masks(data: object, expected_splits: int) -> dict[str, object]:
    errors = []
    split_sizes = []
    for split in range(expected_splits):
        train = select_mask(data.train_mask, split)
        val = select_mask(data.val_mask, split)
        test = select_mask(data.test_mask, split)
        if train.dtype != torch.bool or val.dtype != torch.bool or test.dtype != torch.bool:
            errors.append(f"split {split}: masks must be boolean")
        if train.numel() != data.num_nodes or val.numel() != data.num_nodes or test.numel() != data.num_nodes:
            errors.append(f"split {split}: mask length does not match num_nodes")
        if (train & val).any() or (train & test).any() or (val & test).any():
            errors.append(f"split {split}: train/val/test masks overlap")
        if not train.any() or not val.any() or not test.any():
            errors.append(f"split {split}: one or more masks are empty")
        split_sizes.append(
            {
                "split": split,
                "train": int(train.sum()),
                "val": int(val.sum()),
                "test": int(test.sum()),
            }
        )
    return {"count": expected_splits, "sizes": split_sizes, "errors": errors}


def select_mask(mask: torch.Tensor, split: int) -> torch.Tensor:
    return mask if mask.dim() == 1 else mask[:, split]


def raw_file_manifest(dataset: object) -> list[dict[str, object]]:
    entries = []
    for raw_path in getattr(dataset, "raw_paths", []):
        path = Path(raw_path)
        if not path.is_file() or path.stat().st_size == 0:
            continue
        entries.append(
            {
                "path": str(path.resolve()),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return entries


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_graph_data(
    pyg_data: object,
    split: int,
    rw_steps: int,
    rw_samples: int,
    rw_seed: int,
    normalize_features: bool = True,
    edge_protocol: str = "source_to_target",
    cache_path: Path | None = None,
    cache_key: str | None = None,
    primary_metric: str = "accuracy",
) -> GraphData:
    if primary_metric not in {"accuracy", "roc_auc"}:
        raise ValueError(f"Unknown primary metric: {primary_metric}")
    x = pyg_data.x.float()
    if normalize_features:
        x = row_normalize_features(x)
    y = pyg_data.y.long()
    edge_index = apply_edge_protocol(
        pyg_data.edge_index.long(),
        num_nodes=int(pyg_data.num_nodes),
        protocol=edge_protocol,
    )
    cached = load_reliability_cache(cache_path, cache_key)
    if cached is None:
        # Reliability describes the neighbors whose messages are received by
        # each node. PyG edges are source -> target, so group by target.
        reliability_edge_index = edge_index.flip(0)
        reliability_gate, reliability_qk, local_similarity = compute_real_reliability(
            x,
            reliability_edge_index,
            rw_steps=rw_steps,
            rw_samples=rw_samples,
            rw_seed=rw_seed,
        )
        save_reliability_cache(
            cache_path,
            cache_key,
            reliability_gate,
            reliability_qk,
            local_similarity,
        )
    else:
        reliability_gate, reliability_qk, local_similarity = cached
    return GraphData(
        x=x,
        y=y,
        edge_index=edge_index,
        reliability=reliability_gate,
        reliability_gate=reliability_gate,
        reliability_qk=reliability_qk,
        reliability_gate_raw=reliability_gate.clone(),
        reliability_qk_raw=reliability_qk.clone(),
        train_mask=select_mask(pyg_data.train_mask, split).clone(),
        val_mask=select_mask(pyg_data.val_mask, split).clone(),
        test_mask=select_mask(pyg_data.test_mask, split).clone(),
        local_similarity=local_similarity,
        primary_metric=primary_metric,
    )


def apply_edge_protocol(
    edge_index: torch.Tensor,
    num_nodes: int,
    protocol: str,
) -> torch.Tensor:
    if protocol not in EDGE_PROTOCOLS:
        raise ValueError(f"Unknown edge protocol: {protocol}")
    try:
        from torch_geometric.utils import coalesce, to_undirected
    except ImportError as exc:
        raise RuntimeError("Edge protocols require torch-geometric") from exc

    edge_index = edge_index.long()
    if protocol == "undirected":
        return to_undirected(edge_index, num_nodes=num_nodes, reduce="add")
    if protocol == "target_to_source":
        edge_index = edge_index.flip(0)
    return coalesce(edge_index, num_nodes=num_nodes)


def validation_fingerprint(report: dict[str, object]) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(report["actual"], sort_keys=True).encode("utf-8"))
    for item in report["raw_files"]:
        digest.update(str(item["sha256"]).encode("ascii"))
    return digest.hexdigest()


def load_reliability_cache(
    cache_path: Path | None,
    cache_key: str | None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor] | None:
    if cache_path is None or cache_key is None or not cache_path.exists():
        return None
    payload = torch.load(cache_path, map_location="cpu", weights_only=False)
    if payload.get("cache_key") != cache_key:
        return None
    return (
        payload["reliability_gate"],
        payload["reliability_qk"],
        payload["local_similarity"],
    )


def save_reliability_cache(
    cache_path: Path | None,
    cache_key: str | None,
    reliability_gate: torch.Tensor,
    reliability_qk: torch.Tensor,
    local_similarity: torch.Tensor,
) -> None:
    if cache_path is None or cache_key is None:
        return
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "cache_key": cache_key,
            "reliability_gate": reliability_gate,
            "reliability_qk": reliability_qk,
            "local_similarity": local_similarity,
        },
        cache_path,
    )


def row_normalize_features(x: torch.Tensor) -> torch.Tensor:
    if bool((x < 0).any()):
        denominator = x.abs().sum(dim=-1, keepdim=True)
    else:
        denominator = x.sum(dim=-1, keepdim=True)
    return x / denominator.clamp_min(1e-12)


def compute_real_reliability(
    x: torch.Tensor,
    edge_index: torch.Tensor,
    rw_steps: int = 4,
    rw_samples: int = 128,
    rw_seed: int = 0,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    src, dst = edge_index.cpu()
    num_nodes = x.size(0)
    deg = torch.bincount(src, minlength=num_nodes).float()
    deg_feat = standardize(torch.log1p(deg)).unsqueeze(1)

    x_cpu = x.cpu()
    x_norm = torch.nn.functional.normalize(x_cpu, p=2, dim=-1)
    edge_cos = (x_norm[src] * x_norm[dst]).sum(dim=-1)
    sim_sum = torch.zeros(num_nodes).scatter_add_(0, src, edge_cos)
    local_sim = sim_sum / deg.clamp_min(1.0)
    local_sim_feat = standardize(local_sim).unsqueeze(1)

    neigh_sum = torch.zeros_like(x_cpu).scatter_add_(
        0,
        src.unsqueeze(-1).expand(-1, x_cpu.size(1)),
        x_cpu[dst],
    )
    neigh_mean = neigh_sum / deg.clamp_min(1.0).unsqueeze(1)
    centered_sq = (x_cpu[dst] - neigh_mean[src]).pow(2)
    var_sum = torch.zeros_like(x_cpu).scatter_add_(
        0,
        src.unsqueeze(-1).expand(-1, x_cpu.size(1)),
        centered_sq,
    )
    neighbor_variance = (
        var_sum / deg.clamp_min(1.0).unsqueeze(1)
    ).mean(dim=-1)
    neighbor_variance_feat = standardize(neighbor_variance).unsqueeze(1)

    rwse = monte_carlo_rwse(
        edge_index,
        num_nodes=num_nodes,
        rw_steps=rw_steps,
        samples=rw_samples,
        seed=rw_seed,
    )
    reliability_gate = torch.cat(
        [deg_feat, local_sim_feat, neighbor_variance_feat, rwse],
        dim=1,
    )
    reliability_qk = torch.cat([deg_feat, rwse], dim=1)
    return (
        torch.nan_to_num(reliability_gate),
        torch.nan_to_num(reliability_qk),
        local_sim,
    )


def monte_carlo_rwse(
    edge_index: torch.Tensor,
    num_nodes: int,
    rw_steps: int,
    samples: int,
    seed: int,
) -> torch.Tensor:
    if samples < 1:
        raise ValueError("rw_samples must be at least 1")

    src = edge_index[0].cpu().numpy().astype(np.int64, copy=False)
    dst = edge_index[1].cpu().numpy().astype(np.int64, copy=False)
    order = np.argsort(src, kind="stable")
    src = src[order]
    dst = dst[order]
    counts = np.bincount(src, minlength=num_nodes)
    indptr = np.concatenate(([0], np.cumsum(counts)))

    rng = np.random.default_rng(seed)
    starts = np.repeat(np.arange(num_nodes, dtype=np.int64), samples)
    current = starts.copy()
    outputs = []
    for _ in range(rw_steps):
        degree = counts[current]
        next_nodes = current.copy()
        active = degree > 0
        offsets = (rng.random(active.sum()) * degree[active]).astype(np.int64)
        next_nodes[active] = dst[indptr[current[active]] + offsets]
        current = next_nodes
        returns = (current == starts).reshape(num_nodes, samples).mean(axis=1)
        # No-self-loop random walk: isolated nodes have no valid transition
        # and therefore no return event.
        returns[counts == 0] = 0.0
        outputs.append(torch.from_numpy(returns).float().unsqueeze(1))
    return standardize(torch.cat(outputs, dim=1))


def write_validation_report(reports: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")
