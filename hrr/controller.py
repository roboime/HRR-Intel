from typing import Any, Literal
import os
import pathlib
from hrr.estado import Estado
from hrr.exceptions import ModelNotFoundException, CameraNotFoundException
from hrr.constantes import *


class Controller:
    '''
    Classe controladora do robô, que implementa as funcionalidades de controle do robô em nível lógico, como:
    - Desvio de obstáculo
    - Desvio de degrau
    - Alinhamento

    Essas decisões podem ser tomadas através de um modelo de aprendizado de máquina (ML) ou através de um algoritmo de computação gráfica.

    Esta classe é também responsável por todas as operações lógicas do robô, como a decisão de qual estado o robô deve seguir baseado nas informações obtidas dos sensores e
    também na previsão de estados futuros (baseado em Filtro de Kalman, por exemplo, caso haja).
    '''

    def __init__(self, type: Literal['standard', 'ml'], hardware_components: dict) -> None:
        self._is_ml = type == 'ml'
        self._hardware_components = hardware_components
        self._model = None
        self._align_mode = 'gyro'
        self._distance_tracker = 'sensor-distancia'
        self._is_taking_decision = False
        self._last_decision = Estado.PARAR
        if self._is_ml:
            try:
                logging.info('Importando modelo de aprendizado de máquina')
                self._import_model('ai_model')
            except FileNotFoundError:
                raise ModelNotFoundException()
        
        if 'camera' not in self._hardware_components:
            logging.error('Câmera não encontrada.')
            raise CameraNotFoundException('Câmera não encontrada.')
        
        if 'gyro' not in self._hardware_components:
            logging.warning('Giroscópio não encontrado. Alinhamento será feito através da câmera.')
            self._align_mode = 'camera'

        if 'sensor_distancia' not in self._hardware_components:
            logging.warning('Sensor de distância não encontrado. Distância será calculada através da câmera.')
            self._distance_tracker = 'camera'

        logging.info(f'Controller inicializado com sucesso. Alinhamento: {self._align_mode}. Distância: {self._distance_tracker}')   

    def __str__(self) -> str:
        return f'Controller type: {"ML" if self._is_ml else "Standard"}' 

    def _import_model(self, file_prefix: str) -> None:
        h5_path = pathlib.Path(__file__).parent / (file_prefix + '.h5')
        pkl_path = pathlib.Path(__file__).parent / (file_prefix + '.pkl')
        if h5_path.exists():
            logging.info(f'Importando de {h5_path}')
            ...
        elif pkl_path.exists():
            logging.info(f'Importando de {pkl_path}')
            ...
        else:
            logging.error('Modelo de IA não encontrado.')
            raise FileNotFoundError()

    def _desvio_obstaculo(self) -> Estado: pass

    def _desvio_degrau(self) -> Estado: pass

    def _alinhamento(self) -> Estado: pass

    def _decisao_ml(self) -> Estado: pass

    def _decisao_standard(self) -> Estado: 
        pass            

    def proximo_estado(self) -> Estado:
        if self._is_ml:
            return self._decisao_ml()
        
        else:
            return self._decisao_standard()


    