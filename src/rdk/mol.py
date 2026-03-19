import copy

import numpy as np
import py3Dmol
from PIL.Image import Image
from rdkit import Chem, DistanceGeometry
from rdkit.Chem import AllChem, Descriptors, Draw, Mol, rdDistGeom, rdmolfiles


def mol_from_smiles(smiles: str, with_coords: bool = False) -> Mol:
    """
    Generate an RDKit Mol from a SMILES string.
    """
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)

    if with_coords:
        return with_coordinates(mol)

    return mol

def mol_to_xyz(mol: Mol) -> str:
    """
    Generate an XYZ block from an rdkit Mol.
    """
    return Chem.MolToXYZBlock(mol)


def with_coordinates(
    mol: Mol, in_place: bool = False, bmat: np.ndarray | None = None
) -> Mol:
    """Add coordinates to RDKit molecule, if missing.

    :param mol: RDKit molecule
    :param in_place: Whether to modify the molecule in place
    :return: RDKit molecule
    """
    if bmat is not None or not has_coordinates(mol):
        mol = mol if in_place else copy.deepcopy(mol)

        # Set Distance Geometry (DG) bounds matrix
        bmat = dg_bounds_matrix(mol) if bmat is None else bmat
        params = rdDistGeom.ETKDGv3()
        params.SetBoundsMat(bmat)

        rdDistGeom.EmbedMolecule(mol, params=params)
    return mol


def dg_bounds_matrix(mol: Mol) -> np.ndarray:
    """Get Distance Geometry (DG) bounds matrix.

    The lower triangle contains lower bounds, while the upper triangle contains
    upper bounds.

    :param mol: RDKit molecule
    :return: Distance geometry bounds matrix
    """
    return rdDistGeom.GetMoleculeBoundsMatrix(mol)


def has_coordinates(mol: Mol) -> bool:
    """Determine if RDKit molecule has coordinates.

    :param mol: RDKit molecule
    :return: `True` if it does, `False` if not
    """
    return bool(mol.GetNumConformers())

def view(
    mol: Mol, *, label: bool = True, width: int = 600, height: int = 450
) -> py3Dmol.view:
    """View molecule as a 3D structure.

    :param geo: Geometry
    :param width: Width
    :param height: Height
    """
    xyz_str = Chem.MolToXYZBlock(mol)

    viewer = py3Dmol.view(width=width, height=height)
    viewer.addModel(xyz_str, "xyz")
    viewer.setStyle({"stick": {}, "sphere": {"scale": 0.3}})

    if label:
        for idx in range(mol.GetNumAtoms()):
            viewer.addLabel(
                idx,
                {
                    "backgroundOpacity": 0.0,
                    "fontColor": "black",
                    "alignment": "center",
                    "inFront": True,
                },
                {"index": idx},
            )

    viewer.zoomTo()
    return viewer