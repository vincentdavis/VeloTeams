from ninja import ModelSchema, NinjaAPI

from .models import Profile

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


class ProfileSchema(ModelSchema):
    class Config:
        model = Profile
        model_fields = "__all__"


@api.get("/zp/Profile", response=list[ProfileSchema])
def profile(request):
    return Profile.objects.all()
