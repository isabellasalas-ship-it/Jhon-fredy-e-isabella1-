from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Asignatura
from .serializers import AsignaturaSerializer


@api_view(["GET", "POST"])
def asignatura_lista(request):
    if request.method == "GET":
        asignaturas = Asignatura.objects.all()
        serializer = AsignaturaSerializer(asignaturas, many=True)
        return Response(serializer.data)                          # 200

    # POST
    serializer = AsignaturaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def asignatura_detalle(request, pk):
    try:
        asignatura = Asignatura.objects.get(pk=pk)
    except Asignatura.DoesNotExist:
        return Response(
            {"detail": "Asignatura no encontrada."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        return Response(AsignaturaSerializer(asignatura).data)   # 200

    if request.method in ("PUT", "PATCH"):
        serializer = AsignaturaSerializer(
            asignatura,
            data=request.data,
            partial=(request.method == "PATCH"),
        )
        serializer.is_valid(raise_exception=True)               # 400 automático
        serializer.save()
        return Response(serializer.data)                          # 200

    # DELETE
    asignatura.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
