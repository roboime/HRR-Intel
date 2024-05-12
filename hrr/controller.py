import logging
from colorama import Fore, Style
from typing import Any, Literal
from hrr.estado import Estado
from hrr.exceptions import ModelNotFoundException

logging.basicConfig(level=logging.INFO, format=Fore.GREEN + '[%(levelname)s] %(message)s' + Style.RESET_ALL)

# Implement Kalman Filter here, if useful


class Controller:
    '''
    Classe controladora do robô, que implementa as funcionalidades de controle do robô em nível lógico, como:
    - Desvio de obstáculo
    - Desvio de degrau
    - Alinhamento

    Essas decisões podem ser tomadas através de um modelo de aprendizado de máquina (ML) ou através de um algoritmo de computação gráfica.
    '''


    __slots__ = ['_is_ml', '_hardware_components']

    def __init__(self, type: Literal['standard', 'ml'], hardware_components: dict) -> None:
        self._is_ml = type == 'ml'
        self._hardware_components = hardware_components
        if self._is_ml:
            try:
                logging.info('Importando modelo de aprendizado de máquina')
                pass
            except FileNotFoundError:
                raise ModelNotFoundException()


    def __str__(self) -> str:
        return f'Controller type: {"ML" if self._is_ml else "Standard"}' 

    def _desvio_obstaculo(self) -> None:
        pass

    def _desvio_degrau(self) -> None:
        pass

    def _alinhamento(self) -> None:
        pass

    def _decisao_ml(self) -> Estado:
        pass

    def _decisao_standard(self) -> Estado:
        pass

    def proximo_estado(self) -> Estado:
        if self._is_ml:
            return self._decisao_ml()
        
        else:
            return self._decisao_standard()


    