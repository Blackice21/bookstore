from django.shortcuts import render, get_object_or_404

# Create your views here.
def my_profile(request):
    my_pro = get_object_or_404(Profile, user=request.user)
    context = {
        'my_pro': my_pro,
        'message':'You have No ebooks!'
    }
    return render(request,'my_profile.html', context)