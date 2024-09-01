#!/bin/bash

# Wyczyść plik wakealarm
echo 0 | sudo tee /sys/class/rtc/rtc0/wakealarm

# Sprawdź, czy dzisiaj jest niedziela
current_day=$(date +%u)  # +%u zwraca numer dnia tygodnia, gdzie 1 = poniedziałek, 7 = niedziela

if [ "$current_day" -eq 7 ]; then
  # Jeśli dzisiaj jest niedziela, oblicz czas do dzisiejszej niedzieli o 21:00
  next_sunday=$(date -d "21:55" +%s)
else
  # Jeśli dzisiaj nie jest niedziela, oblicz czas do nadchodzącej niedzieli o 21:00
  next_sunday=$(date -d "next sunday 21:55" +%s)
fi

current_time=$(date +%s)
seconds_until_next_sunday=$((next_sunday - current_time))

# Ustaw alarm RTC
echo "+$seconds_until_next_sunday" | sudo tee /sys/class/rtc/rtc0/wakealarm
