from models.db import _Sessao, ServidorBase, FeedConfig

class Manipular_Servidor:
    def Obter_todos_servidore():
        with _Sessao() as sessao:
            listaServidores = sessao.query(ServidorBase).all()
            print(listaServidores)
            return listaServidores
        
    def Obter_todos_feeds():
        with _Sessao() as sessao:
            listaFeeds = sessao.query(FeedConfig).all()
            print(listaFeeds)
            return listaFeeds

    def Obter_servidor(id_servidor:int):
        with _Sessao() as sessao:
            servidor = sessao.query(ServidorBase).filter_by(id_servidor=id_servidor).first()
            if servidor:
                print(servidor)
                return servidor
            return None
        
    def Obter_feed(id_ServidorBase:int):
        with _Sessao() as sessao:
            feed = sessao.query(FeedConfig).filter_by(id_ServidorBase=id_ServidorBase).first()
            if feed:
                print(feed)
                return feed
            return None

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
                sessao.commit()
                return True
            print("Servidor ja cadastrado")
            return None

            