
from opex.economic import EconomicConfig
from capex.equipments.equipments import teste_print
from capex.services import ProjectServices
from capex.models import EquipmentUnity
from .models import CashFlow, OpexAuxiliateFactor, OpexProjectSettings, ProjectUtilitiesConstant, fcilSourceList, Opex


class OpexServices():

    def __init__(self, projectNumber=None):
        if projectNumber is not None:
            self.project = ProjectServices.getProjectFromNum(projectNumber)

    # Retorna um OpexAuxiliateFactor com base no numero de projeto
    def getAuxiliateFactors(self, project: int):
        return OpexAuxiliateFactor.objects.filter(project__project_number=project).first()

    def getOpex(self, project: int):
        return Opex.objects.filter(project__project_number=project).first()

    def getProjectSettings(self, project: int):
        return OpexProjectSettings.objects.filter(project__project_number=project).first()

    def getUtilitiesConstants(self, project: int):
        return ProjectUtilitiesConstant.objects.filter(project__project_number=project).all()

    # Função auxiliar para criar função do COMd exibida no form
    def createComEquation(self, configs: OpexAuxiliateFactor):
        equation = "COMd = "
        equation = equation + (str(configs.fcil) + "*FCIL + ")
        equation = equation + (str(configs.col) + "*COL + ")
        equation = equation + (str(configs.cut) + "*(CUT + CWT + CRM) ")
        return equation

    def formUtilitiesConstants(values):
        fields = [
            'Common Utilities',
            'Steam from Boilers',
            'Fuels',
            'Thermal Systems',
            'Refrigeration',
            'Waste Disposal (solid and liquid)',
            'Process Equipment'
        ]

    # Listas a serem exportadas para o form de configuração da OPEX
    def listForms(self):
        export = {
            'fcilSource': fcilSourceList,
            'cut_constants': []
        }
        return export

    # Atualiza os valores recebidos do form Settings OPEX
    def updateOpexConfig(self, project, args):

        # atualizar ProjectUtilitiesConstant[ok], OpexAuxiliateFactor[ok], OpexProjectSettings[ok], Opex

        utilities = self.getUtilitiesConstants(project)
        listOfFields = list(utilities.values_list('aka', flat=True).distinct())
        listOfFields = set([*args]) & set(listOfFields)

        # TODO: Esta transação deveria ser feita utilizando transactions, porem ainda não foi possivel implementar
        for item in listOfFields:
            utilitie = utilities.filter(aka=item).first()
            utilitie.value = args[item]
            utilitie.save()
            listOfFields = {
                'crm': args['cut_cost_factor'],
                'cwt': args['cut_cost_factor'],
                'cut': args['cut_cost_factor'],
                'col': args['col_cost_factor'],
                'fcil': args['fcil_cost_factor'],
                'working_capital_a': args['factorA'],
                'working_capital_b': args['factorB'],
                'working_capital_c': args['factorC'],
                'year1': args['year1'],
                'year2': args['year2'],
                'year3': args['year3'],
                'year4': args['year4'],
                'year5': args['year5'],
            }

        auxiliarFactor = OpexAuxiliateFactor.objects.filter(project__project_number=project)
        auxiliarFactor.update(**listOfFields)

        settings = OpexProjectSettings.objects.filter(project__project_number=project)
        listOfFields = {
            'revenue_calculated': parse_boolean(args['revenue_source']),
            'crm_calculated': parse_boolean(args['crm_source']),
            'salvage_calculated': parse_boolean(args['salvage_source']),
            'cut_calculated': parse_boolean(args['cut_source']),
            'wc_calculated': parse_boolean(args['wc_source']),
            'col_calculated': parse_boolean(args['col_source']),
            'cwt_calculated': parse_boolean(args['cwt_source']),
            'construction_period': args['construction_period'],
            'project_life': args['project_life'],
            'cwt_calculated': args['construction_period'],
            'capex_source': args['fcil_source'],
        }

        settings.update(**listOfFields)

        opex = Opex.objects.filter(project__project_number=project).first()

        values = ['fcil_value', 'revenue_value', 'crm_value', 'salvage_value', 'cut_value', 'wc_value', 'col_value', 'cwt_value']
        listOfFields = set([*args]) & set(values)
        for lists in listOfFields:
            field = lists.replace("_value", "")
            setattr(opex, field, args[lists])
        opex.save()

        listOfFields = set(values) - set([*args])

        # TODO: atualizar aqui com calculos... pendente de equipamentos e materiais
        teste_print(listOfFields)

        return

    def formCreateMaterial(self):

        formValues = {
            'options': ['Raw Material', 'Product', 'Material Waste - Hazarduous', 'Material Waste - Non Hazarduous'],
            'buying_price_unity': EquipmentUnity.objects.filter(dimension__dimension='Mass Cost'),
            'material_flow_unity': EquipmentUnity.objects.filter(dimension__dimension='Mass Flow'),
        }
        return formValues


def parse_boolean(b):
    return b == 'True'
