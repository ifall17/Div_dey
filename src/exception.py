import sys
from src.logger import logging

#Custom exception
def error_message_detail (error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_infos() #Cette fonction renvoie un triplet contenant des informations sur l'exception actuellement traitée.

    file_name = exc_tb.tb_frame.f_code.co_filename #extraction du nom du fichier où l'exception s'est produite à partir de l'objet


    '''Le nom du fichier où l'erreur s'est produite (file_name).
        Le numéro de ligne où l'erreur s'est produite (exc_tb.tb_lineno).
            Le texte de l'erreur lui-même (str(error)).'''

    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message