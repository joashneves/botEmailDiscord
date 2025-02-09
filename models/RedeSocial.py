from models.db import _Sessao, RedesSociais

class Manipular_redesSociais:
    def Obter_redes_de_usuario(id_usuario):
        with _Sessao() as sessao:
            redes = sessao.query(RedesSociais).filter_by(id_usuario=id_usuario).all()
            return redes

    def Criar_redes(id_usuario, nome, link):
        with _Sessao() as sessao:
            rede = sessao.query(RedesSociais).filter_by(id_usuario=id_usuario, nome=nome, link=link).first()
            if not rede:
                novaRede = RedesSociais(
                    id_usuario=id_usuario,
                    nome=nome,
                    link=link)
                sessao.add(novaRede)
                sessao.commit()
                return True
            return None

    def Remover_rede(id_usuario, nome):
        with _Sessao() as sessao:
            rede = sessao.query(RedesSociais).filter_by(id_usuario=id_usuario, nome=nome).first()
            if not rede:
                print("Usuario não tem rede")
                return False
            sessao.delete(rede)
            sessao.commit()
            return True
