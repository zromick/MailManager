from typing import TypeVar

from fastapi_pagination.customization import (
    CustomizedPage,
    UseIncludeTotal,
    UseParamsFields,
)
from fastapi_pagination.limit_offset import LimitOffsetPage as BaseLimitOffsetPage

# Pagination type based on docs: https://uriyyo-fastapi-pagination.netlify.app/learn/pagination/techniques/
# You can refer to the 'Techniques' section for different pagination types.

LimitOffsetPageType = TypeVar("LimitOffsetPageType")

# This can be used for any Pydantic model (e.g., MailItems)
GenericLimitOffsetPage = CustomizedPage[
    BaseLimitOffsetPage[LimitOffsetPageType],
    UseIncludeTotal(True),
    UseParamsFields(limit=10, offset=0),
]
