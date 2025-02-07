import os
import subprocess
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse

from api.schemas.agave_obj import AgaveObjModel
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

router = APIRouter()

UPLOAD_DIR = "./images"


async def save_and_convert_image(image_file: UploadFile) -> bool:
    """
    画像を受け取って、.avif 形式に変換し、保存してパスを返す
    """
    if image_file.filename is None:
        raise ValueError("Image file must have a filename.")

    temp_input_path = f"{UPLOAD_DIR}/{image_file.filename}"
    with open(temp_input_path, "wb") as f:
        f.write(await image_file.read())

    temp_output_path = (
        f"{UPLOAD_DIR}/{image_file.filename.rsplit('.', 1)[0]}.avif"
    )

    try:
        # ffmpegでAVIF形式に変換
        command = [
            "ffmpeg",
            "-i",
            temp_input_path,
            "-c:v",
            "libaom-av1",
            "-b:v",
            "0",
            "-crf",
            "30",
            temp_output_path,
        ]
        subprocess.run(command, check=True)
        return True

    except subprocess.CalledProcessError:
        return False
    finally:
        # 一時ファイルの削除
        os.remove(temp_input_path)


@router.post("/post/data")
async def post_agave_obj(
    name: str = Form(...),
    username: str = Form(...),
    username_source: str = Form(...),
    image_file: UploadFile = File(...),
    image_file_path: str = Form(...),
    source: str = Form(...),
    sourcename: str = Form(...),
    image_source: str = Form(...),
    origin_country: Optional[str] = Form(None),
    is_display: bool = Form(...),
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    """
    ESにアガベデータをアップロード
    """
    try:
        if not await save_and_convert_image(image_file):
            return False

        doc = AgaveObjModel(
            name=name,
            username=username,
            username_source=username_source,
            image_file_path=f"{UPLOAD_DIR}/{image_file_path.rsplit('.', 1)[0]}.avif",
            source=source,
            sourcename=sourcename,
            image_source=image_source,
            origin_country=(
                origin_country if origin_country is not None else "不明"
            ),
            is_display=is_display,
        ).__dict__

        builder = ESQueryBuilder()
        builder.set_bool()
        builder.set_should()
        builder.create_search_name_query("name", name)
        response = es.search(builder.build())
        if _check_doc(response["hits"]["hits"], doc):
            es.insert(doc)
            print(f"{name}を格納しました。")

        return True

    except Exception:
        import traceback

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )


def _check_doc(response, doc: dict) -> bool:
    for res in response:
        if doc == res["_source"]:
            return False
    return True
