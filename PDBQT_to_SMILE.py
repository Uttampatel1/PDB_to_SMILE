import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
import openbabel

def convert_pdbqt_to_pdb(pdbqt_content):
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdbqt", "pdb")
    
    mol = openbabel.OBMol()
    obConversion.ReadString(mol, pdbqt_content)
    
    pdb_content = obConversion.WriteString(mol)
    return pdb_content

def convert_to_smiles(file_content, file_type):
    if file_type == 'pdb':
        mol = Chem.MolFromPDBBlock(file_content, sanitize=True)
    elif file_type == 'pdbqt':
        pdb_content = convert_pdbqt_to_pdb(file_content)
        mol = Chem.MolFromPDBBlock(pdb_content, sanitize=True)
    else:
        return None
    
    if mol is None:
        return None

    smiles = Chem.MolToSmiles(mol)
    return smiles

def main():
    st.title("PDB/PDBQT to SMILES Converter")
    
    uploaded_files = st.file_uploader("Upload PDB or PDBQT files", type=['pdb', 'pdbqt'], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.name.split('.')[-1]
            file_content = uploaded_file.getvalue().decode("utf-8")
            
            smiles = convert_to_smiles(file_content, file_type)
            
            if smiles:
                st.write(f"## SMILES String for {uploaded_file.name}:")
                st.write(smiles)
            else:
                st.error(f"Could not convert {uploaded_file.name} to a SMILES string.")
    
    st.markdown("""
        ### Instructions:
        1. Upload `.pdb` or `.pdbqt` files using the uploader above.
        2. The app will parse each file and display the corresponding SMILES string.
    """)

if __name__ == "__main__":
    main()
