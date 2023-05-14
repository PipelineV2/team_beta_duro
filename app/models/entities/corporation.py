from typing import Optional

from app.models.core import IDModelMixin, TimestampsMixin
from app.models.entities.core.email import EmailMixin


class CorporationBase(EmailMixin):
    name: str
    description: Optional[str]
    legal_name: Optional[str]
    telephone: Optional[str]
    url: Optional[str]
    tax_id: Optional[str]
    vat_id: Optional[str]


class Corporation(CorporationBase):
    # address: str
    ...


class CorporationDBModel(TimestampsMixin, Corporation, IDModelMixin):
    ...
