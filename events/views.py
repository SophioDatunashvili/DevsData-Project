from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from .forms import ReservationForm
from .models import Event, Reservation, Ticket
from .serializers import EventSerializer, ReservationSerializer


class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    # event = get_object_or_404(Event, pk=pk)
    # form = ReservationForm(request.POST or None)
    #
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         return redirect('event-list')
    #
    # else:
    #     form = ReservationForm
    #
    # return render(request, 'events/event_detail.html', {'event': event, 'form': form} )
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.event = event
            reservation.save()
            return redirect('reservation_detail', pk=reservation.pk, reservation_code=reservation.reservation_code)

    else:
        form = ReservationForm()
    return render(request, 'events/event_detail.html', {'event': event, 'form': form})


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        Ticket.objects.create(buyer=reservation, event=reservation.event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def update(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, reservation_code=kwargs['pk'])
        if (reservation.event.start_date - reservation.event.end_date).days > 2:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Reservation cannot be cancelled'})
        self.perform_update(reservation, request.data)
        return Response(status=status.HTTP_200_OK)


def reservation_detail(request, pk, reservation_code):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'events/reservation_detail.html', {'reservation': reservation})


def delete_reservation(request):
    if request.method == 'POST':
        reservation_code = request.POST.get('reservation_code')
        reservation = get_object_or_404(Reservation, reservation_code=reservation_code)
        reservation.delete()
        return redirect('reservation_deleted')
    return render(request, 'events/delete_reservation.html')


def reservation_deleted(request):
    return render(request, 'events/reservation_deleted.html')
