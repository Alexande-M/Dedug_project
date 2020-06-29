from django.db.models import transaction


@api_view('POST')
def deposit(request):
    try:
        amount = int(request.data\['amount'\])
    except (KeyError, ValueError):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        try:
            account = (
                Account.objects
                .select_for_update()
                .get(user=request.user)
            )
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            account.deposit(
                amount=amount,
                deposited_by=request.user,
                asof=timezone.now(),
            )
        except (ExceedsLimit, InvalidAmount):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)