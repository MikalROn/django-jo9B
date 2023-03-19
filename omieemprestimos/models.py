from django.db import models


class Lojas(models.Model):
    nome = models.CharField(max_length=64)
    
    def __str__(self) -> str:
        return f'{self.nome}'


class Emprestimos(models.Model):
    data = models.DateField()
    credor = models.ForeignKey(Lojas, on_delete=models.CASCADE, related_name='emprestimos_credor')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    devedor = models.ForeignKey(Lojas, on_delete=models.CASCADE, related_name='emprestimos_devedor')
    status = models.CharField(max_length=20, choices=(('PAGO', 'Ja foi pago'), ('DEVENDO', 'Nao foi pago')))
    
    def __str__(self):
        return f'dia {self.data} {self.credor.nome} emprestou {self.valor} para {self.devedor.nome}, ( status: {self.status})'
    