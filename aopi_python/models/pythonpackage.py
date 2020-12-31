from typing import Any, Dict, Optional

import orm

from aopi_python.ctx import context
from aopi_python.models.dist_info import DistInfoModel


class PythonPackage(orm.Model):
    __tablename__ = "python_packages"
    __database__ = context.database
    __metadata__ = context.metadata

    id = orm.Integer(primary_key=True)
    user_id = orm.Integer(allow_null=True, index=True)

    name = orm.Text(allow_null=False, index=True)
    author = orm.Text(allow_null=True)
    summary = orm.Text(allow_null=True)
    license = orm.Text(allow_null=True)
    keywords = orm.Text(allow_null=True)
    home_page = orm.Text(allow_null=True)
    maintainer = orm.Text(allow_null=True)
    project_urls = orm.Text(allow_null=True)
    author_email = orm.Text(allow_null=True)
    maintainer_email = orm.Text(allow_null=True)

    @staticmethod
    def cast_dist_info_to_data(upload: DistInfoModel) -> Dict[str, Any]:
        return dict(
            name=upload.name,
            summary=upload.summary,
            license=upload.license,
            keywords=upload.keywords,
            home_page=upload.home_page,
            author=upload.author,
            author_email=upload.author_email,
            project_urls=";".join(upload.project_urls) if upload.project_urls else None,
            maintainer=upload.maintainer,
            maintainer_email=upload.maintainer_email,
        )

    @classmethod
    async def create_by_dist_info(
        cls, *, upload: DistInfoModel, user_id: Optional[int]
    ) -> "PythonPackage":
        upload_dict = cls.cast_dist_info_to_data(upload)
        return await cls.objects.create(**upload_dict, user_id=user_id)

    async def update_by_dist_info(self, upload: DistInfoModel) -> None:
        upload_dict = self.cast_dist_info_to_data(upload)
        await self.update(**upload_dict)
