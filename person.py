class Person:
  cpf = None
  cnh = None
  cnpj = None
  pis = None
  titulo = None
  cep = None
  endereco = None
  celular = None
  
  def serialize(self):
      return {
          'cpf': self.cpf, 
          'cnh': self.cnh,
          'cnpj': self.cnpj,
          'pis': self.pis,
          'titulo': self.titulo,
          'cep': self.cep,
          'endereco': self.endereco,
          'celular': self.celular
      }