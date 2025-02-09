from models.db import _Sessao, Seguindo

class Manipular_seguidor:
    def Obter_seguidores(id_alvo):
        with _Sessao() as sessao:
            seguidores = sessao.query(Seguindo).filter_by(id_usuario_alvo=id_alvo).all()
            if not seguidores:
                print("Ninguem segue esse cara")
                return None
            print("Seguidores", seguidores)
            return seguidores

    def Obter_seguindo(id_pessoa_seguindo):
        with _Sessao() as sessao:
            seguindo_lista = sessao.query(Seguindo).filter_by(id_usuario_seguidor=id_pessoa_seguindo).all()
            if not seguindo_lista:
                print("não segue ninguem")
                return None
            print("Seguindo:", seguindo_lista.count)
            return seguindo_lista

    def Seguir_pessoa(id_pessoa_seguir, id_alvo):
        with _Sessao() as sessao:
            seguidores = sessao.query(Seguindo).filter_by(id_usuario_seguidor=id_pessoa_seguir,id_usuario_alvo=id_alvo).first()
            if not seguidores:
                seguidor = Seguindo(
                    id_usuario_seguidor=id_pessoa_seguir,
                    id_usuario_alvo=id_alvo
                )
                sessao.add(seguidor)
                sessao.commit()
                return True
            print("Fulano ja segue")
            return False

    def remover_seguidor(id_pessoa_seguidora, id_alvo):
        with _Sessao() as sessao:
            seguidor = sessao.query(Seguindo).filter_by(id_usuario_seguidor=id_pessoa_seguidora,id_usuario_alvo=id_alvo).first()
            if not seguidor:
                print("Seguidor não existe para deletar")
                return False
            sessao.delete(seguidor)
            sessao.commit()
            return True
