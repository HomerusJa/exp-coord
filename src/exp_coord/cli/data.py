from pathlib import Path

import typer
from pydantic import TypeAdapter
from structlog.stdlib import get_logger

from exp_coord.core.config import get_settings
from exp_coord.db.connection import create_grid_fs_client, init_db
from exp_coord.db.gridfs import ImageFileMetadata

from .utils import async_command

logger = get_logger(__name__)


app = typer.Typer()
images_app = typer.Typer(name="images")
app.add_typer(images_app, no_args_is_help=True)


@images_app.command("load-all")
@async_command
async def load_all_images(output_dir: Path):
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Using output directory: {output_dir}")

    # TODO: This should not be done here
    await init_db()
    bucket = create_grid_fs_client(get_settings().mongodb.collection_names.image_gridfs)
    metadata_dict: dict[str, ImageFileMetadata] = {}

    cursor = bucket.find({})  # find all files (empty filter)
    async for grid_out in cursor:
        file_id = grid_out._id
        filename = grid_out.filename or str(file_id)
        output_file = output_dir / filename.replace(":", "_")

        # Download the file content asynchronously and write to disk

        with open(output_file, "wb") as f:
            async for chunk in await bucket.open_download_stream(file_id):
                f.write(chunk)

        metadata_dict[filename] = ImageFileMetadata.model_validate(grid_out.metadata)

    with (output_dir / "metadata.json").open("wb") as f:
        ta = TypeAdapter(dict[str, ImageFileMetadata])
        f.write(ta.dump_json(metadata_dict))
