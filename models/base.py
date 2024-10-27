from mongoengine import (
    DynamicDocument,
)
from mongoengine.fields import (
    DateTimeField,
)
from fp_common.fp_utils.time_utils import get_now_time


class BaseModel(DynamicDocument):
    meta = {'allow_inheritance': True}
    created_datetime = DateTimeField(verbose_name='이동날짜', default=get_now_time)
    updated_datetime = DateTimeField(verbose_name='이동날짜', default=get_now_time)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        # Update the updated_datetime before saving
        document.updated_datetime = get_now_time()
