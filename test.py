import os
import time  # 引入time模块
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.data.dataset import SupportedPdfParseMethod

# 记录开始时间
start_time = time.time()
# args
pdf_file_name = "abc.pdf"  # replace with the real pdf path
name_without_suff = pdf_file_name.split(".")[0]

# prepare env
local_image_dir, local_md_dir = "output/images", "output"
image_dir = str(os.path.basename(local_image_dir))

os.makedirs(local_image_dir, exist_ok=True)

image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(
    local_md_dir
)

# read bytes
reader1 = FileBasedDataReader("")
pdf_bytes = reader1.read(pdf_file_name)  # read the pdf content

# proc
## Create Dataset Instance
ds = PymuDocDataset(pdf_bytes)

## inference
if ds.classify() == SupportedPdfParseMethod.OCR:
    ds.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(
    md_writer, f"{name_without_suff}.md", image_dir
)

else:
    ds.apply(doc_analyze, ocr=False).pipe_txt_mode(image_writer).dump_md(
    md_writer, f"{name_without_suff}.md", image_dir
)

# 记录结束时间
end_time = time.time()
# 打印总共花费时间
print(f"总共花费时间: {end_time - start_time:.2f} 秒")