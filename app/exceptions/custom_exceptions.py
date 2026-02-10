class ClienteNoEncontradoError(Exception):
    """El cliente especificado no existe"""
    pass
class ClienteYaExisteError(Exception):
    """Ya existe un cliente con el mismo email"""
    pass   
class MesaNoDisponibleError(Exception):
    """La mesa no está disponible en el horario solicitado"""
    pass

class ReservaSolapadaError(Exception):
    """Ya existe una reserva para esa mesa en ese horario"""
    pass

class CapacidadExcedidaError(Exception):
    """El número de comensales excede la capacidad de la mesa"""
    pass

class FueraDeHorarioError(Exception):
    """La reserva está fuera del horario de operación"""
    pass

class CancelacionNoPermitidaError(Exception):
    """La reserva no puede cancelarse (muy tarde o estado inválido)"""
    pass

class MesaNoExisteError(Exception):
    """"No existe una mesa con esta informaciones"""
    pass

class MesaYaExisteError(Exception):
    """Ya existe una mesa con este numero de mesa"""
    pass  