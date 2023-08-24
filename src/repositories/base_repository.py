from mongoengine import QuerySet


class BaseRepository:
    model_class = None

    @classmethod
    def get(cls, **kwargs):
        return cls.model_class.objects.get(**kwargs)

    @classmethod
    def get_all(cls):
        return cls.model_class.objects.all()

    @classmethod
    def create(cls, **data):
        return cls.model_class(**data).save()

    @classmethod
    def update(cls, obj, **data):
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    @classmethod
    def delete(cls, obj):
        obj.delete()

    @classmethod
    def get_queryset(cls) -> QuerySet:
        return cls.model_class.objects
