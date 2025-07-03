from django.db import models

class DeviceType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название типа устройства')
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'
    


class Object(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название объекта')
    adress = models.CharField(max_length=255, verbose_name='Адрес объекта')
    def __str__(self):
        return f'{self.name} - {self.adress}' 
    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, verbose_name='Тип устройства')
    name = models.CharField(max_length=255, verbose_name='Название устройства')
    model = models.CharField(max_length=255, verbose_name='Модель устройства')
    ip = models.CharField(max_length=255, verbose_name='IP адрес устройства')
    login = models.CharField(max_length=255, verbose_name='Логин устройства')
    password = models.CharField(max_length=255, verbose_name='Пароль устройства')
    description = models.CharField(max_length=255, verbose_name='Описание устройства')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект', related_name='devices')
    def __str__(self):
        return f'{self.object} - {self.name}'
    
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'