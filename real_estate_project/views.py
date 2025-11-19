from django.shortcuts import render, redirect
from .NetworkHelper import NetworkHelper

helper_1 = NetworkHelper(
    api_url="http://127.0.0.1:7000/companies",
    token="ac45e86b0efaa07abfe666c2ae110dece7b46670"
)

helper_2 = NetworkHelper(
    api_url="http://127.0.0.1:7000/directors",
    token="ac45e86b0efaa07abfe666c2ae110dece7b46670"
)

def list_companies_api(request):
    items = helper_1.get_list_api()
    if request.method == "POST":
        item_id = request.POST.get("delete_id")
        response = helper_1.delete_item_api(item_id)
        print("DELETE response:", response.status_code, response.text)
        return redirect("list_companies_api")
    return render(request, "list_companies_api.html", {"items": items})


def list_directors_api(request):
    items = helper_2.get_list_api()
    if request.method == "POST":
        item_id = request.POST.get("delete_id")
        response = helper_2.delete_item_api(item_id)
        print("DELETE response:", response.status_code, response.text)
        return redirect("list_directors_api")
    return render(request, "list_directors_api.html", {"items": items})