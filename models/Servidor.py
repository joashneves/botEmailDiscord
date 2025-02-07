from models.db import _Sessao, ServidorBase, FeedConfig

class Manipular_Servidor:
    def Obter_servidor(id_servidor:int):
        with _Sessao() as sessao:
            servidor = sessao.query(ServidorBase).filter_by(id_servidor=id_servidor)
            if not servidor:
                print("Servidor não cadastrado")
                return "Servidor não cadastrado"
            print(servidor)
            return servidor
        
    def Obter_feed(id_ServidorBase:int):
        with _Sessao() as sessao:
            feed = sessao.query(FeedConfig).filter_by(id_ServidorBase=id_ServidorBase)
            if not feed:
                return "Não existe"
            print(feed)
            return feed

    def Registrar_servidor(id_servidor: int, email: str, id_chat:int):
        with _Sessao() as sessao:
            servidor = sessao.query(ServidorBase).filter_by(id_servidor=id_servidor).first()
            if not servidor:
                servidorNovo = ServidorBase(
                    id_servidor=id_servidor,
                    email=email,)
                sessao.add(servidorNovo)
                feedNovo = FeedConfig(
                    id_ServidorBase=id_servidor,
                    id_chat=id_chat)
                sessao.add(feedNovo)
                print(f"Servidor : {servidorNovo} e feed {feedNovo}")
                return "Servidor cadastrado"
            return "Servidor ja cadastrado"

            