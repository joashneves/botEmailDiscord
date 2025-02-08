from models.db import _Sessao, Usuario, Seguindo, UsuariosBanidos

class Manipular_Usuario:
    def Obter_usuario(id_discord: int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                print("usuario não existe")
                return None
            print(usuario)
            return usuario

    def Criar_usuario(id_discord: int, apelido:str, descricao:str, pronome: str = "N/a", id_ServidorBase:int = None):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                NovoUsuario = Usuario(
                    id_discord=id_discord,
                    aceita_dm=True,
                    apelido=apelido,
                    descricao=descricao,
                    pronome=pronome,
                    post=0,
                    id_ServidorBase=id_ServidorBase)
                sessao.add(NovoUsuario)
                print(f"Usuario criado {NovoUsuario}")
                sessao.commit()
                return True
            return None
        
    def Atualiza_usuario(id_discord: int, descricao:str, pronome: str = "N/a"):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()    
            print(usuario)
            if not usuario:
                print("Usuario não existe")
                return None
            usuario.descricao = descricao
            usuario.pronome = pronome
            sessao.commit()
            return True
        
    def Atualiza_post(id_discord:int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not Usuario:
                return None
            usuario.post += 1;
            sessao.commit()
            return True
            