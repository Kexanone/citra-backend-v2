def base(request):
    """
    Contexts for
    """
    return {
        'hostname': request.get_host(),
    }
