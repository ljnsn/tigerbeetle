"""PDM build hooks."""

from pathlib import Path

c_header = Path(__file__).parent.joinpath("tb_client", "native", "tb_client.h")


# def pdm_build_initialize(context):
#     context.ensure_build_dir()  # make sure it is created.
#     bd = Path(context.build_dir)
#     bd.joinpath("native").mkdir(parents=True, exist_ok=True)
#     with bd.joinpath("native", "tb_client.h").open("w") as f:
#         f.write(here.read_text())


def pdm_build_update_setup_kwargs(context, setup_kwargs):
    setup_kwargs.update(cffi_modules=["build.py:ffibuilder"])
