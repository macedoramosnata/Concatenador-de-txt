import streamlit as st
from pathlib import Path
import tempfile
import shutil

st.title("📂 Juntar Arquivos .txt de um ZIP")

st.markdown('### Faça o upload da pasta ZIPADA (.zip) contendo os arquivos *.txt* que deseja juntar.')
uploaded_file = st.file_uploader('Escolha o arquivo ZIP:', type='zip')

if uploaded_file is not None:
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Salvar o ZIP no disco temporário
        zip_path = temp_path / "upload.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        # Descompactar o ZIP
        unpacked_folder = temp_path / "descompactado"
        unpacked_folder.mkdir(exist_ok=True)
        shutil.unpack_archive(zip_path, unpacked_folder, 'zip')

        # Pegar todos os arquivos .txt
        arquivos_txt = list(unpacked_folder.rglob("*.txt"))

        if not arquivos_txt:
            st.warning("Nenhum arquivo .txt foi encontrado no ZIP.")
        else:
            resultado_final = ""
            for i, arquivo in enumerate(arquivos_txt):
                with open(arquivo, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                    if i != 0:
                        resultado_final += "\n"
                    resultado_final += conteudo

            # Exibe o conteúdo
            st.success(f"✅ {len(arquivos_txt)} arquivos .txt foram unidos com sucesso.")

            # Botão de download
            st.download_button(
                label="📥 Baixar resultado.txt",
                data=resultado_final,
                file_name="resultado.txt",
                mime="text/plain"
            )
